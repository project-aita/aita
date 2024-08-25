from typing import Any, List, Optional

import logging

import reflex as rx
from sqlmodel import delete, select

from ryoma.datasource.base import DataSource as DataSourceBase
from ryoma.datasource.factory import DataSourceFactory, DataSourceProvider
from ryoma_lab.apis.datasource import get_datasource_by_name, get_datasource_configs
from ryoma_lab.models.datasource import DataSource


class DataSourceState(rx.State):
    id: int
    name: str
    datasource: Optional[str] = ""
    connection_url: str
    attributes: dict[str, str] = {}
    catalog_id: int
    sort_value: str
    is_open: bool = False
    allow_crawl_catalog: bool = True

    config_type: str = "connection_url"

    datasources: list[DataSource] = []
    open_alert: bool = False

    def change_crawl_catalog(self, value: bool):
        self.allow_crawl_catalog = value

    @rx.var
    def datasource_names(self) -> List[str]:
        return [datasource.name for datasource in self.datasources]

    @rx.var
    def num_datasources(self) -> int:
        return len(self.datasources)

    def _datasource_fields(self, datasource: str) -> dict[str, Any]:
        fields = DataSourceProvider[datasource].value.__fields__.copy()
        for additional_field in ["type", "name", "connection_url"]:
            if additional_field in fields:
                del fields[additional_field]
        return fields

    @rx.var
    def datasource_attribute_names(self) -> List[str]:
        if self.datasource:
            fields = self._datasource_fields(self.datasource)
            return [key for key in fields]
        else:
            return []

    @rx.var
    def missing_configs(self) -> bool:
        # Required by all data sources
        if not self.datasource or not self.name:
            return True

        # Use connection_url
        if self.config_type == "connection_url":
            if not self.connection_url:
                return True
        else:
            # Required by the data source
            model_fields = self._datasource_fields(self.datasource)
            for key in model_fields:
                if model_fields[key].required and not self.attributes.get(key):
                    return True
        return False

    def set_datasource_attributes(self, attribute: str, value: str):
        self.attributes[attribute] = value

    def get_datasource_attributes(self) -> dict[str, str]:
        model_fields = self._datasource_fields(self.datasource)
        ds_attrs = {key: self.attributes.get(key, "") for key in model_fields}
        return ds_attrs

    def get_datasource_configs(self) -> dict:
        if self.config_type == "connection_url":
            return {"connection_url": self.connection_url}
        else:
            return self.attributes

    def load_entries(self):
        with rx.session() as session:
            self.datasources = session.exec(select(DataSource)).all()

            if self.sort_value:
                self.datasources = sorted(
                    self.datasources,
                    key=lambda datasource: getattr(datasource, self.sort_value).lower(),
                )

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def render_update_datasource(self, datasource: DataSource):
        self.id = datasource["id"]
        self.name = datasource["name"]
        self.datasource = datasource["datasource"]
        self.connection_url = datasource["connection_url"]
        attributes = eval(datasource["attributes"])
        for key, value in attributes.items():
            self.attributes[key] = value

    def connect_and_add_datasource(self):
        if self.missing_configs:
            return
        configs = self.get_datasource_configs()
        try:
            ds = DataSourceFactory.create_datasource(self.datasource, **configs)
            ds.connect()
            logging.info(f"Connected to {self.datasource}")
        except Exception as e:
            logging.error(f"Failed to connect to {self.datasource}: {e}")
            return rx.toast.error(f"Failed to connect to {self.datasource}: {e}")
        with rx.session() as session:
            datasource = self.build_datasource()
            session.add(datasource)
            session.commit()
        self.load_entries()

    def build_datasource(self, datasource: Optional[DataSource] = None):
        datasource_attrs = self.get_datasource_attributes()

        datasource_params = {
            "name": self.name,
            "datasource": self.datasource,
            "connection_url": self.connection_url,
            "attributes": str(datasource_attrs),
        }

        if not datasource:
            datasource = DataSource(**datasource_params)
        else:
            for key, value in datasource_params.items():
                setattr(datasource, key, value)

        return datasource

    def update_datasource(self, ds_id: str):
        with rx.session() as session:
            datasource = session.exec(select(DataSource).where(DataSource.id == ds_id)).first()
            datasource = self.build_datasource(datasource)
            session.add(datasource)
            session.commit()
        self.load_entries()

    def delete_datasource(self, datasource_id: str):
        with rx.session() as session:
            session.exec(delete(DataSource).where(DataSource.id == datasource_id))
            session.commit()
        self.load_entries()

    @staticmethod
    def connect(datasource_name: str) -> Optional[DataSourceBase]:
        ds = get_datasource_by_name(datasource_name)
        configs = get_datasource_configs(ds)
        if not ds:
            return
        try:
            source = DataSourceFactory.create_datasource(ds.datasource, **configs)
            source.connect()
            logging.info(f"Connected to {ds.datasource}")
            return source
        except Exception as e:
            logging.error(f"Failed to connect to {ds.datasource}: {e}")

    def on_load(self):
        self.load_entries()

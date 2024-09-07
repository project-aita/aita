import logging
import os
from pathlib import Path
from typing import Optional

import reflex as rx
from feast.feature_store import FeatureStore

from ryoma_lab.models.vector_store import FeatureViewModel, VectorStore
from ryoma_lab.services.datasource import DataSourceService
from ryoma_lab.services.vector_store import VectorStoreService
from ryoma_lab.states.ai import AIState


class VectorStoreState(AIState):
    projects: list[VectorStore] = []
    project: Optional[VectorStore] = None

    # Vector store configuration
    project_name: str
    online_store: str
    offline_store: Optional[str] = ""
    embedding_dimension: int = 512

    # Feature view configuration
    feature_view_name: str
    feature_name: str
    feature_entity_name: Optional[str] = None
    feature_datasource: Optional[str] = None

    # Feast feature store
    _current_fs: Optional[FeatureStore] = None
    current_feature_views: list[FeatureViewModel] = []

    create_store_dialog_open: bool = False
    create_feature_dialog_open: bool = False
    materialize_feature_dialog_open: bool = False

    files: list[str] = []
    feature_source_configs: dict[str, str] = {}

    def set_feature_source_config(self, key: str, value: str):
        self.feature_source_configs[key] = value

    def _get_datasource_configs(self, ds: str) -> dict[str, str]:
        with DataSourceService() as datasource_service:
            datasource = datasource_service.get_datasource_by_name(ds)
            if datasource:
                configs = datasource_service.get_datasource_configs(datasource)
        if not configs:
            return {}
        if "connection_url" in configs:
            configs = {
                "path": configs["connection_url"],
            }
        return configs

    def set_online_store(self, ds: str):
        self.online_store = ds
        logging.info(
            f"Online store type set to {self.online_store} with configs {self.online_store_configs}"
        )

    def set_offline_store(self, ds: str):
        self.offline_store = ds
        logging.info(
            f"Offline store type set to {self.offline_store} with configs {self.offline_store_configs}"
        )

    def toggle_create_feature_dialog(self):
        self.create_feature_dialog_open = not self.create_feature_dialog_open

    def toggle_create_store_dialog(self):
        self.create_store_dialog_open = not self.create_store_dialog_open

    def toggle_materialize_feature_dialog(self):
        self.materialize_feature_dialog_open = not self.materialize_feature_dialog_open

    def set_project(self, project_name: str):
        self.project_name = project_name
        self._reload_store(self.project_name)

    def get_project(self, project_name: str):
        return next(
            (
                project
                for project in self.projects
                if project.project_name == project_name
            ),
            None,
        )

    def _reload_store(self, project_name: Optional[str] = None):
        project = None
        if project_name:
            project = self.get_project(project_name)
        elif self.projects:
            project = self.projects[0]
        if project:
            self.project = project
            with VectorStoreService() as vector_store_service:
                self._current_fs = vector_store_service.get_feature_store(self.project)
                self.current_feature_views = vector_store_service.get_feature_views(
                    self._current_fs
                )

    def create_store(self):
        datasource_configs = self._get_datasource_configs(self.online_store)
        online_store_configs = {
            "type": self.online_store,
            **datasource_configs,
            "dimension": self.embedding_dimension,
        }

        repo_config_input = {
            "project_name": self.project_name,
            "online_store": self.online_store,
            "online_store_configs": online_store_configs,
            "offline_store": self.offline_store,
            "offline_store_configs": None,
        }
        logging.info(
            "Creating feature store with the following configurations: %s",
            repo_config_input,
        )

        try:
            with VectorStoreService() as vector_store_service:
                vector_store_service.apply_feature_store(repo_config_input)

                logging.info("Feature store applied successfully.")

                # save the project to the database
                vector_store_service.save_project(**repo_config_input)
            self.load_store()
        except Exception as e:
            logging.error(f"Error creating feature store: {e}")
            raise e
        finally:
            self.toggle_create_store_dialog()

    def create_vector_feature(self):
        with VectorStoreService() as vector_store_service:
            vector_store_service.create_vector_feature_view(
                self._current_fs,
                feature_view_name=self.feature_view_name,
                feature_name=self.feature_name,
                entity=(self.feature_entity_name, self.feature_entity_name),
                source_type=self.feature_datasource,
                source_configs=self.feature_source_configs,
                files=self.files,
            )
        logging.info(f"Feature View {self.feature_view_name} created")
        self._reload_store()
        self.toggle_create_feature_dialog()

    def index_feature(self, feature_view: FeatureViewModel):
        logging.info(f"Indexing feature view {feature_view}")
        with VectorStoreService() as vector_store_service:
            vector_store_service.index_feature_from_source(
                self._current_fs, feature_view
            )
        logging.info(f"Feature view {feature_view} indexed")

    def load_store(self):
        with VectorStoreService() as vector_store_service:
            self.projects = vector_store_service.load_projects()
        self._reload_store()

        logging.info("Feature store loaded")

    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        root_dir = rx.get_upload_dir()
        source_dir = f"{root_dir}/{self.feature_view_name}"
        if not os.path.exists(source_dir):
            os.makedirs(source_dir)

        for file in files:
            upload_data = await file.read()
            outfile = Path(f"{source_dir}/{file.filename}")

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the files var.
            self.files.append(file.filename)

    def delete_project(self, project_name):
        with VectorStoreService() as vector_store_service:
            vector_store_service.delete_project(project_name)
        self.load_store()

    def on_load(self) -> None:
        self.load_store()

from typing import Union

from enum import Enum

from ryoma.agent.arrow_agent import ArrowAgent
from ryoma.agent.base import RyomaAgent
from ryoma.agent.embedding import EmbeddingAgent
from ryoma.agent.pandas_agent import PandasAgent
from ryoma.agent.python_agent import PythonAgent
from ryoma.agent.spark_agent import SparkAgent
from ryoma.agent.sql import SqlAgent
from ryoma.agent.workflow import WorkflowAgent


class AgentProvider(Enum):
    ryoma = RyomaAgent
    sql = SqlAgent
    pandas = PandasAgent
    pyarrow = ArrowAgent
    pyspark = SparkAgent
    python = PythonAgent
    embedding = EmbeddingAgent


def get_builtin_agents():
    return list(AgentProvider)


class AgentFactory:

    @staticmethod
    def create_agent(agent_type: str, *args, **kwargs) -> Union[RyomaAgent, WorkflowAgent]:
        if not agent_type or not hasattr(AgentProvider, agent_type):
            agent_class = RyomaAgent
        else:
            agent_class = AgentProvider[agent_type].value
        return agent_class(*args, **kwargs)

# Ryoma
AI Powered Data Agent framework, a comprehensive solution for data analysis, engineering, and visualization.

[![Build status](https://github.com/project-ryoma/ryoma/workflows/build/badge.svg)](https://github.com/project-ryoma/ryoma/actions/workflows/build.yml?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/ryoma.svg)](https://pypi.org/project/ryoma/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/project-ryoma/ryoma/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/project-ryoma/ryoma/blob/main/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/project-ryoma/ryoma)](https://github.com/project-ryoma/ryoma/blob/main/LICENSE)
[![Coverage Report](assets/images/coverage.svg)](https://github.com/project-ryoma/ryoma/blob/main/assets/images/coverage.svg)

## Tech Stack

Our platform leverages a combination of cutting-edge technologies and frameworks:

- **[Langchain](https://www.langchain.com/)**: Facilitates the seamless integration of language models into application workflows, significantly enhancing AI interaction capabilities.
- **[Reflex](https://reflex.dev/)**: An open-source framework for quickly building beautiful, interactive web applications in pure Python
- **[Apache Arrow](https://arrow.apache.org/)**: A cross-language development platform for in-memory data that specifies a standardized language-independent columnar memory format for flat and hierarchical data, organized for efficient analytic operations on modern hardware like CPUs and GPUs.
- **[Jupyter Ai Magics](https://github.com/jupyterlab/jupyter-ai)**: A JupyterLab extension that provides a set of magics for working with AI models.
- **[Amundsen](https://www.amundsen.io/)**: A data discovery and metadata platform that helps users discover, understand, and trust the data they use.
- **[Ibis](https://ibis-project.org/)**: A Python data analysis framework that provides a pandas-like API for analytics on large datasets.
- **[Feast](https://feast.dev/)**: An operational feature store for managing and serving machine learning features to models in production.

## Installation
Simply install the package using pip:

```shell
pip install ryoma_ai
```
Or with extra dependencies:

```shell
pip install ryoma_ai[snowflake]
```

## Basic Example
Below is an example of using Ryoma to connect to a postgres database and ask a question.
You can read more details in the [documentation](https://project-ryoma.github.io/ryoma/).

```python
from ryoma_ai import Ryoma
from ryoma_data import DataSource

# Connect to a postgres database
datasource = DataSource(
    "postgres",
    host="localhost",
    port=5432,
    database="dbname",
    user="user",
    password="password"
)

# Create Ryoma instance and SQL agent
ryoma = Ryoma(datasource=datasource)
agent = ryoma.sql_agent(model="gpt-4", mode="enhanced")

# Ask question to the agent
agent.stream("I want to get the top 5 customers which making the most purchases", display=True)
```

The Sql agent will try to run the tool as shown below:
```text
================================ Human Message =================================

I want to get the top 5 customers which making the most purchases
================================== Ai Message ==================================
Tool Calls:
  sql_database_query (call_mWCPB3GQGOTLYsvp21DGlpOb)
 Call ID: call_mWCPB3GQGOTLYsvp21DGlpOb
  Args:
    query: SELECT C.C_NAME, SUM(L.L_EXTENDEDPRICE) AS TOTAL_PURCHASES FROM CUSTOMER C JOIN ORDERS O ON C.C_CUSTKEY = O.O_CUSTKEY JOIN LINEITEM L ON O.O_ORDERKEY = L.L_ORDERKEY GROUP BY C.C_NAME ORDER BY TOTAL_PURCHASES DESC LIMIT 5
    result_format: pandas
```
Continue to run the tool with the following code:
```python
from ryoma_ai.agent.workflow import ToolMode
sql_agent.stream(tool_mode=ToolMode.ONCE)
```
Output will look like after running the tool:
```text
================================== Ai Message ==================================

The top 5 customers who have made the most purchases are as follows:

1. Customer#000143500 - Total Purchases: $7,154,828.98
2. Customer#000095257 - Total Purchases: $6,645,071.02
3. Customer#000087115 - Total Purchases: $6,528,332.52
4. Customer#000134380 - Total Purchases: $6,405,556.97
5. Customer#000103834 - Total Purchases: $6,397,480.12
```

## Use Ryoma Lab
Ryoma lab is an application that allows you to interact with your data and AI models in UI.
The ryoma lab is built with [Reflex](https://reflex.dev/).

1. Create Ryoma lab configuration file `rxconfig.py` in your project:
```python
import logging

import reflex as rx
from reflex.constants import LogLevel

config = rx.Config(
    app_name="ryoma_lab",
    loglevel=LogLevel.INFO,
)

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
```

2. You can start the ryoma lab by running the following command:
```shell
ryoma_lab run
```
the ryoma lab will be available at `http://localhost:3000`.
![ui.png](assets%2Fui.png)

## Supported Models
Model provider are supported by jupyter ai magics. Ensure the corresponding environment variables are set before using the Ryoma agent.

| Provider            | Provider ID          | Environment variable(s)    | Python package(s)               |
|---------------------|----------------------|----------------------------|---------------------------------|
| AI21                | `ai21`               | `AI21_API_KEY`             | `ai21`                          |
| Anthropic           | `anthropic`          | `ANTHROPIC_API_KEY`        | `langchain-anthropic`           |
| Anthropic (playground)    | `anthropic-playground`     | `ANTHROPIC_API_KEY`        | `langchain-anthropic`           |
| Bedrock             | `bedrock`            | N/A                        | `boto3`                         |
| Bedrock (playground)      | `bedrock-playground`       | N/A                        | `boto3`                         |
| Cohere              | `cohere`             | `COHERE_API_KEY`           | `cohere`                        |
| ERNIE-Bot           | `qianfan`            | `QIANFAN_AK`, `QIANFAN_SK` | `qianfan`                       |
| Gemini              | `gemini`             | `GOOGLE_API_KEY`           | `langchain-google-genai`        |
| GPT4All             | `gpt4all`            | N/A                        | `gpt4all`                       |
| Hugging Face Hub    | `huggingface_hub`    | `HUGGINGFACEHUB_API_TOKEN` | `huggingface_hub`, `ipywidgets`, `pillow` |
| NVIDIA              | `nvidia-playground`        | `NVIDIA_API_KEY`           | `langchain_nvidia_ai_endpoints` |
| OpenAI              | `openai`             | `OPENAI_API_KEY`           | `langchain-openai`              |
| OpenAI (playground)       | `openai-playground`        | `OPENAI_API_KEY`           | `langchain-openai`              |
| SageMaker           | `sagemaker-endpoint` | N/A                        | `boto3`                         |

## Supported Data Sources
- [x] Snowflake
- [x] Sqlite
- [x] BigQuery
- [x] Postgres
- [x] MySQL
- [x] File (CSV, Excel, Parquet, etc.)
- [ ] Redshift
- [ ] DynamoDB

## Supported Engines
- [x] Apache Spark
- [x] Apache Flink
- [ ] Presto

## ❓ FAQ

### What is Ryoma?

Ryoma is an **AI-powered Data Agent framework** designed for data analysis, engineering, and visualization. It combines LangChain for AI interactions, Apache Arrow for efficient data operations, and Reflex for web UI development. Ryoma provides SQL agents, data source integrations, and a web-based "Ryoma Lab" interface.

### How is Ryoma different from LangChain or Pandas?

| Feature | Ryoma | LangChain | Pandas |
|---------|-------|-----------|--------|
| **Primary focus** | Data analysis with AI agents | General LLM application framework | Pure data manipulation |
| **SQL Agent** | ✅ Built-in SQL agent with natural language queries | ❌ Requires custom chain | ❌ Manual SQL |
| **Data sources** | ✅ Snowflake, Postgres, MySQL, BigQuery, files | ❌ Custom integration needed | ✅ Limited SQL support |
| **Web UI** | ✅ Ryoma Lab (Reflex-based) | ❌ No built-in UI | ❌ None |
| **Arrow support** | ✅ Apache Arrow for efficient analytics | ❌ No native Arrow | ⚠️ Limited |

**Ryoma = LangChain + Data Sources + SQL Agent + UI**

### What data sources are supported?

| Source | Status |
|--------|--------|
| Snowflake | ✅ Supported |
| SQLite | ✅ Supported |
| BigQuery | ✅ Supported |
| Postgres | ✅ Supported |
| MySQL | ✅ Supported |
| File (CSV, Excel, Parquet) | ✅ Supported |
| Redshift | ❌ Coming soon |
| DynamoDB | ❌ Coming soon |

### What LLM providers are supported?

Ryoma uses Jupyter AI Magics for LLM integration:

| Provider | Provider ID | Environment Variable | Package |
|----------|-------------|---------------------|---------|
| OpenAI | `openai` | `OPENAI_API_KEY` | `langchain-openai` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` | `langchain-anthropic` |
| Gemini | `gemini` | `GOOGLE_API_KEY` | `langchain-google-genai` |
| Cohere | `cohere` | `COHERE_API_KEY` | `cohere` |
| AI21 | `ai21` | `AI21_API_KEY` | `ai21` |
| Bedrock | `bedrock` | N/A | `boto3` |
| Hugging Face | `huggingface_hub` | `HUGGINGFACEHUB_API_TOKEN` | `huggingface_hub` |
| NVIDIA | `nvidia-playground` | `NVIDIA_API_KEY` | `langchain_nvidia_ai_endpoints` |
| GPT4All (local) | `gpt4all` | N/A | `gpt4all` |
| Qianfan (ERNIE) | `qianfan` | `QIANFAN_AK`, `QIANFAN_SK` | `qianfan` |
| SageMaker | `sagemaker-endpoint` | N/A | `boto3` |

### How do I use the SQL Agent?

```python
from ryoma_ai import Ryoma
from ryoma_data import DataSource

# Connect to database
datasource = DataSource(
    "postgres",
    host="localhost",
    port=5432,
    database="mydb",
    user="user",
    password="password"
)

# Create SQL agent
ryoma = Ryoma(datasource=datasource)
agent = ryoma.sql_agent(model="gpt-4", mode="enhanced")

# Ask questions in natural language
agent.stream("Show top 5 customers by purchase amount", display=True)

# Continue tool execution
from ryoma_ai.agent.workflow import ToolMode
agent.stream(tool_mode=ToolMode.ONCE)
```

### What is Ryoma Lab?

Ryoma Lab is a **web-based UI** for interacting with your data and AI agents. Built with Reflex framework, it provides:
- Natural language query interface
- Data visualization
- SQL agent interaction
- Model configuration

**Start Ryoma Lab:**
```shell
# Create rxconfig.py in your project
# Then run:
ryoma_lab run
```
Access at `http://localhost:3000`

### What processing engines are supported?

| Engine | Status |
|--------|--------|
| Apache Spark | ✅ Supported |
| Apache Flink | ✅ Supported |
| Presto | ❌ Coming soon |

### How do I install Ryoma?

**Basic installation:**
```shell
pip install ryoma_ai
```

**With extra dependencies (e.g., Snowflake):**
```shell
pip install ryoma_ai[snowflake]
```

### How do I configure environment variables?

Set LLM provider API keys:
```shell
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Gemini
export GOOGLE_API_KEY="AIza..."
```

### What tech stack does Ryoma use?

- **LangChain** — LLM integration and agent framework
- **Reflex** — Python web UI framework
- **Apache Arrow** — Efficient in-memory data format
- **Jupyter AI Magics** — LLM provider abstraction
- **Amundsen** — Data discovery and metadata
- **Ibis** — Large dataset analytics
- **Feast** — Feature store for ML

### How do I contribute?

1. Read [Contributing Guide](docs/source/contribution/contribution.md)
2. Check [Documentation Index](docs/INDEX.md)
3. Submit Pull Request

For major changes, open an issue first.

### Where can I find documentation?

- **[Documentation Index](docs/INDEX.md)** — Start here
- **[Getting Started](docs/source/getting-started/)** — Setup guides
- **[Architecture](docs/source/architecture/)** — Internal design
- **[Changelog](CHANGELOG.md)** — Version history

### What license does Ryoma use?

**Apache Software License 2.0** — Open-source, permissive license for commercial and personal use.

### Troubleshooting

**"No module named ryoma_ai":**
```shell
pip install ryoma_ai
```

**"Connection refused" for database:**
- Check host/port are correct
- Verify database is running
- Check firewall settings

**"API key not found":**
```shell
# Set the correct environment variable
export OPENAI_API_KEY="your-key"
# Or for Anthropic
export ANTHROPIC_API_KEY="your-key"
```

**Ryoma Lab won't start:**
- Ensure `rxconfig.py` exists in project directory
- Check Reflex is installed: `pip install reflex`
- Verify port 3000 is not blocked

### Help Resources

- **GitHub Issues** — [project-ryoma/ryoma/issues](https://github.com/project-ryoma/ryoma/issues)
- **Documentation** — [project-ryoma.github.io/ryoma](https://project-ryoma.github.io/ryoma)
- **Community** — Check README for Discord/Slack links

---## 📚 Documentation

For comprehensive documentation including architecture, API reference, and guides:

- **[Documentation Index](docs/INDEX.md)** - Start here for all documentation
- **[Getting Started](docs/source/getting-started/)** - Detailed setup and configuration guides
- **[Architecture](docs/source/architecture/)** - Understanding Ryoma AI's internals
- **[Changelog](CHANGELOG.md)** - Release notes and version history

## 🤝 Contributing

We welcome contributions! To get started:

1. **[Read the Contributing Guide](docs/source/contribution/contribution.md)** - Guidelines and best practices
2. **[Check the Documentation Index](docs/INDEX.md)** - Understand the codebase structure
3. **Submit a Pull Request** - We review PRs regularly

For major changes or architectural discussions, please open an issue first to discuss your proposed changes.

## 🛡 License

[![License](https://img.shields.io/github/license/project-ryoma/ryoma)](https://github.com/project-ryoma/ryoma/blob/main/LICENSE)

This project is licensed under the terms of the `Apache Software License 2.0` license. See [LICENSE](https://github.com/ryoma/ryoma/blob/master/LICENSE) for more details.

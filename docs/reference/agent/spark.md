# Spark Agent

Spark agent is an Aita agent specialize in writing spark code.

## Example

{% code title="python" %}
```python
from aita.agent.pyspark import PySparkAgent
from aita.datasource.postgresql import PostgreSqlDataSource 

datasource = PostgreSqlDataSource("postgresql://localhost:5432/db")
spark_configs = {
    "master": "local",
    "appName": "Aita"
}
spark_agent = PySparkAgent(spark_configs, "gpt-3.5-turbo")

spark_agent.stream("I want to get the top customers which making the most purchases")
```
{% endcode %}

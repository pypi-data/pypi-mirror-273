# Utility functions for using common Snowflake actions with Metaflow

This extension introduces a `metaflow.Snowflake` plugin that removes boilerplate for common Snowflake actions in Metaflow tasks and development workstations.

## Installation
```bash
pip install metaflow-snowflake
```

### Use Snowflake in notebooks and Metaflow workflows
```python
from metaflow import Snowflake

with Snowflake(database=DB, schema=SCHEMA, warehouse=WH) as sf:
    df = sf.get('SELECT * FROM TABLE', return_type='pandas')
    ...
    sf.put(transformed_df, 'TRANSFORMED_TABLE')
```

### Examples
- [Getting started](./examples/00-getting-started/)
- [First workflow](./examples/01-hello-flow/)
- [Batch inference](./examples/02-basic-batch-inference/)
- [Snowpark batch inference](./examples/03-snowpark-batch-inference/)
- [Parallel processing](./examples/04-parallel-processing/)
- [dbt](./examples/05-dbt/)
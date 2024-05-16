Combine [duckdb-dbt](https://github.com/duckdb/dbt-duckdb/tree/master) and [Kedro](https://docs.kedro.org/en/stable/) [Datases](https://docs.kedro.org/projects/kedro-datasets/en/kedro-datasets-3.0.0/) to enable:

- extension of dbt to ingest wide array of data, and;
- conversion of Kedro projects to dbt by easily reading your Kedro data catalog configs (yaml files)

## Demo

You can add your existing Kedro definitions to your dbt sources like so:

`pip install dbt_duckdb_kedro_datasets`

```
version: 2

sources:
  - name: my_source # can call this anything
    schema: main
    meta:
      plugin: dbt_duckdb_kedro_datasets # this library
    tables:
      - name: my_table # can call this anything
        description: "A dbt_duckdb_kedro_datasets test"
        meta:
          type: pandas.CSVDataset
          filepath: ./data/1_raw/bikes.csv # file to ingest
          load_args:
            sep: ','
```

Now we can access this CSV in dbt

```
select *
from {{ source('my_source', 'my_table') }}
```

For a more complete example look at [this](example/example_dbt)

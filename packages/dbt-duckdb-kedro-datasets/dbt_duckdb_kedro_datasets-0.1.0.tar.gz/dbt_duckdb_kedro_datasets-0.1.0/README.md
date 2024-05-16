Combine duckdb-dbt and Kedro Dataset to easily read Kedro Dataset configs (yaml), enabling conversion of Kedro projects to dbt.

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

## Todo

-[x] plugin backbone
-[x] initial install
-[x] initial execution
-[x] one config passed from yaml

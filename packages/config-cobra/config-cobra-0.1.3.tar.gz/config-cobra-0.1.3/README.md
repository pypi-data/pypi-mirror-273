# ConfigCobra v0.1.3

This is a basic project to provide a way to deploy database configuration to remote databases via pipelines. The basic premise is that we can control the config via yaml file declarations.  These yaml files provide instructions on what operation should be performed on data and the fields associated with it.

This is the initial version and the feature set is somewhat limited but useful for my purposes.

----

## features

Features in v0.1.3 of ConfigCobra

- postgres data deployments
- Supports standard CRUD operations
- basic local validation of fields supplied against a list of columns
- flexible pk field names

Database connection is controlled by environment variables since the intended use case for this is inside a container

for example:

``` bash
CONFIG_COBRA_DB_NAME=load-test
CONFIG_COBRA_DB_USER=user-name
CONFIG_COBRA_DB_PASSWORD=strong-password
CONFIG_COBRA_DB_HOST=localhost
CONFIG_COBRA_DB_PORT=54321
```

This software is offered without warranty or obligation. 

Contributions to the base that is here is welcome via pull requests. Please ensure any contributions are clearly defined. If they don't match with the goals of the project they will be rejected. If you wish to fork then go for it!

## Usage

Currently takes on arg to a valid yaml file:

```bash
config-cobra --yaml_file %path_to_the_yaml%
```


## YAML format

The yaml file serves as the instructions about what we should do in any particular operation.

The current actions supported in this version are:

- insert
- update
- update_or_insert
- delete

----

### Examples:
#### to insert 

``` yaml
deploy: 
  - table: simple_table
    pk: id
    action: insert
    types:
      id: string
      name: string
      age: int
      json: json
    data:
      - id: 1
        name: John
        age: 30
        json: |
          {
            "key1": "value1",
            "key2": "value2"
          }
      - id: 2
        name: Jane
        age: 25
        json: |
          {
            "key1": "value1",
            "key2": "value2"
          }
```

#### To update

``` yaml

deploy:
  - table: simple_table
    pk: id
    action: update
    types:
      id: string
      name: string
      age: int
      json: json
    data:
      - id: 1
        name: John
        age: 30
        json: |
          {
            "key1": "value1",
            "key2": "value2"
          }
      - id: 2
        name: Jane
        age: 25
        json: |
          {
            "key1": "value1",
            "key2": "value2"
          }

```

#### To update or insert

``` yaml

  - table: simple_table
    pk: id
    action: update_or_insert
    types:
      id: string
      name: string
      age: int
      json: json
    data:
      - id: 7
        name: Bob
        age: 88
        json: |
          {
            "key1": "value1",
            "key2": "value2"
          }

```

#### To delete

``` yaml
deploy: 
  - table: simple_table
    pk: id
    action: delete
    types:
      id: string
      name: string
      age: int
      json: json
    data:
      - id: 1
      - id: 2
      - id: 7
```

# Z Order Indexing Proof of Concept for Meet Near Me Events

## Setup

1. create virtual env
```bash
python3 -m venv venv
```
2. activate the virtual env
```bash
source venv/bin/activate
```

## Seeding Database

1. If there is a need to reseed database after initial startup please delete the .seed_complete file before running 


## Interacting with DynamoDB Local Instance 
1. It is exposed from docker container at http://localhost:8000 and internally from docker compose services
as http://dynamodb-local:8000
2. Dropping table with flag 

```bash
DROP_TABLE=true docker compose up # will drop the Events Table to reset
``` 

### Resources 

#### JQ 

1. Processing line by line json objects with jq
    https://blog.differentpla.net/blog/2019/01/11/jq-reduce/

## Run Project

```shell
docker-compose -f .\docker-compose.yaml up --build
```

## Stop Project

```shell
docker-compose -f .\docker-compose.yaml down
```

## Run Tests

```shell
docker-compose -f .\docker-compose.yaml run --rm backend pytest -vv --cov
```

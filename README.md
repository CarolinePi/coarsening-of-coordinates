# coordinate project
### Fast setting
If you want to launch locally, do next steps:
1. Download docker and docker-compose
2. For the first launch need init db: ```docker-compose up database```
3. Start app: ```docker-compose up```
3. Use swagger http://localhost:8080/api/docs

### Launch Tests
2. For the first launch need init test db: ```docker-compose up database-pytest```
2. Start tests: ```docker-compose up tests```
It must set up db port 5433 with init sql migration for first launch

## Linters
### Mypy
```docker-compose up mypy```


### Flake8
```docker-compose up flake```

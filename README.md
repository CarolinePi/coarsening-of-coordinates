# coordinate project
### Fast setting
If you want to launch locally, do next steps:
1. Download docker and docker-compose
2. Start app: ```docker-compose up```
It must set up db port 5432 with init sql migration for first launch
3. Use swagger http://localhost:8080/api/docs

### Launch Tests
1. Start tests: ```docker-compose up tests```
It must set up db port 5433 with init sql migration for first launch


### Mypy
```docker-compose up mypy```


### Flake8
```docker-compose up flake```
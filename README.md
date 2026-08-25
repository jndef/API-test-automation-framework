# API Test Automation Framework

Test automation framework for REST API testing built on top of 
QA Automation Sandbox (https://github.com/manikosto/qa-automation-sandbox)
Refactoring is currently in progress. See here 
https://github.com/jndef/API-test-automation-framework/tree/refactor/architecture-and-services

## Stack
- Python 3.12
- pytest
- Allure
- Requests
- Docker / docker-compose
- Pydantic

## Architecture
- `auth/` — authentication, token management, role factory
- `services/` — API service layer (endpoints, payloads, models)
- `common/` — common request params (models)
- `tests/` — test suites
- `fixtures/` — pytest fixtures
- `utilits/` — data api helper, db helper, allure helper + validation helper
- `config/` — base test db configuration,headers configuration, stages configuration
- pytest.ini - pytest run configuration

## Environments
Local: http://localhost:8000
Staging: configure STAGE in .env. default - local

## How to run

### Local
Check specified pytest options at pytest.ini
```bash
clone repository
pip install -r requirements.txt
pytest

```

### Docker
```bash
docker-compose up --build
```

## Features
- Multi-role service factory with token caching
- Pydantic response validation
- Allure reporting
- Parametrized test data

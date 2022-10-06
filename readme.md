# fastSchedule
cron 명령어 기반으로 schedule을 실행합니다.

## Features

- cron 명령 기반, schedule 실행
- 현재 등록된 schedule 확인
- 실행된 schedule 이력 조회

## DB 설정
```yml
# apis/configs/config_dev.yml 및 config_prod.yml에 설정합니다

databases:
  inner:
    host: "somthing.db.host.com"
    port: 3306
    database: "database_name"
    username: "username"
    password: "password"
    timezone: "+09:00"
```

## Installation

```sh
cd apis
poetry install
python -m uvicorn main:app
```

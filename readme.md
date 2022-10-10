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
cd ../
python -m uvicorn main:app
```

## 구조
Scheduler는 생성자에서 아래와 같은 동작을 합니다.
- Apscheduler 프로세스를 띄웁니다. 
- Apscheduler에 run_default_task 스케쥴을1분 간격으로 실행하도록 스케쥴링에 추가합니다.
- Apscheduler에 run_long_running_task 스케쥴을 10분 간격으로 실행하도록 스케쥴링에 추가합니다.
- DB에 등록된 schedule을  조회 후, cron 조건에 맞는 것은 실행하는 스케쥴을 일정한 주기(1분, 10분)로 실행합니다.
 ![structure_imgae1](https://s3.us-west-2.amazonaws.com/secure.notion-static.com/74db6ba6-6016-4da2-8619-925ce58d580b/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA_2022-10-10_%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE_10.37.45.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20221010%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20221010T133948Z&X-Amz-Expires=86400&X-Amz-Signature=c4332565a697454a5f98fa149b0b256fe8d5b2d9fd3b741d9a7d59034550d53c&X-Amz-SignedHeaders=host&response-content-disposition=filename%20%3D%22%25E1%2584%2589%25E1%2585%25B3%25E1%2584%258F%25E1%2585%25B3%25E1%2584%2585%25E1%2585%25B5%25E1%2586%25AB%25E1%2584%2589%25E1%2585%25A3%25E1%2586%25BA%25202022-10-10%2520%25E1%2584%258B%25E1%2585%25A9%25E1%2584%2592%25E1%2585%25AE%252010.37.45.png%22&x-id=GetObject)

## Project info
- python version: 3.12
- framework: fastapi
- database: mysql, mongodb, redis

## Features
- Short Link 생성 API
![img.png](img.png)
- Short Link 조회 API
![img_1.png](img_1.png)
- Short Link Origin url redirect API
![img_2.png](img_2.png)
- Short Link 7일 조회 API
![img_3.png](img_3.png)
- 테스트 코드
![img_4.png](img_4.png)

## Hot to Run
```shell
# 가상환경 구축 및 활성 
virtualenv venv --python=python3.12
source venv/bin/activate
pip install -r requirements.txt

# database 실행
docker-compose -f ./app/db/docker-compose.yaml up -d

# 1~2분 대기
# mysql migration
alembic upgrade head

# 테스트 코드 실행
bash test.bash

# 서버 실행
uvicorn app.main:app --host localhost --port 8080
```

## API
- swagger url: http://localhost:8080/swagger#
- redoc url: http://localhost:8080/redoc

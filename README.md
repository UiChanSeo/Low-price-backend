# 프로그래 정보

```
이름  : Low-Price Backend
개발자 : seouichan@naver.com, hoopa2@naver.com, alex021009@naver.com
```

# 설명
```
- 이 앱은 Low-Price-App의 백엔드로 동작하는 프로그램입니다.
- Low-Price-App 사용자의 정보를 서버에 저장을 하거나, 서버에 저장된 정보를 앱으로 가져갈 떄 백엔드에서 역할으 합니다.
- 사용자 정보를 관리합니다.
```

# 실행
```
RUN="dev" PYTHONPATH=${PWD} gunicorn app.run_api:app -b 0.0.0.0:8080 -w 3
```

# History
- v0.1.1 : 2022/06, 앱과 연동이 되도록 기본적인 동작을 구현
- v0.1.2 : 2022/08, 대상 db는 sqlite로 함. ( 차후 mysql 고려 )
- ...

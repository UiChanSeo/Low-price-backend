# LowPriceFind Backend

## Operating with LowPriceFind Project
## Included Modules
* api server

# RUN
## api server
* RUN="dev" PYTHONPATH=${PWD} gunicorn app.run_api:app -b 0.0.0.0:8080 -w 3

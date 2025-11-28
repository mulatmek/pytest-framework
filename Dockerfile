# create docker file for a python application version 3.12
FROM python:3.12-slim
WORKDIR /app
COPY . /app
#install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV BASE_URL="http://default-hardcoded-url.com"

CMD python -m pytest -sv --json-report --endpoints=${BASE_URL} tests/unitest

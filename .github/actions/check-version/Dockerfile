FROM python:3.8-slim

RUN apt-get update && apt-get install -y git && apt-get clean
RUN pip install click packaging dunamai actions-toolkit
COPY docker-entrypoint.py /usr/local/bin/docker-entrypoint.py

ENTRYPOINT ["python", "/usr/local/bin/docker-entrypoint.py"]

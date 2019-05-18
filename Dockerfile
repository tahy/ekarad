FROM python
LABEL version="0.1"

COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY ./src /opt/src
ENTRYPOINT ["python3", "/opt/src/app.py"]
FROM python:3.5.4-alpine3.4
ENV FLASK_APP /usr/local/pathfinder/api.py
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY pathfinder /usr/local/pathfinder/
CMD flask run --host 0.0.0.0

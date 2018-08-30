FROM python:3.7-alpine

RUN adduser -D analysis

WORKDIR /home/analysis

COPY requirements.txt requirements.txt
RUN apk add build-base
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn
RUN venv/bin/pip install -U spacy
RUN venv/bin/python -m spacy download en
RUN venv/bin/python -m nltk.downloader -d /usr/local/share/nltk_data wordnet

COPY core core
COPY endpoints endpoints
COPY app.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R analysis:analysis ./
USER analysis

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
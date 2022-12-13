FROM python:3.9-slim-buster

ADD atlas /root/atlas
WORKDIR /root/atlas
RUN pip install -r requirements.txt
WORKDIR /root/atlas/atlas

CMD ["python3", "main.py"]
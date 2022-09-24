FROM python:3.10.6-slim-bullseye

WORKDIR /finapp

COPY . .

RUN pip3 install -r ./src/requirements.txt
RUN python3 -m pip install -e .

CMD python3 ./src/update.py
FROM python:3.9-slim

WORKDIR /code

COPY req.txt /code/req.txt

RUN pip install --no-cache-dir --upgrade -r /code/req.txt

COPY . /code

ENTRYPOINT [ "streamlit", "run" ]
CMD [ "client.py" ]
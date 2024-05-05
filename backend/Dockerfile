FROM python:3.9

WORKDIR /code

COPY req.txt /code/req.txt

RUN pip install --no-cache-dir --upgrade -r /code/req.txt

COPY . /code

EXPOSE 3000

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
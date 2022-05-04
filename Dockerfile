# (1)
FROM python:3.8

# (2)
WORKDIR /code

# (3)
COPY ./requirements.txt /code/requirements.txt

ADD . /code

# (4)
RUN python3.8 -m pip install --upgrade pip setuptools
#RUN python3.8 -m pip install numpy
RUN python3.8 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com

# (5)
#COPY ./ACenterWeb /code/ACenterWeb

# (6)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2022"]

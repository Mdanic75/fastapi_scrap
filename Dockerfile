FROM python:3.10

WORKDIR /code

COPY . /code

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN python -m pip install pipenv
RUN pipenv install --deploy --system --ignore-pipfile
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
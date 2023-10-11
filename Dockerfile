FROM python:latest

WORKDIR /expenseTracker

COPY requirements.txt /expenseTracker

RUN pip install -r requirements.txt

COPY . /expenseTracker

EXPOSE 8000

CMD python /expenseTracker/manage.py runserver 0.0.0.0:8000

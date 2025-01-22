FROM python:3.12
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/skrbacz/django-project-se.git
WORKDIR /django-project-se
RUN pip install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 9999
CMD ["python", "djangoProject/manage.py", "runserver", "0.0.0.0:9999"]

FROM python:3.13.11-trixie

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN pip install --upgrade pip wheel

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . ./

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "manul_routine.wsgi:application"]
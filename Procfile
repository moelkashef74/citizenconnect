web: gunicorn api.wsgi --log-file -
worker: celery -A api worker --loglevel=info
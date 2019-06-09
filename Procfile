web: python project_cenpilos/manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT project_cenpilos/settings.py

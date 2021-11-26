release: flask db upgrade
web: gunicorn url_shortener.app:create_app\(\) -b 0.0.0.0:$PORT -w 3

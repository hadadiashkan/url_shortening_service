FLASK_ENV=development
FLASK_APP=url_shortening.app:create_app
SECRET_KEY=changeme
DATABASE_URI=sqlite:///url_shortening.db
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=rpc://

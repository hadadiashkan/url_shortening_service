from url_shortening.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("url_shortening.tasks.example",)

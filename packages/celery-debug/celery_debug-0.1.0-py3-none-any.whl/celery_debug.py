from celery import shared_task
from celery.app import app_or_default


@shared_task(name="debug.ping")
def ping():
    return "pong"


@shared_task(name="debug.echo")
def echo(msg):
    return msg


app = app_or_default()
if app.conf.task_routes is None:
    app.conf.task_routes = {}

if not "debug.*" in app.conf.task_routes:
    app.conf.task_routes.update(
        {
            "debug.*": {"queue": "debug"},
        }
    )

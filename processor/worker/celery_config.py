import os
from celery import Celery
from dotenv import load_dotenv

# Both broker and result backend must use database 0
broker_url = 'redis://default:9TX3gyyakwM6sHd5LEMAl0GYswvWmW1s@redis-16662.c339.eu-west-3-1.ec2.redns.redis-cloud.com:16662'
result_backend = 'redis://default:9TX3gyyakwM6sHd5LEMAl0GYswvWmW1s@redis-16662.c339.eu-west-3-1.ec2.redns.redis-cloud.com:16662'

celery_app = Celery(
    "document_converter",
    broker=broker_url,
    backend=result_backend,
    include=["processor.worker.tasks"],
)

# Add explicit Redis backend settings
celery_app.conf.update(
    redis_max_connections=20,
    broker_transport_options={'visibility_timeout': 3600},
    result_backend_transport_options={'visibility_timeout': 3600}
)

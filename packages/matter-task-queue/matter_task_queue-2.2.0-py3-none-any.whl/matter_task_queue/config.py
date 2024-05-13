import os


class Config:
    def __init__(self):
        self.load_variables()

    @classmethod
    def load_variables(cls):
        cls.ENV = os.getenv("ENV", "local")
        cls.IS_ENV_LOCAL_OR_TEST = cls.ENV.lower() in ["local", "test"]
        cls.DEBUG = os.getenv("DEBUG", "false").lower() == "true"

        cls.INSTANCE_NAME = os.environ["INSTANCE_NAME"]
        cls.AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
        cls.CELERY_LOG_LEVEL = os.environ.get("CELERY_LOG_LEVEL", "INFO").upper()
        cls.CELERY_LOG_FILE_PATH = os.getenv("CELERY_LOG_FILE_PATH", "/tmp/celery.txt")
        cls.CELERY_DEAD_LETTER_QUEUE = os.getenv("CELERY_DEAD_LETTER_QUEUE", "dead_letter_queue")
        cls.SENTRY_DSN = os.getenv("SENTRY_DSN")
        cls.AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")
        cls.CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"] if cls.ENV != "test" else os.getenv("CELERY_BROKER_URL")
        cls.CELERY_RESULT_BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND_URL")


Config()

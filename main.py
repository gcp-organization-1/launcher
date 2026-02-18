from google.cloud import pubsub_v1
from bigquerychecker.check import Launcher
import json
from config.settings import settings
from config.logger import logger


def main(request):
    topic_id = settings.TOPIC_ID
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(settings.PROJECT_ID, topic_id)

    launcher = Launcher()
    missing_dates = launcher.get_missing_dates_from_bigquery()

    logger.info("Missing dates", missing_dates)

    futures = []

    for date in missing_dates:
        message = {
            "start_date": date,
            "end_date": date
        }

        logger.info("Publishing:", message)

        message_bytes = json.dumps(message).encode("utf-8")
        future = publisher.publish(topic_path, message_bytes)
        futures.append(future)

    for future in futures:
        logger.info(future.result())

    return {"success"}, 200

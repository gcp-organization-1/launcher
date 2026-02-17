
from google.cloud import bigquery
from config.settings import settings
from config.helper import get_current_week_dates

class Launcher:
    def __init__(self):
        self.client = bigquery.Client()


    def get_missing_dates_from_bigquery(self):
        sql = f"""
            SELECT DISTINCT date
            FROM `{settings.PROJECT_ID}.asteroids.asteroids-table`
            WHERE DATE(date) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
        """

        query_job = self.client.query(sql)
        results = query_job.result()

        bq_dates = {
            row.date
            for row in results
        }

        expected_dates = set(get_current_week_dates())

        missing_dates = sorted(expected_dates - bq_dates)
        print(missing_dates)
        return missing_dates


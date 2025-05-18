import importlib
from celery_app import celery
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

@celery.task(name="tasks.run_scraper_task", bind=True)
def run_scraper_task(self, scraper_name, data):
    # try:
    module = importlib.import_module(f"modules.{scraper_name}.scraper")
    scraper_class = getattr(module, scraper_name)
    scraper = scraper_class(**data)
    total_items, items = scraper.scrape()
    return {"total_items": total_items, "items": items}
    # except Exception as e:
    #     raise self.retry(exc=e, countdown=10, max_retries=3)

import time
import random
import requests
from datetime import datetime
from mpscanner.extensions import mongo
from lib.potato.onpage import PageParse
from lib.potato.extract import websiteDomain, webpageData
from mpscanner.app import create_celery_app

celery = create_celery_app()


@celery.task(bind=True)
def crawl(self, url):
    webData = mongo.db.scan
    homepage = websiteDomain(url)
    r = requests.get(url, timeout=5)
    siteData = webpageData(r.text, url, 'prospect', url)
    webData.insert_one(
        {
            'crawl_data': siteData,
            'crawl_time': datetime.now(),
            'homepage': homepage
        })

    # Restrict crawling to only internal links on same domain
    page = PageParse(r.text, url)
    links = page.hrefs()
    domain_links = [x for x in links if websiteDomain(x) ==
                    websiteDomain(url)]
    nextlinks = random.sample(domain_links, 2)

    for link in nextlinks:
        time.sleep(random.randint(2, 5))
        if webData.find({'homepage': homepage}).count() < 10:
            time.sleep(random.randint(2, 5))
            crawl(link)
    return None

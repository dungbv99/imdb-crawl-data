from scrapy.crawler import CrawlerProcess
from imdb.spiders.ImdbSpiders import ImdbSpiders
import pandas as pd
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ImdbSpiders)
    process.start()
    # imdbId = pd.read_csv('imdb/spiders/links.csv')['imdbId']
    # for id in imdbId:
    #     a = "uuuu"+str(id)
    #     print(a)

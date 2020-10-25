import scrapy
from scrapy.loader import ItemLoader
from imdb.items import ImdbItem
import pandas as pd

class ImdbSpiders(scrapy.Spider):
    name = "imdb"


    def start_requests(self):
        imdbUrl = "https://www.imdb.com/title/tt"
        imdbId = pd.read_csv('./imdb/spiders/links.csv', dtype=str)['imdbId']
        for id in imdbId:
            url = imdbUrl+id
            yield scrapy.Request(url=url, callback=self.parse)

    storyLineXPath = "//div[@id='titleStoryLine']/div[@class='inline canwrap']/p/span/text()"
    castXpathOdd = "//div[@id='titleCast']/table[@class='cast_list']/tr[@class='odd']/td/a/text()"
    castXpathEven = "//div[@id='titleCast']/table[@class='cast_list']/tr[@class='even']/td/a/text()"
    averageRatingXPath = "//div[@class='mini-article']/div[@id='ratingWidget']/span/span/text()"
    directorXPath = "//*[@id='title-overview-widget']/div[2]/div[1]/div[2]/a/text()"
    writerXPath = "//*[@id='title-overview-widget']/div[2]/div[1]/div[3]/a/text()"
    starsXPath = "//*[@id='title-overview-widget']/div[2]/div[1]/div[4]/a/text()"
    countryXPath = "//div[@id='titleDetails']/div[2]/a/text()"
    languageXPath = "//div[@id='titleDetails']/div[2]/a/text()"

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'HTTPCACHE_ENABLED': True,
        'CONCURRENT_REQUESTS': 4,
        'DOWNLOAD_DELAY': 4,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_deltafetch.DeltaFetch': 100,
            'imdb.middlewares.ImdbSpiderMiddleware': 543,
        },
        'DELTAFETCH_ENABLED': True,
        'DELTAFETCH_DIR': '/home/dung/PycharmProjects/imdb/delta_fetch',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
        },
        'ITEM_PIPELINES': {
            'imdb.pipelines.ImdbPipeline': 300,
        }
    }

    def parse(self, response):
        imdbLoader = ItemLoader(item=ImdbItem(), response=response)

        storyLine = response.xpath(self.storyLineXPath).get()
        imdbLoader.add_value('storyLine', storyLine)

        odd = response.xpath(self.castXpathOdd).getall()
        even = response.xpath(self.castXpathEven).getall()
        cast = []
        for i in range(int(len(odd) / 2)):
            cast.append(odd[i * 2].replace('\n', ''))
        for i in range(int(len(even) / 2)):
            cast.append(even[i * 2].replace('\n', ''))
        imdbLoader.add_value('cast', cast)

        averageRating = response.xpath(self.averageRatingXPath).get()
        imdbLoader.add_value('averageRating', averageRating)

        budget = ' '.join(response.css(".txt-block:contains('Budget')::text").extract()).strip()
        imdbLoader.add_value('budget', budget)

        cumulative = ' '.join(response.css(".txt-block:contains('Cumulative Worldwide')::text").extract()).strip()
        imdbLoader.add_value('cumulative', cumulative)

        director = response.xpath(self.directorXPath).getall()
        imdbLoader.add_value('director', director)

        writer = response.xpath(self.writerXPath).getall()
        if(len(writer) > 1):
            writer.pop()
        imdbLoader.add_value('writer', writer)

        stars = response.xpath(self.starsXPath).getall()
        if(len(stars) > 1):
            stars.pop()
        imdbLoader.add_value('stars', stars)

        country = response.xpath(self.countryXPath).getall()
        imdbLoader.add_value('country', country)

        print("storyLine ", storyLine)
        print('cast', cast)
        print("averageRating ", averageRating)
        print("budget: ", budget)
        print("cumulative: ", cumulative)
        print('director ', director)
        print('writer ', writer)
        print("stars ", stars)
        print('country ', country)

        yield imdbLoader.load_item()
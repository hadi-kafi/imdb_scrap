from turtle import title
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,asc']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield {
            'title' : response.xpath("//div[@class='sc-80d4314-1 fbQftq']/h1/text()").get(),
            'year' : response.xpath("(//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh'])[1]/text()").get(),
            'duration' : response.xpath("normalize-space(//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt']/li[3]/text())").get(),
            'genre' : response.xpath("//div[@class='sc-16ede01-8 hXeKyz sc-2a827f80-11 kSXeJ']/div/div[2]/a/span/text()").getall(),
            'rating' : response.xpath("//div[@class='sc-7ab21ed2-2 kYEdvH']/span[1]/text()").get(),
            'movie_url' : response.url,
        }

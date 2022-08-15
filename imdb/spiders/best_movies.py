from turtle import title
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestMoviesSpider(CrawlSpider):
    name = 'best_movies'
    allowed_domains = ['imdb.com']
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,asc']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,asc', headers= {
            'User-Agent' : self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//h3[@class='lister-item-header']/a")), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=("(//a[@class='lister-page-next next-page'])[2]")), process_request='set_user_agent')
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title' : response.xpath("//div[@class='sc-80d4314-1 fbQftq']/h1/text()").get(),
            'year' : response.xpath("(//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh'])[1]/text()").get(),
            'duration' : response.xpath("normalize-space(//ul[@class='ipc-inline-list ipc-inline-list--show-dividers sc-8c396aa2-0 kqWovI baseAlt']/li[3]/text())").get(),
            'genre' : response.xpath("//div[@class='sc-16ede01-8 hXeKyz sc-2a827f80-11 kSXeJ']/div/div[2]/a/span/text()").getall(),
            'rating' : response.xpath("//div[@class='sc-7ab21ed2-2 kYEdvH']/span[1]/text()").get(),
            'movie_url' : response.url,
            'user-agent' : response.request.headers['User-Agent']
        }

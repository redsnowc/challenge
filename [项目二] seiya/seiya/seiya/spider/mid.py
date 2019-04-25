from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class SeiyaMidlleware(UserAgentMiddleware):
    ua = UserAgent()
    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)

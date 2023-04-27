import datetime
import scrapy
from selenium import webdriver
from scrapy.http import Request
from sina import settings
from sina.items import SinaItem

class SinaSpiderSpider(scrapy.Spider):
    name = "sina_spider"
    
    def __init__(self):
        self.start_urls = ["https://news.sina.com.cn/china/"]
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("no=sandbox")
        self.option.add_argument("--headless")
        self.option.add_argument("--blink-settings=imagesEnabled=false")

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse_time(self, news_time):
        today = datetime.datetime.now()
        # 替换今天字符串
        news_time = news_time.replace("今天", str(today.month) + "月" + str(today.day) + "日 ")

        # 替换分钟前关键字
        if "分钟前" in news_time:
            mintue = news_time.split("分钟前")[0]
            now = today - datetime.timedelta(minutes=int(mintue))
            news_time = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)
            news_time = news_time.strftime("%Y年%m月%d日 %H:%M")

        # 添加年份
        if "年" not in news_time:
            news_time = str(today.year) + "年" + news_time
        return news_time

    def parse(self, response):
        driver = webdriver.Chrome(chrome_options=self.option)
        driver.set_page_load_timeout(30)
        driver.get(response.url)
        for i in range(2):
            while not driver.find_element_by_xpath("//div[@class='feed-card-page']").text:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            title = driver.find_elements_by_xpath("//div[@class='feed-card-item']/h2/a")
            time = driver.find_elements_by_xpath("//div[@class='feed-card-time']")

            for i in range(len(title)):
                items = SinaItem()
                items["news_number"] = "No." + str(i + 1) if i + 1 > 9 else "No." + "0" + str(i + 1)
                items["news_type"] = settings.BOT_TYPE
                items["news_title"] = title[i].text
                href = title[i].get_attribute("href")
                items["news_time"] = self.parse_time(time[i].text)
                yield Request(url=response.urljoin(href), meta={"name": items}, callback=self.parse_namedetail)
            # 翻页
            try:
                driver.find_element_by_xpath("//div[@class='feed-card-page']/span[@class='pagebox_next']/a").click()
            except:
                break

    def parse_namedetail(self, response):
        selector = scrapy.Selector(response)
        desc = selector.xpath("//div[@class='article']/p/text()").extract()
        desc = list(map(str.strip, desc))
        items = response.meta["name"]
        items["news_desc"] = "".join(desc)
        yield items
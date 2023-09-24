# -*- coding: utf-8 -*-
import scrapy
import re


class CovidSpider(scrapy.Spider):
    name = 'covid'
    allowed_domains = ['web.archive.org']
    start_urls = ['https://web.archive.org/web/20210907023426/https://ncov.moh.gov.vn/vi/web/guest/dong-thoi-gian/']

    def parse(self, response):
        for case in response.xpath("//div[@class='timeline-sec']/ul"):
            match = re.search('[0-9.]+', case.xpath(".//li/div/div[2]/div[2]/p/text()").get())
            if match:
                yield{
                    'time': case.xpath(".//li/div/div[2]/div[1]/h3/text()").get(),
                    'new_case': float(match.group())   
                }
        next_page = response.xpath("//ul[@class='lfr-pagination-buttons pager']/li[2]/a/@href").get()
        if next_page is not None:
            yield scrapy.Request(url=next_page, callback=self.parse)

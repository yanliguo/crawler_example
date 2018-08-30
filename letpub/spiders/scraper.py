import scrapy
import urllib

letpub_host = "*****" 
query_params = {
        'page': 'grant',
        'name': '',
        'person': '',
        'no': '',
        'company': '',
        'startTime': '2018',
        'endTime': '2018',
        'money1': '',
        'money2': '',
        'subcategory': '青年科学基金项目',
        'addcomment_s1': '0',
        'addcomment_s2': '0',
        'addcomment_s3': '0',
        'currentpage': '1',
        }

query_url = letpub_host + '?' + urllib.parse.urlencode(query_params)


class Letpub(scrapy.Spider):
    name = "letpub_spider"
    start_urls = [ query_url ]

    def extract_project(self, selector_tuple):
        if selector_tuple is None or len(selector_tuple) < 3:
            return None
        person_in_charge, institute, money, proj_id, proj_type, department, approve_year = \
                selector_tuple[0].css('td::text').extract()
        titles = selector_tuple[1].css('td::text').extract()
        title = ""
        if len(titles) > 0 and titles[0] == '题目':
            title = titles[-1]
        subject_classes = {}
        _, classes = selector_tuple[2].css('td::text').extract()
        # , in Chinese
        classes = classes.split('，')
        clses = []
        for i in range(len(classes)):
            # : in Chinese
            clses.append(classes[i].split('：')[-1])
        return {
                'person_in_charge': person_in_charge,
                'institute': institute,
                'money': float(money),
                'project_id': proj_id,
                'project_type': proj_type,
                'department': department,
                'approve_year': approve_year,
                'title': title,
                'subject_classes': clses,
                }


    def parse(self, response):
        # remove paginations, header
        trs = response.css('.table_yjfx tr')[2:-1]
        #trs = [2:-1] 
        zipped_trs = list(zip(*[trs[i::3] for i in range(3)]))
        for z in zipped_trs:
            if len(z) == 3:
                project_object = self.extract_project(z)
                if project_object is not None:
                    yield project_object

        for href in response.css('.table_yjfx tr a'):
            text = href.css('::text').extract_first()
            if text is not None and text == '下一页':
                next_page = href.css('::attr(href)').extract_first()
                if next_page is not None:
                    yield scrapy.Request(next_page, callback=self.parse)



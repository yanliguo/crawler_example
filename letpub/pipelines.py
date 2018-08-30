# -*- coding: utf-8 -*-
import json, codecs
import sys

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LetpubPipeline(object):
    """
    1. change unicode to chinese
    2. if run by 'scrapy crawl letpub_spider --out result.json', 
       this pipeline opens result.json and write item line by line
    """

    def __init__(self):
        filename = 'result.json'
        """
        try:
            out_idx = sys.argv.index('--out')
            if out_idx < len(sys.argv) - 1:
                filename = sys.argv[out_idx + 1]
        except:
            pass
        """
        if filename is not None:
            self.file = codecs.open(filename, 'w', encoding='utf-8')
        else:
            self.file = None

    def process_item(self, item, spider):
        if self.file is not None:
            line = json.dumps(item, ensure_ascii=False) + "\n"
            self.file.write(line)
        return item

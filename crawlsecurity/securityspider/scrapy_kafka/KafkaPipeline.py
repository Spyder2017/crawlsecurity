# -*- coding: utf-8 -*-
from scrapy.utils.serialize import  ScrapyJSONEncoder
#from kafka.client import KafkaClient
#from kafka.producer import SimpleProducer
from pykafka import KafkaClient

class KafkaPipeline(object):
    #初始化配置 Kafka Topic
    def __init__(self,producer):
        self.producer = producer
        #self.topic = topic
        self.encoder = ScrapyJSONEncoder()

    #处理和编码每条数据记录,并发送给Kafka
    def process_item(self,item,spider):
        item = dict(item)
        item['spider'] = spider.name
        msg = self.encoder.encode(item)
        self.producer.produce(msg)
	return item

    #初始化配置 并创建客户端和调用写入Kafka函数逻辑
    @classmethod
    def from_settings(cls,settings):
        # k_hosts = settings.get('KAFKA_HOSTS',['112.74.216.232:9092'])
        # topic = settings.get('KAFKA_ITEM_PIPELINE_TOPIC',['scrapy_kafka_item'])
        #topic = settings.get('KAFKA_ITEM_PIPELINE_TOPIC')
        #kafka = KafkaClient(hosts="112.74.216.232:9092")
        client = KafkaClient(hosts='112.74.216.232:9092')
        topic = client.topics['scrapy']
        #conn = SimpleProducer(kafka)
        producer = topic.get_producer()
        return cls(producer)

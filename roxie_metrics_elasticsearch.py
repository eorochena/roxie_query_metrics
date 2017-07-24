#!/usr/bin/python

from elasticsearch import Elasticsearch
from datetime import date
from datetime import datetime

import xml.etree.ElementTree as et
import os
import sys
import time

es = Elasticsearch('192.168.1.120', port = 9200)
cmd = '2>/dev/null testsocket . "<control:metrics/>"'
epoch_cmd = 'date +%s'
counter = 0
while True:
    get_metrics = os.popen(cmd).read()
    epoch = os.popen(epoch_cmd).read()
    timestamp = datetime.utcnow()
    index_name = 'roxie_index-%s' % date.today()
    if get_metrics:
        metrics ={}
        payload = {}
        parse_xml = et.fromstring(get_metrics)
        doc_root = parse_xml
        for ip in doc_root:
            ip_address = ip.attrib['ep'].replace(':9876', '')
        payload['roxie_address'] = ip_address
        for metric in doc_root.iter('Metric'):
            metrics[metric.attrib['name']] = metric.attrib['value']
            payload['roxie_metrics'] = metrics
            payload['timestamp'] = timestamp
            res = es.index(index=index_name.strip(), doc_type='roxie_metrics', id=epoch, body=payload)
        counter += 1
        print(counter, payload)
        time.sleep(1)
    else:
        counter += 1
        print(counter, ' sleeping')
        time.sleep(3)
        continue


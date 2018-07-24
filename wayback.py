#!/usr/bin/env python

import requests
import sys

domain = sys.argv[1]
res = requests.get("https://web.archive.org/cdx/search/cdx?url=%s/*&fl=original" % (domain))

urls = set()
for line in res.text.split('\n'):
    urls.add(line.replace(':80', ''))

for url in urls:
    print url

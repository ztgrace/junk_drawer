#!/usr/bin/env python

import argparse
import datetime
from flask import Flask, jsonify
from ipwhois import IPWhois, IPDefinedError
import json
import time

app = Flask(__name__, static_url_path='/static')
app.debug = True
cache = dict()
cache_timeout = 60  # minutes


@app.route('/ipwhois/<ip>', methods=['GET'])
def ipwhois(ip):
    res = query(ip)
    return mkresponse(res)


def mkresponse(res):
    if res.get('error', None):
        return jsonify(res)

    asn = {
        'asn': res['asn'],
        'asn_description':  res['asn_description'],
        'asn_cidr': res['asn_cidr'],
        'nets': res['nets']}
    encoded = json.dumps(asn)
    return encoded


def query(ip):
    global cache
    res = cache.get(ip, None)
    if res is None or getTimeDelta(res['retrieved']) > cache_timeout:
        try:
            res = IPWhois(ip).lookup_whois()
        except (ValueError, IPDefinedError) as e:
            return {'error': str(e)}
        res['retrieved'] = time.mktime(datetime.datetime.now().timetuple())
        cache[ip] = res
    else:
        print("Using cached value")
    return res


def getTimeDelta(ts):
        retreived = datetime.datetime.fromtimestamp(float(ts))
        diff = datetime.datetime.now() - retreived

        minutes = int(diff.total_seconds()/60)
        return minutes


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-c', '--cache-timeout', type=int, required=False, help='ipwhois cache time in minutes. Default is 60 minutes.', default=60)
    args = ap.parse_args()

    cache_timeout = args.cache_timeout

    app.run(host='0.0.0.0', port=42424)

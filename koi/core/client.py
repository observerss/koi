#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hmac
import base64
import urllib
import random
import hashlib
from datetime import datetime

import requests

from koi import __aliyun_version__


def quote(s):
    r = urllib.parse.quote(str(s))
    return r.replace('+', '%20').replace('*', '%2A').replace('%7E', '~')


class Client(object):
    """ Aliyun Common Client """

    def __init__(self, access_key_id=None, access_key_secret=None):
        self.access_key_id = access_key_id or os.getenv('ALIYUN_ACCESS_KEY_ID')
        self.access_key_secret = access_key_secret or \
            os.getenv('ALIYUN_ACCESS_KEY_SECRET')
        self.api_url = 'https://ecs.aliyuncs.com/'
        self.nonce = None
        self.session = requests.Session()

    def reset_nonce(self):
        self.nonce = str(random.randint(1e14, 1e15-1))

    def request(self, action, data={}):
        self.reset_nonce()
        params = {
            'Action': action,
            'Format': 'json',
            'Version': __aliyun_version__,
            'AccessKeyId': self.access_key_id,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureVersion': '1.0',
            'SignatureNonce': self.nonce,
            'Timestamp': datetime.utcnow().isoformat(),
        }
        params.update(data)
        to_sign = 'GET&%2F&' + quote('&'.join(['='.join([quote(r[0]), quote(r[1])])
                                     for r in sorted(params.items())]))
        sign = base64.b64encode(hmac.new((self.access_key_secret + '&').encode('utf-8'),
                                         to_sign.encode('utf-8'),
                                         hashlib.sha1).digest()).strip()
        params['Signature'] = sign
        r = self.session.get(self.api_url, params=params)
        if r.status_code == 200:
            return r.json()
        else:
            raise ValueError('request {}/{} returns {}'.format(action, data, r.text))

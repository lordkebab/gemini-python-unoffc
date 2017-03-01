from __future__ import print_function

import requests
import base64
import hashlib
import hmac
import json
import time

class Client(object):
    """ Client for the Gemini Exchange REST API.

    Full API docs are here: https://docs.gemini.com
    """

    API_KEY = ''
    API_SECRET = ''
    API_VERSION = '/v1'
    BASE_URI = "https://api.sandbox.gemini.com" + API_VERSION

    def _get_nonce(self):
        return time.time()*1000

    def _invoke_api(self, endpoint, payload):
        # base64 encode the payload
        payload = str.encode(json.dumps(payload))
        b64 = base64.b64encode(payload)

        # sign the requests
        signature = hmac.new(str.encode(self.API_SECRET), b64, hashlib.sha384).hexdigest()

        headers = {
            'Content-Type': 'text/plain',
            'X-GEMINI-APIKEY': self.API_KEY,
            'X-GEMINI-PAYLOAD': b64,
            'X-GEMINI-SIGNATURE': signature
        }

        url = self.BASE_URI + endpoint

        r = requests.post(url, headers=headers)

        return r

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


    def __init__(self, api_key, api_secret):
        self.API_KEY = api_key
        self.API_SECRET = api_secret

    # Private API methods
    # -------------------
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

    # Order Status API
    # https://docs.gemini.com/rest-api/#order-status
    # ----------------------------------------------
    def get_active_orders(self):
        """ https://docs.gemini.com/rest-api/#get-active-orders """
        endpoint = '/orders'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload).json()

    def get_order_status(self, order_id):
        """ https://docs.gemini.com/rest-api/#order-status """
        endpoint = '/order/status'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'order_id': order_id
        }

        return self._invoke_api(endpoint, payload).json()

    def get_trade_volume(self):
        """ https://docs.gemini.com/rest-api/#get-trade-volume """
        endpoint = '/tradevolume'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload).json()

    def get_past_trades(self, symbol, limit_trades, timestamp=None):
        """ https://docs.gemini.com/rest-api/#get-past-trades """
        endpoint = '/mytrades'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'limit_trades': limit_trades,
            'timestamp': timestamp
        }

        return self._invoke_api(endpoint, payload).json()

    # Order Placement API
    # https://docs.gemini.com/rest-api/#new-order
    # -------------------------------------------
    def new_order(self, client_order_id, symbol, amount, price, side, type, options=None):
        """ https://docs.gemini.com/rest-api/#new-order """
        endpoint = '/order/new'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'client_order_id': client_order_id,
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'side': side,
            'type': 'exchange limit',
            'options': options
        }

        return self._invoke_api(endpoint, payload).json()

    def cancel_order(self, order_id):
        """ https://docs.gemini.com/rest-api/#cancel-order """
        endpoint = '/order/cancel'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'order_id': order_id
        }

        return self._invoke_api(endpoint, payload).json()

    def cancel_session_orders(self):
        """ https://docs.gemini.com/rest-api/#cancel-all-session-orders """
        endpoint = '/order/cancel/session'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload).json()

    def cancel_all_orders(self):
        """ https://docs.gemini.com/rest-api/#cancel-all-active-orders """
        endpoint = '/order/cancel/all'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload).json()

    # Fund Management API's
    # https://docs.gemini.com/rest-api/#get-available-balances
    # --------------------------------------------------------
    def get_balance(self):
        """ https://docs.gemini.com/rest-api/#get-available-balances """
        endpoint = '/balances'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload).json()

    def new_deposit_address(self, currency, label):
        """ https://docs.gemini.com/rest-api/#new-deposit-address """
        endpoint = '/' + currency + '/newAddress'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'label': label
        }

        return self._invoke_api(endpoint, payload).json()

    def withdraw_crypto(self, currency, address, amount):
        """ https://docs.gemini.com/rest-api/#withdraw-crypto-funds-to-whitelisted-address """
        endpoint = '/withdraw/' + currency

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'address': address,
            'amount': amount
        }

        return self._invoke_api(endpoint, payload).json()

from __future__ import print_function

from gemini.error import raise_api_error

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

    API_VERSION = '/v1'

    def __init__(self, api_key, api_secret, sandbox=False):
        self.API_KEY = api_key
        self.API_SECRET = api_secret

        if not sandbox:
            self.BASE_URI = "https://api.gemini.com" + self.API_VERSION
        else:
            self.BASE_URI = "https://api.sandbox.gemini.com" + self.API_VERSION

    # Private API methods
    # -------------------
    def _get_nonce(self):
        return time.time()*1000

    def _handle_response(self, request, response):
        """ Handles all responses from the API. Checks the return HTTP status code and formats the response in JSON. """
        status_code = str(response.status_code)

        if not status_code.startswith('2'):
            raise raise_api_error(request, response)
        else:
            return response.json()

    def _invoke_api(self, endpoint, payload, params=None, pub=True):
        """ Sends the request to the Gemini Exchange API.

            Args:
                endpoint (str):   URL the call will go to
                payload (dict):   Headers containing the request specifics
                params (dict, optional):    A dict containing URL parameters (for public API calls)
                pub(bool, optional):    Boolean value identifying a Public API call (True) or Private API call (False)
        """

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

        # build a request object in case there's an error so we can echo it
        request = {'payload': payload, 'headers': headers, 'url': url}

        if not pub:
            # private api methods are POSTs
            response = requests.post(url, headers=headers)
        else:
            response = requests.get(url, headers=headers, params=params)

        return self._handle_response(request, response)

    # Public API methods
    # ------------------
    def get_symbols(self):
        """ https://docs.gemini.com/rest-api/#symbols """
        endpoint = '/symbols'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=True)

    def get_ticker(self, symbol):
        """ https://docs.gemini.com/rest-api/#ticker """
        endpoint = '/pubticker/' + symbol

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=True)

    def get_order_book(self, symbol):
        """ https://docs.gemini.com/rest-api/#current-order-book """
        endpoint = '/book/' + symbol

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=True)

    def get_trade_history(self, symbol, since=None, limit_trades=None, include_breaks=None):
        """ https://docs.gemini.com/rest-api/#trade-history """

        # build URL parameters
        params = {}
        if since:
            params['since'] = since

        if limit_trades:
            params['limit_trades'] = limit_trades

        if include_breaks:
            params['include_breaks'] = include_breaks

        endpoint = '/trades/' + symbol

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, params, pub=True)

    def get_current_auction(self, symbol):
        """ https://docs.gemini.com/rest-api/#current-auction """
        endpoint = '/auction/' + symbol

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=True)

    def get_auction_history(self, symbol, since=None, limit_auction_results=None, include_indicative=None):
        """ https://docs.gemini.com/rest-api/#auction-history """

        # build URL parameters
        params = {}
        if since:
            params['since'] = since

        if limit_auction_results:
            params['limit_auction_results'] = limit_auction_results

        if include_indicative:
            params['include_indicative'] = include_indicative

        endpoint = '/auction/' + symbol + '/history'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, params, pub=True)

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

        return self._invoke_api(endpoint, payload, pub=False)

    def get_order_status(self, order_id):
        """ https://docs.gemini.com/rest-api/#order-status """
        endpoint = '/order/status'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'order_id': order_id
        }

        return self._invoke_api(endpoint, payload, pub=False)

    def get_trade_volume(self):
        """ https://docs.gemini.com/rest-api/#get-trade-volume """
        endpoint = '/tradevolume'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=False)

    def get_past_trades(self, symbol, limit_trades, timestamp=None):
        """ https://docs.gemini.com/rest-api/#get-past-trades """
        endpoint = '/mytrades'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'limit_trades': limit_trades,
            'timestamp': timestamp
        }

        return self._invoke_api(endpoint, payload, pub=False)

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

        return self._invoke_api(endpoint, payload, pub=False)

    def cancel_order(self, order_id):
        """ https://docs.gemini.com/rest-api/#cancel-order """
        endpoint = '/order/cancel'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'order_id': order_id
        }

        return self._invoke_api(endpoint, payload, pub=False)

    def cancel_session_orders(self):
        """ https://docs.gemini.com/rest-api/#cancel-all-session-orders """
        endpoint = '/order/cancel/session'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=False)

    def cancel_all_orders(self):
        """ https://docs.gemini.com/rest-api/#cancel-all-active-orders """
        endpoint = '/order/cancel/all'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce()
        }

        return self._invoke_api(endpoint, payload, pub=False)

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

        return self._invoke_api(endpoint, payload, pub=False)

    def new_deposit_address(self, currency, label):
        """ https://docs.gemini.com/rest-api/#new-deposit-address """
        endpoint = '/' + currency + '/newAddress'

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'label': label
        }

        return self._invoke_api(endpoint, payload, pub=False)

    def withdraw_crypto(self, currency, address, amount):
        """ https://docs.gemini.com/rest-api/#withdraw-crypto-funds-to-whitelisted-address """
        endpoint = '/withdraw/' + currency

        payload = {
            'request': self.API_VERSION + endpoint,
            'nonce': self._get_nonce(),
            'address': address,
            'amount': amount
        }

        return self._invoke_api(endpoint, payload, pub=False)

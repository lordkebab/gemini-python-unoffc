class GeminiError(Exception):
    """
    Basic exception class for errors raised by the API Library.

    https://docs.gemini.com/rest-api/#error-codes
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class AuctionNotOpen(GeminiError): pass
class ClientOrderIdTooLong(GeminiError): pass
class ClientOrderIdMustBeString(GeminiError): pass
class ConflictingOptions(GeminiError): pass
class EndpointMismatch(GeminiError): pass
class EndpointNotFound(GeminiError): pass
class IneligibleTiming(GeminiError): pass
class InsufficientFunds(GeminiError): pass
class InvalidJson(GeminiError): pass
class InvalidNonce(GeminiError): pass
class InvalidOrderType(GeminiError): pass
class InvalidPrice(GeminiError): pass
class InvalidQuantity(GeminiError): pass
class InvalidSide(GeminiError): pass
class InvalidSignature(GeminiError): pass
class InvalidSymbol(GeminiError): pass
class Maintenance(GeminiError): pass
class MarketNotOpen(GeminiError): pass
class MissingApikeyHeader(GeminiError): pass
class MissingOrderField(GeminiError): pass
class MissingRole(GeminiError): pass
class MissingPayloadHeader(GeminiError): pass
class MissingSignatureHeader(GeminiError): pass
class NoSSL(GeminiError): pass
class OptionsMustBeArray(GeminiError): pass
class OrderNotFound(GeminiError): pass
class RateLimit(GeminiError): pass
class System(GeminiError): pass
class UnsupportedOption(GeminiError): pass

api_error_map = {
    'AuctionNotOpen': AuctionNotOpen,
    'ClientOrderIDTooLong': ClientOrderIdTooLong,
    'ClientOrderIDMustBeString': ClientOrderIdMustBeString,
    'ConflictingOptions': ConflictingOptions,
    'EndpointMismatch': EndpointMismatch,
    'EndpointNotFound': EndpointNotFound,
    'IneligibleTiming': IneligibleTiming,
    'InsufficientFunds': InsufficientFunds,
    'InvalidJson': InvalidJson,
    'InvalidNonce': InvalidNonce,
    'InvalidOrderType': InvalidOrderType,
    'InvalidPrice': InvalidPrice,
    'InvalidQuantity': InvalidQuantity,
    'InvalidSide': InvalidSide,
    'InvalidSignature': InvalidSignature,
    'InvalidSymbol': InvalidSymbol,
    'Maintenance': Maintenance,
    'MarketNotOpen': MarketNotOpen,
    'MissingApikeyHeader': MissingApikeyHeader,
    'MissingOrderField': MissingOrderField,
    'MissingRole': MissingRole,
    'MissingPayloadHeader': MissingPayloadHeader,
    'MissingSignatureHeader': MissingSignatureHeader,
    'NoSSL': NoSSL,
    'OptionsMustBeArray': OptionsMustBeArray,
    'OrderNotFound': OrderNotFound,
    'RateLimit': RateLimit,
    'System': System,
    'UnsupportedOption': UnsupportedOption
}

def raise_api_error(request, response):
    err_txt = response.json()['message'] + '(' + str(request) + ')'
    error = api_error_map.get(response.json()['reason'])

    return error(err_txt)

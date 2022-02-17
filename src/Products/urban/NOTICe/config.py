# -*- coding: utf-8 -*-

_EXTENSIONS_BASE_URL = 'http://soa.spw.wallonie.be/services/noticeTwiceExtensions/messages/v1'

REF_TAG = '{{{url}}}municipalityReference'.format(url=_EXTENSIONS_BASE_URL)

# notificaction status codes
GET_ERROR = 'error when calling getNotification endpoint'
NO_RESULTS = 'no results found for getNotification'
UNBOUND = 'notification does not match any licence'
MATCH = 'notification match a licence but is not created as a task'
BOUND = 'notification match a licence and has been created as a licence task'

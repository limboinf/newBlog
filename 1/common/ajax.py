#coding=utf-8
from django.http import HttpResponse
from django.utils import simplejson
from django.conf import settings

class SimpleAjaxException(Exception):pass

def ajax_ok_data(data='', next=None, message=None):
    
    return ajax_data('ok', data=data, next=next, message=message)

def json_ok_data(data='', message=None):
    return json_data(ajax_data('ok', data=data))

def json_data(data, check=False):
    encode = settings.DEFAULT_CHARSET
    if check:
        if not is_ajax_data(data):
            raise SimpleAjaxException, 'Return data should be follow the Simple Ajax Data Format'
    return simplejson.dumps(uni_str(data, encode))


def ajax_fail_data(error='', next=None, message=None):
    return ajax_data('fail', error=error, next=next, message=message)
    
def ajax_ok(data='', next=None, message=None):
    """
    return a success response
    """
    
    return json_response(ajax_ok_data(data, next, message))

def ajax_fail(error='', next=None, message=None):
    """
    return an error response
    """
   
    return json_response(ajax_fail_data(error, next, message))

def json(data, check=False):
    encode = settings.DEFAULT_CHARSET
    if check:
        if not is_ajax_data(data):
            raise SimpleAjaxException, 'Return data should be follow the Simple Ajax Data Format'
    return simplejson.dumps(uni_str(data, encode))
    
def json_response(data, check=False):
    
    encode = settings.DEFAULT_CHARSET
    
    if check:
        if not is_ajax_data(data):
            raise SimpleAjaxException, 'Return data should be follow the Simple Ajax Data Format'
    try:
        return HttpResponse(simplejson.dumps(uni_str(data, encode)))
    except:
        return HttpResponse(simplejson.dumps(uni_str(data, "gb2312")))


def ajax_data(response_code, data=None, error=None, next=None, message=None):
    """if the response_code is true, then the data is set in 'data',
    if the response_code is false, then the data is set in 'error'
    """
    
    r = dict(response='ok', data='', error='', next='', message='')
    if response_code is True or response_code.lower() in ('ok', 'yes', 'true'):
        r['response'] = 'ok'
    else:
        r['response'] = 'fail'
    if data:
        r['data'] = data
    if error:
        r['error'] = error
    if next:
        r['next'] = next
    if message:
        r['message'] = message
    return r
    
def is_ajax_data(data):
    """Judge if a data is an Ajax data"""
    
    if not isinstance(data, dict): return False
    for k in data.keys():
        if not k in ('response', 'data', 'error', 'next', 'message'): return False
    if not data.has_key('response'): return False
    if not data['response'] in ('ok', 'fail'): return False
    return True

def uni_str(a, encoding=None):
    if not encoding:
        encoding = settings.DEFAULT_CHARSET
    
    if isinstance(a, (list, tuple)):
    
        s = []
        for i, k in enumerate(a):
            s.append(uni_str(k, encoding))
        return s
    elif isinstance(a, dict):
    
        s = {}
        for i, k in enumerate(a.items()):
            key, value = k
            s[uni_str(key, encoding)] = uni_str(value, encoding)
        return s
    elif isinstance(a, unicode):
    
        return a
    elif isinstance(a, (int, float)):
    
        return a
    elif isinstance(a, str) or (hasattr(a, '__str__') and callable(getattr(a, '__str__'))):
    
        if getattr(a, '__str__'):
            a = str(a)
        
        return unicode(a, encoding)
    else:
        return a
    
def get_options_data(data):
    """
    return select element's options
    """
    
    retval = ''
    for item in data:
        retval = retval + item.__option__() + ","
    
    return retval[0:-1]    

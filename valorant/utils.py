# This code is licensed under MIT license (see LICENSE.txt for details)
import re

from .enums import ValorantCountryCodes, ValorantRegions
from time import sleep
from urllib.parse import quote

def encode_uri(str):
    return quote(str, safe='~@#$&()*!+=:;,?/\'')

def is_valid_act_filter(filter):
    valid_filters = [None, 'e3a1', 'e2a3', 'e2a2', 'e2a1', 'e1a3', 'e1a2', 'e1a1']
    return filter in valid_filters

def is_valid_country_code(country_code):
    return country_code in [ValorantCountryCodes.__dict__[k] for k in ValorantCountryCodes.__dict__.iterkeys()]

def is_valid_puuid(puuid):
    regex = re.compile('[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}', re.I)
    match = regex.match(str(puuid))
    return bool(match)

def is_valid_region(region):
    return region in [ValorantRegions.__dict__[k] for k in ValorantRegions.__dict__.iterkeys()]

# https://gist.github.com/n1ywb/2570004
def retries(max_tries, delay=1, backoff=2, exceptions=(Exception,), hook=None):
    """
    Function decorator implementing retrying logic.
    
    delay: Sleep this many seconds * backoff * try number after failure
    backoff: Multiply delay by this factor after each failure
    exceptions: A tuple of exception classes; default (Exception,)
    hook: A function with the signature myhook(tries_remaining, exception);
        default None
    
    The decorator will call the function up to max_tries times if it raises
    an exception.
    
    By default it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.
    
    Additionally you may specify a hook function which will be called prior
    to retrying with the number of remaining tries and the exception instance;
    see given example. This is primarily intended to give the opportunity to
    log the failure. Hook is not called after failure if no retries remain.
    """
    def dec(func):
        def f2(*args, **kwargs):
            mydelay = delay
            tries = reversed(range(max_tries))
            
            for tries_remaining in tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if tries_remaining > 0:
                        if hook is not None:
                            hook(tries_remaining, e, mydelay)
                        sleep(mydelay)
                        mydelay = mydelay * backoff
                    else:
                        raise
                else:
                    break
        return f2
    return dec
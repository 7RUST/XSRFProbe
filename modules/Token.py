#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-:-:-:-:-:-:-::-:-:#
#    XSRF Probe     #
#-:-:-:-:-:-:-::-:-:#

# Author: @_tID
# This module requires XSRFProbe
# https://github.com/0xInfection/XSRFProbe

from re import search, I
from time import sleep
from files.config import *
from core.colors import *
from core.verbout import verbout
from files.discovered import REQUEST_TOKENS
from urllib.parse import urlencode, unquote
from files.paramlist import COMMON_CSRF_NAMES

def Token(req):
    '''
    This method checks for whether Anti-CSRF Tokens are
               present in the request.
    '''
    param = ''  # Initializing param
    query = ''
    # First lets have a look at config.py and see if its set
    if TOKEN_CHECKS:
        verbout(O,'Parsing request for detecting anti-csrf tokens...')
        try:
            # Lets check for the request values. But before that lets encode and unquote the request :D
            con = unquote(urlencode(req)).split('&')
            for c in con:
                for name in COMMON_CSRF_NAMES:
                    qu = c.split('=')
                    if qu[0].lower() == name.lower():
                        verbout(color.GREEN,' [+] The form was requested with a '+color.ORANGE+'Anti-CSRF Token'+color.GREEN+'...')
                        verbout(color.GREY,' [+] Token Parameter: '+color.CYAN+qu[0]+'='+qu[1]+' ...')
                        query, param = qu[0], qu[1]
                        REQUEST_TOKENS.append(param)  # We are appending the token to a variable for further analysis
                        break  # Break execution if a Anti-CSRF token is found

        except Exception as e:
            verbout(R,'Request Parsing Execption!')
            verbout(R,'Error: '+e.__str__())

        if param != '':
            return query, param
        else:
            verbout(color.RED,' [-] The form was requested '+color.BR+' Without an Anti-CSRF Token '+color.END+color.RED+'...')
            print(color.RED+' [-] Endpoint seems '+color.BR+' VULNERABLE '+color.END+color.RED+' to '+color.BR+' POST-Based Request Forgery '+color.END)
            return '', ''

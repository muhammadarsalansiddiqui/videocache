#!/usr/bin/env python
#
# (C) Copyright Kulbir Saini <saini@saini.co.in>
# Product Website : http://cachevideos.com/
#

__author__ = """Kulbir Saini <saini@saini.co.in>"""
__docformat__ = 'plaintext'

import os
import re
import sys
import urllib
import urlparse

VALIDATE_XHAMSTER_DOMAIN_REGEX = re.compile('-xh.clients.cdn[0-9a-zA-Z]?[0-9a-zA-Z]?[0-9a-zA-Z]?.com')
VALIDATE_XHAMSTER_VIDEO_REGEX1 = re.compile('(.*)key=[a-zA-Z0-9]+(.*)\.flv')
VALIDATE_XHAMSTER_VIDEO_REGEX2 = re.compile('(.*)key=[a-zA-Z0-9]+(.*)\.flv')
VALIDATE_XHAMSTER_VIDEO_REGEX3 = re.compile('data\/(.*)\.flv')

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, root_dir)
from common import is_valid_ip

def check_xhamster_video(o, url, host = None, path = None, query = None):
    matched, website_id, video_id, format, search, queue, report_hit = True, 'xhamster', None, '', True, True, True

    if not (host and path and query):
        fragments = urlparse.urlsplit(url)
        [host, path, query] = [fragments[1], fragments[2], fragments[3]]

    if VALIDATE_XHAMSTER_DOMAIN_REGEX.search(host) and VALIDATE_XHAMSTER_VIDEO_REGEX3.search(path):
        pass
    elif is_valid_ip(host) and VALIDATE_XHAMSTER_VIDEO_REGEX1.search(path):
        queue = False
    elif host.find('.xhcdn.com') > -1 and VALIDATE_XHAMSTER_VIDEO_REGEX2.search(path):
        search = False
    else:
        matched = False

    if matched:
        try:
            video_id = urllib.quote(urllib.unquote(path).strip('/').split('/')[-1])
        except Exception, e:
            pass

    return (matched, website_id, video_id, format, search, queue, report_hit)


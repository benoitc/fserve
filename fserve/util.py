# -*- coding: utf-8 -
#
# This file is part of fserve released under the MIT license. 
# See the NOTICE for more information.

def to_bytestring(s):
    """ convert to bytestring an unicode """
    if not isinstance(s, basestring):
        return s
    if isinstance(s, unicode):
        return s.encode('utf-8')
    else:
        return s

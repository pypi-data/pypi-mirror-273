# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import weakref

class WeakValueKeepaliveDictionary(weakref.WeakValueDictionary):
    """A WeakvalueDictionary that has a timeout on its accesses. Values stored
    (or accessed) are kept as strong references for some time between the
    configured `timeout` and twice the timeout, and only become fully weak
    after that."""

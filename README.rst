=======
PyPlete
=======

Information
===========

PYPLETE (PYthon autocomPLETE) is a interface to autocomplete in python.

PyPlete uses pysmell but unlike this, PyPlete is dynamic, it does not need execute a command to pre-analyze the code. This is a good tool to analyze (or autocomplete) the code that you are writing currently

Requeriments
============

 * pysmell

Installation
============

 * Install `Pysmell <http://pypi.python.org/pypi/pysmell>`_
 * Install `pyplete <http://pypi.python.org/pypi/pyplete>`_

::

 easy_install pysmell==0.7.3
 easy_install pyplete==0.0.1
 

Usage (examples)
================


Get the top level importable package and modules:

::

    In [1]: from pyplete import PyPlete
    In [2]: pyplete = PyPlete()
    In [3]: importables = []
    In [4]: autocompletes = pyplete.get_importables_top_level(importables)
    In [5]: autocompletes
    Out[5]: True
    In [6]: importables
    Out[6]: 
    [('smtpd', 'module'),
     ('virtualenv', 'module'),
     ('virtualenv_support', 'package'),
     ('jinja2', 'package'),
     ('geopy', 'package'),
     ('dateutil', 'package'),
     ('pep8', 'module'),
     ('johnny', 'package'),
     ('django_like', 'package'),
     ('django', 'package'),
     ...]

Get the importable subpackages:

::

    In [7]: importables = []
    In [8]: autocompletes = pyplete.get_importables_rest_level(importables, "django", into_module=False)
    In [9]: autocompletes
    Out[9]: True
    In [10]: importables
    Out[10]: 
    [('bin', 'package'),
    ('conf', 'package'),
    ('contrib', 'package'),
    ('core', 'package'),
    ('db', 'package'),
    ('dispatch', 'package'),
    ('forms', 'package'),
    ('http', 'package'),
    ('middleware', 'package'),
    ('shortcuts', 'package'),
    ('template', 'package'),
    ('templatetags', 'package'),
    ('test', 'package'),
    ('test.pystone', 'module'),
    ('test.regrtest', 'module'),
    ('test.test_support', 'module'),
    ('utils', 'package'),
    ('views', 'package'),
    ('VERSION', 'constant')]


Get the importable names:

::

    In [7]: importables = []
    In [8]: autocompletes = pyplete.get_importables_rest_level(importables, "django")
    In [9]: autocompletes
    Out[9]: True
    In [10]: importables
    Out[10]:
    [('bin', 'package'),
    ('conf', 'package'),
    ('contrib', 'package'),
    ('core', 'package'),
    ('db', 'package'),
    ('dispatch', 'package'),
    ('forms', 'package'),
    ('http', 'package'),
    ('middleware', 'package'),
    ('shortcuts', 'package'),
    ('template', 'package'),
    ('templatetags', 'package'),
    ('test', 'package'),
    ('test.pystone', 'module'),
    ('test.regrtest', 'module'),
    ('test.test_support', 'module'),
    ('utils', 'package'),
    ('views', 'package'),
    ('get_version', 'function', ' ()', ''),  # This is the difference
    ('VERSION', 'constant')]

Other example to the importable names:

::

    In [11]: importables = []
    In [12]: autocompletes = pyplete.get_importables_rest_level(importables, "django", ["contrib", "auth", "models"], into_module=True)
    Out[12]:
    [('get_hexdigest',
    'function',
    ' (algorithm, salt, raw_password)',
    "\n    Returns a string of the hexdigest of the given plaintext password and salt\n    using the given algorithm ('md5', 'sha1' or 'crypt').\n    "),
    ...
    ('User',
    'class',
    ' ()',
    '\n    Users within the Django authentication system are represented by this model.\n\n    Username and password are required. Other fields are optional.\n    '),
    ('PermissionManager', 'class', ' ()', ''),
    ('Permission',
    'class',
    ' ()',
    'The permissions system provides a way to assign permissions to specific users and groups of users.\n\n    The permission system is used by the Django admin site, but may also be useful in your own code. The Django admin site uses permissions as follows:\n\n        - The "add" permission limits the user\'s ability to view the "add" form and add an object.\n        - The "change" permission limits a user\'s ability to view the change list, view the "change" form and change an object.\n        - The "delete" permission limits the ability to delete an object.\n\n    Permissions are set globally per type of object, not per specific object instance. It is possible to say "Mary may change news stories," but it\'s not currently possible to say "Mary may change news stories, but only the ones she created herself" or "Mary may only change news stories that have a certain status or publication date."\n\n    Three basic permissions -- add, change and delete -- are automatically created for each Django model.\n    '),
    ...
    ('AnonymousUser', 'class', ' ()', ''),
    ('UNUSABLE_PASSWORD', 'constant')]


Get names importables from a text:

::

    In [13]: importables = []
    In [14]: text = """class A(object):
    ....:     def __init__(self, x, y, z):
    ....:         self.x = x
    ....:         self.y = y
    ....:         self.z = z
    ....:     def xxx(self, a):
    ....:         return a
    ....: def myfunc(u, v):
    ....:     return u + v"""
    In [15]: autocompletes = pyplete.get_importables_from_text(importables, text)
    In [16]: importables
    Out[16]: 
    [('myfunc', 'function', ' (u, v)', ''),
    ('A', 'class', ' (x, y, z)', '')]


Get names importables from a line:

::

    In [17]: importables = []
    In [18]: text = "import requests"
             line = "requests.models."
    In [19]: pyplete.get_importables_from_line(importables, text, line)
    Out[19]: 
    [('Request',
    'class',
    ' (url=None, headers=dict(), files=None, method=None, data=dict(), params=dict(), auth=None, cookies=None, timeout=None, redirect=False, allow_redirects=False, proxies=None, hooks=None, config=None, prefetch=False, _poolmanager=None, verify=None, session=None, cert=None)',
    'The :class:`Request <Request>` object. It carries out all functionality of\n    Requests. Recommended interface is with the Requests functions.\n    '),
    ('Response',
    'class',
    ' ()',
    'The core :class:`Response <Response>` object. All\n    :class:`Request <Request>` objects contain a\n    :class:`response <Response>` attribute, which is an instance\n    of this class.\n    '),
    ('chardet', 'constant'),
    ('REDIRECT_STATI', 'constant'),
    ('CONTENT_CHUNK_SIZE', 'constant')]

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
 easy_install pyplete==0.0.2
 
Next features
=============

 * Treatment of the __all__ variable
 * Change the format of importables, this must be a dict



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
    [{'category': 'module', 'text': 'smtpd'},
     {'category': 'module', 'text': 'make_metadata'},
     {'category': 'module', 'text': 'strace'},
     {'category': 'module', 'text': 'rst2man'},
     {'category': 'module', 'text': 'libxml2macro'},
     {'category': 'package', 'text': 'django_like'},
     {'category': 'package', 'text': 'template_repl'},
     {'category': 'module', 'text': 'pyjslint'},
     {'category': 'package', 'text': 'pyflakes'},
     {'category': 'package', 'text': 'hghooks'},
     {'category': 'package', 'text': 'django'},
    ...]

Get the importable subpackages:

::

    In [7]: importables = []
    In [8]: autocompletes = pyplete.get_importables_rest_level(importables, "django", into_module=False)
    In [9]: autocompletes
    Out[9]: True
    In [10]: importables
    Out[10]: 
    [{'category': 'package', 'text': 'bin'},
     {'category': 'package', 'text': 'conf'},
     {'category': 'package', 'text': 'contrib'},
     {'category': 'package', 'text': 'core'},
     {'category': 'package', 'text': 'db'},
     {'category': 'package', 'text': 'dispatch'},
     {'category': 'package', 'text': 'forms'},
     {'category': 'package', 'text': 'http'},
     {'category': 'package', 'text': 'middleware'},
     {'category': 'package', 'text': 'shortcuts'},
     {'category': 'package', 'text': 'template'},
     {'category': 'package', 'text': 'templatetags'},
     {'category': 'package', 'text': 'test'},
     {'category': 'module', 'text': 'test.pystone'},
     {'category': 'module', 'text': 'test.regrtest'},
     {'category': 'module', 'text': 'test.test_support'},
     {'category': 'package', 'text': 'utils'},
     {'category': 'package', 'text': 'views'}]

Get the importable names:

::

    In [11]: importables = []
    In [12]: autocompletes = pyplete.get_importables_rest_level(importables, "django")
    In [13]: autocompletes
    Out[13]: True
    In [14]: importables
    Out[14]:
    [{'category': 'constant', 'text': 'VERSION'},
     {'args': ' (version=None)',
      'category': 'function',
      'description': 'Derives a PEP386-compliant version number from VERSION.',
      'text': 'get_version'},
     {'category': 'module', 'text': 'test.pystone'},
     {'category': 'module', 'text': 'test.regrtest'},
     {'category': 'module', 'text': 'test.test_support'},
     {'category': 'package', 'text': 'bin'},
     {'category': 'package', 'text': 'conf'},
     {'category': 'package', 'text': 'contrib'},
     {'category': 'package', 'text': 'core'},
     {'category': 'package', 'text': 'db'},
     {'category': 'package', 'text': 'dispatch'},
     {'category': 'package', 'text': 'forms'},
     {'category': 'package', 'text': 'http'},
     {'category': 'package', 'text': 'middleware'},
     {'category': 'package', 'text': 'shortcuts'},
     {'category': 'package', 'text': 'template'},
     {'category': 'package', 'text': 'templatetags'},
     {'category': 'package', 'text': 'test'},
     {'category': 'package', 'text': 'utils'},
     {'category': 'package', 'text': 'views'},
     {'category': 'pointer', 'text': 'get_svn_revision'}]



Other example to the importable names:

::

    In [15]: importables = []
    In [16]: autocompletes = pyplete.get_importables_rest_level(importables, "django", ["contrib", "auth", "models"], into_module=True)
    Out[16]:
    [{'args': ' ()',
      'category': 'class',
      'description': '\n    Users within the Django authentication system are represented by this\n    model.\n\n    Username and password are required. Other fields are optional.\n    ',
      'text': 'User'},
     {'args': ' ()',
      'category': 'class',
      'description': "\n    The manager for the auth's Group model.\n    ",
      'text': 'GroupManager'},
     {'args': ' ()',
      'category': 'class',
      'description': '',
      'text': 'PermissionManager'},
     {'args': ' ()',
      'category': 'class',
      'description': '\n    The permissions system provides a way to assign permissions to specific\n    users and groups of users.\n\n    The permission system is used by the Django admin site, but may also be\n    useful in your own code. The Django admin site uses permissions as follows:\n\n        - The "add" permission limits the user\'s ability to view the "add" form\n          and add an object.\n        - The "change" permission limits a user\'s ability to view the change\n          list, view the "change" form and change an object.\n        - The "delete" permission limits the ability to delete an object.\n\n    Permissions are set globally per type of object, not per specific object\n    instance. It is possible to say "Mary may change news stories," but it\'s\n    not currently possible to say "Mary may change news stories, but only the\n    ones she created herself" or "Mary may only change news stories that have a\n    certain status or publication date."\n\n    Three basic permissions -- add, change and delete -- are automatically\n    created for each Django model.\n    ',
      'text': 'Permission'},
     {'args': ' ()',
      'category': 'class',
      'description': "\n    Groups are a generic way of categorizing users to apply permissions, or\n    some other label, to those users. A user can belong to any number of\n    groups.\n\n    A user in a group automatically has all the permissions granted to that\n    group. For example, if the group Site editors has the permission\n    can_edit_home_page, any user in that group will have that permission.\n\n    Beyond permissions, groups are a convenient way to categorize users to\n    apply some label, or extended functionality, to them. For example, you\n    could create a group 'Special users', and you could write code that would\n    do special things to those users -- such as giving them access to a\n    members-only portion of your site, or sending them members-only email\n    messages.\n    ",
      'text': 'Group'},
     {'args': ' ()',
      'category': 'class',
      'description': '',
      'text': 'UserManager'},
     {'args': ' ()',
      'category': 'class',
      'description': '',
      'text': 'SiteProfileNotAvailable'},
     {'args': ' ()',
      'category': 'class',
      'description': '',
      'text': 'AnonymousUser'},
     {'args': ' (sender, user, **kwargs)',
      'category': 'function',
      'description': '\n    A signal receiver which updates the last_login date for\n    the user logging in.\n    ',
      'text': 'update_last_login'},
     {'args': ' (user, obj)',
      'category': 'function',
      'description': '',
      'text': '_user_get_all_permissions'},
     {'args': ' (user, perm, obj)',
      'category': 'function',
      'description': '',
      'text': '_user_has_perm'},
     {'args': ' (user, app_label)',
      'category': 'function',
      'description': '',
      'text': '_user_has_module_perms'},
     {'category': 'pointer', 'text': 'check_password'},
     {'category': 'pointer', 'text': 'models'},
     {'category': 'pointer', 'text': 'auth'},
     {'category': 'pointer', 'text': '_'},
     {'category': 'pointer', 'text': 'get_random_string'},
     {'category': 'pointer', 'text': 'settings'},
     {'category': 'pointer', 'text': 'ImproperlyConfigured'},
     {'category': 'pointer', 'text': 'make_password'},
     {'category': 'pointer', 'text': 'send_mail'},
     {'category': 'pointer', 'text': 'EmptyManager'},
     {'category': 'pointer', 'text': 'user_logged_in'},
     {'category': 'pointer', 'text': 'smart_str'},
     {'category': 'pointer', 'text': 'timezone'},
     {'category': 'pointer', 'text': 'UNUSABLE_PASSWORD'},
     {'category': 'pointer', 'text': 'ContentType'},
     {'category': 'pointer', 'text': 'is_password_usable'},
     {'category': 'pointer', 'text': 'urllib'}]


Get names importables from a text:

::

    In [17]: importables = []
    In [18]: text = """class A(object):
    ....:     def __init__(self, x, y, z):
    ....:         self.x = x
    ....:         self.y = y
    ....:         self.z = z
    ....:     def xxx(self, a):
    ....:         return a
    ....: def myfunc(u, v):
    ....:     return u + v"""
    In [19]: autocompletes = pyplete.get_importables_from_text(importables, text)
    In [20]: importables
    Out[20]: 
    [{'args': ' (x, y, z)', 'category': 'class', 'description': '', 'text': 'A'},
     {'args': ' (u, v)',
      'category': 'function',
      'description': '',
      'text': 'myfunc'}]


Get names importables from a line:

::

    In [21]: importables = []
    In [22]: text = "import requests"
             line = "requests.models."
    In [23]: pyplete.get_importables_from_line(importables, text, line)
    Out[23]: 
    [{'args': ' (url=None, headers=dict(), files=None, method=None, data=dict(), params=dict(), auth=None, cookies=None, timeout=None, redirect=False, allow_redirects=False, proxies=None, hooks=None, config=None, _poolmanager=None, verify=None, session=None)',
      'category': 'class',
      'description': 'The :class:`Request <Request>` object. It carries out all functionality of\n    Requests. Recommended interface is with the Requests functions.\n    ',
      'text': 'Request'},
     {'args': ' ()',
      'category': 'class',
      'description': 'The core :class:`Response <Response>` object. All\n    :class:`Request <Request>` objects contain a\n    :class:`response <Response>` attribute, which is an instance\n    of this class.\n    ',
      'text': 'Response'},
     {'category': 'constant', 'text': 'REDIRECT_STATI'},
     {'category': 'pointer', 'text': 'HTTPResponse'},
     {'category': 'pointer', 'text': 'urljoin'},
     {'category': 'pointer', 'text': 'get_encoding_from_headers'},
     {'category': 'pointer', 'text': 'dispatch_hook'},
     {'category': 'pointer', 'text': 'MaxRetryError'},
     {'category': 'pointer', 'text': 'TooManyRedirects'},
     {'category': 'pointer', 'text': 'datetime'},
     {'category': 'pointer', 'text': '_HTTPError'},
     {'category': 'pointer', 'text': '_SSLError'},
     {'category': 'pointer', 'text': 'connectionpool'},
     {'category': 'pointer', 'text': 'encode_multipart_formdata'},
     {'category': 'pointer', 'text': 'get_netrc_auth'},
     {'category': 'pointer', 'text': 'Timeout'},
     {'category': 'pointer', 'text': 'urlencode'},
     {'category': 'pointer', 'text': 'RequestException'},
     {'category': 'pointer', 'text': 'urlunparse'},
     {'category': 'pointer', 'text': 'is_py2'},
     {'category': 'pointer', 'text': 'ConnectionError'},
     {'category': 'pointer', 'text': 'str'},
     {'category': 'pointer', 'text': 'CaseInsensitiveDict'},
     {'category': 'pointer', 'text': 'HTTPProxyAuth'},
     {'category': 'pointer', 'text': 'bytes'},
     {'category': 'pointer', 'text': 'chardet'},
     {'category': 'pointer', 'text': 'guess_filename'},
     {'category': 'pointer', 'text': 'requote_uri'},
     {'category': 'pointer', 'text': 'stream_decode_response_unicode'},
     {'category': 'pointer', 'text': 'SCHEMAS'},
     {'category': 'pointer', 'text': 'poolmanager'},
     {'category': 'pointer', 'text': 'dict_from_string'},
     {'category': 'pointer', 'text': 'codes'},
     {'category': 'pointer', 'text': 'URLRequired'},
     {'category': 'pointer', 'text': 'HOOKS'},
     {'category': 'pointer', 'text': 'SimpleCookie'},
     {'category': 'pointer', 'text': 'os'},
     {'category': 'pointer', 'text': 'stream_untransfer'},
     {'category': 'pointer', 'text': 'SSLError'},
     {'category': 'pointer', 'text': 'urlsplit'},
     {'category': 'pointer', 'text': 'HTTPBasicAuth'},
     {'category': 'pointer', 'text': 'urlparse'},
     {'category': 'pointer', 'text': 'HTTPError'}]

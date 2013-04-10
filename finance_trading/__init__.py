"""
The trading platform for all finance product
"""
import os
import platform

VERSION = (0, 1, 1)

#keys are module names used by python imports,
#values - the package qualifier to use for pip
REQUIREMENTS = {
    'django': 'django>=1.3.1',
    'jinja2': 'Jinja2',
    'coffin': 'Coffin>=0.3',
    'south': 'South>=0.7.1',
    'oauth2': 'oauth2',
    'markdown2': 'markdown2',
    'html5lib': 'html5lib==0.90',
    'keyedcache': 'django-keyedcache',
    'djcelery': 'django-celery==2.2.7',
    'recaptcha_works': 'django-recaptcha-works',
    'openid': 'python-openid',
    'pystache': 'pystache==0.3.1',
}

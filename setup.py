#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Flask-Auth',
      version = '0.4',
      description = 'Flask authentication framework',
      author = 'Kaitlin Poskaitis',
      author_email = 'kposkaitis2011@gmail.com',
      url = 'https://github.com/katiepru/python3-flask-auth',
      packages = ['flask_auth'],
      install_requires = ['Flask',
                          'Flask-Login',
                          'python3-ldap',
                          'WTForms'
                         ],
      keywords = 'auth flask login ldap',
      license = "PSF"
     )

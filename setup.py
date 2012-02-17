# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the calendar Sphinx extension using `Google Chart`_ .

.. _Google Chart: http://code.google.com/intl/ja/apis/chart/

This extension enable you to insert charts and graphs in your Sphinx document.
Following code is sample::

   .. schedule::

      item1: 10/1 - 10/3
      item2: 10/4 - 10/6
      item3: 10/5 - 10/7

See more examples and output images in http://packages.python.org/sphinxjp.shibukawa/ .

This module needs internet connection.

'''

requires = ['Sphinx>=0.6', 'funcparserlib']

setup(
    name='sphinxjp.shibukawa',
    version='0.1.1',
    url='http://bitbucket.org/tk0miya/',
    download_url='http://pypi.python.org/pypi/sphinxjp.shibukawa',
    license='BSD',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='Sphinx calendar extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxjp'],
)

sphinxjp.shibukawa extension README
====================================

This is a sphinx extension which render calendar by using
`Google Chart <http://code.google.com/intl/ja/apis/chart/>`_ .

source:

.. code-block:: text

   .. schedule::

      item1: 10/1 - 10/3
      item2: 10/4 - 10/6
      item3: 10/5 - 10/7

rendered:

.. schedule::

   item1: 10/1 - 10/3
   item2: 10/4 - 10/6
   item3: 10/5 - 10/7

Who's shibukawa?
================

Yoshiki Shibukawa (@shibukawa) is great Sphinx evangelist in Japan.
This module is one of gifts for his birthday (11/14)!

Setting
=======

You can see available package at `PyPI <http://pypi.python.org/pypi/sphinxjp.shibukawa>`_.

You can get source code at http://bitbucket.org/tk0miya/

Install
-------

.. code-block:: bash

   $ easy_install sphinxjp.shibukawa


Configure Sphinx
----------------

To enable this extension, add ``sphinxjp.shibukawa`` module to extensions 
option at :file:`conf.py`. 

.. code-block:: python

   # Enabled extensions
   extensions = ['sphinxjp.shibukawa']


Directive
=========

.. describe:: .. schedule::

   This directive insert a calendar into the generated document.
   schedule directive takes code block as source script.

   Examples::

      .. schedule::

         item1: 10/1 - 10/3
         item2: 10/4 - 10/6
         item3: 10/5 - 10/7

   .. schedule::

      item1: 10/1 - 10/3
      item2: 10/4 - 10/6
      item3: 10/5 - 10/7

   You can change interval of date labels using `interval` option.

   Examples::

      .. schedule::
         :interval: 2

         item1: 10/1 - 10/3
         item2: 10/4 - 10/6
         item3: 10/5 - 10/7

   .. schedule::
      :interval: 2

      item1: 10/1 - 10/3
      item2: 10/4 - 10/6
      item3: 10/5 - 10/7


Repository
==========

This code is hosted by Bitbucket.

  https://bitbucket.org/tk0miya/sphinxjp.shibukawa

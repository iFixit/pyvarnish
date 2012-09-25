PyVarnish
=========

PyVarnish is a collection of python management tools for Varnish

Currently it only sends Varnish stat output to Graphite.

Screenshots
-----------

.. image:: http://www.8t8.eu/img/graphite.png


Status
------
This software is used in production and works. Documentation and tests are a work
in progress. If you have any questions please feel free to contact me. Any
contributions are also welcomed.

Resources
---------

* `Bug Tracker <http://github.com/redsnapper8t8/pyvarnish/issues>`_
* `Code <http://github.com/redsnapper8t8/pyvarnish>`_
* `My Blog <http://www.8t8.eu>`_


PyVarnish is a Console App
--------------------------

The PyVarnish package is designed to be run at intervals from crontab. It runs varnishstat on
remote varnish servers using SSH commands and sends the data it receives to a
Graphite server over UDP.

Installation
------------

This guide assumes that you already have a Graphite server set up.
Graphite: http://graphite.wikidot.com/

It also assumes familiarity with SSH. In order to run properly PyVarnish needs
to be able to run command remotely. The recommended way to do this is to set up
a restricted account on each of your varnish servers with permission to run a
single command

Below is an example of ssh authorized_keys file for the graphite user on your
varnish server.

``command="/usr/local/bin/graphitewrapper.sh",no-port-forwarding,no-X11-forwarding,no-pty ssh-rsa  publickey```


/usr/local/bin/graphitewrapper.sh might look like this ::


    #!/bin/sh
    # http://binblog.info/2008/10/20/openssh-going-flexible-with-forced-commands/
    case "$SSH_ORIGINAL_COMMAND" in
        "varnishstat -x")
                varnishstat -x
                ;;
        "sysctl fs.file-nr")
                /sbin/sysctl fs.file-nr
                ;;
        *)
                exit 1
                ;;
    esac



To install the PyVarnish package
--------------------------------

from github ::

    pip install https://github.com/redsnapper8t8/pyvarnish/zipball/master

or simply download to a local directory and run from there.

PyVarnish settings can be specified in a config file; copy
``config.ini.example`` to ``~/.config/pyvarnish/config.ini`` and change the
values as you like.

Alternatively, PyVarnish takes command-line parameters that override settings
defined in the config file.  See ``--help`` for more information.


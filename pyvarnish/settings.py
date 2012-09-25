# -*- coding: utf-8 -*-
import os
try:
    from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
except ImportError:
    # Renamed in py3k
    from configparser import SafeConfigParser, NoOptionError, NoSectionError

__author__ = 'John Moylan'

defaults = {
    'varnish_servers': 'localhost',
    'ssh_config':  os.path.expanduser('~/.ssh/config'),
    'debug':  'True',
    'carbon_server':  'localhost',
    'carbon_port':  '2003',
}

config = SafeConfigParser(defaults)
# Loosely follow the XDG Base Directory Specification:
# http://standards.freedesktop.org/basedir-spec/basedir-spec-0.6.html
configPath = os.path.expanduser('~/.config/pyvarnish/config.ini')
config.read(configPath)
  
VARNISH_SERVERS = config.get('DEFAULT', 'varnish_servers').split(',')
VARNISH_SERVERS = [server.strip() for server in VARNISH_SERVERS]
SSH_CONFIG = config.get('DEFAULT', 'ssh_config')
DEBUG = config.getboolean('DEFAULT', 'debug')
CARBON_SERVER = config.get('DEFAULT', 'carbon_server')
CARBON_PORT = config.getint('DEFAULT', 'carbon_port')


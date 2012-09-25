# -*- coding: utf-8 -*-
#!/usr/bin/env python

import time
import socket

from argparse import ArgumentParser
from lxml import etree
from traceback import format_exc
from StringIO import StringIO

import pyvarnish
from pyvarnish.remote import Varnish_admin


class VarnishGather():

    def __init__(self, server):
        self.server_name = server.replace('.','_')
        self.lines = []

    def parse_xml(self, xml):
        tree = etree.parse(xml)
        root = tree.getroot()

        stat_time = root.get('timestamp')
        epochstamp = time.mktime(time.strptime(stat_time, '%Y-%m-%dT%H:%M:%S'))

        lines = []
        for node in root:
            for stat in  node:
                if stat.tag == "name" and stat.getnext().tag == "value":
                    self.lines.append('varnish.%s.%s %s %d' % (self.server_name,
                                                               stat.text,
                                                               stat.getnext().text,
                                                               int(epochstamp)))

    def parse_sysctl(self, input):
        epochstamp = int(time.time())
        key = "varnish.%s.%s_current" % (
            self.server_name, input.split()[0].replace('.','_'))
        value = input.split()[2]
        #append current useage
        self.lines.append("%s %s %d" % (key, value, epochstamp))

        key = "varnish.%s.%s_total" % (
            self.server_name, input.split()[0].replace('.','_'))
        value = input.split()[4]
        #append total useage
        self.lines.append("%s %s %d" % (key, value, epochstamp))





def msg(message):
    return '\n'.join(message) + '\n'


def main():
    from pyvarnish.settings import VARNISH_SERVERS, SSH_CONFIG, DEBUG, \
                                   CARBON_SERVER, CARBON_PORT
    parser = ArgumentParser(description=pyvarnish.__description__)
    
    parser.add_argument('--varnish-servers', nargs='+', metavar='SERVER')
    parser.add_argument('--carbon-server', action='store', metavar='SERVER')
    parser.add_argument('--carbon-port', action='store', metavar='PORT')
    parser.add_argument('--ssh-config', action='store',
                        metavar='SSH_CONFIG_FILE', type=int)
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--version', action='version',
                        version='pyvarnish %s' % pyvarnish.__version__)
    
    args = parser.parse_args()
    if args.varnish_servers:
        VARNISH_SERVERS = args.varnish_servers
    if args.carbon_server:
        CARBON_SERVER = args.carbon_server
    if args.carbon_port:
        CARBON_PORT = args.carbon_port
    if args.ssh_config:
        SSH_CONFIG = args.ssh_config
    if args.debug is not None:
        DEBUG = args.debug
    
    for server in VARNISH_SERVERS:
        if DEBUG:
            print 'Connecting to Varnish server at %s...' % server
        try:
            #connect to server
            vserver = Varnish_admin(server, SSH_CONFIG)
            data = vserver.runcmd("varnishstat -x")
        except Exception:
            if DEBUG:
                print "Whoops, that didn't work.  Here's the exception:"
                print format_exc()
                print "Continuing on to the next server..."
            continue

        #print data
        xml = StringIO(data)

        if DEBUG:
            print "Here's the data we got:"
            print data

        vg = VarnishGather(server)

        #parseXML
        try:
            vg.parse_xml(xml)
        except etree.XMLSyntaxError:
            break

        #get fildescriptors counter
        vg.parse_sysctl(vserver.runcmd("sysctl fs.file-nr"))

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            for i in range(0, len(vg.lines), 50):
                sock.sendto( msg(vg.lines[i:i+50]), (CARBON_SERVER, CARBON_PORT))
        except:
            import sys, traceback
            print "failed"
            traceback.print_exc(file=sys.stdout)
        finally:
            sock.close()
    if DEBUG:
        print 'All done!'


if __name__ == "__main__":
    main()


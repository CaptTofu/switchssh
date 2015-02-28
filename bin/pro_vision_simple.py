#!/usr/bin/env python

from switchssh.pro_vision import ProVision 
import os
import re

import pprint

pp = pprint.PrettyPrinter(indent=2)

# simple script to show how to use this library
def main():
    conn = ProVision('192.168.1.x',
                     'operator',
                     'redacted',
                     read_end="tty=none",
                     dismiss_banner=True) 

    out = conn.exec_command("show run\n")
    pp.pprint(out)
    out = conn.exec_command("configure\n")
    pp.pprint(out)
    out = conn.exec_command("vlan 88\n")
    pp.pprint(out)
    out = conn.exec_command("name eighty-eight\n")
    pp.pprint(out)
    out = conn.exec_command("exit\n")
    pp.pprint(out)
    out = conn.exec_command("exit\n")
    pp.pprint(out)
    out = conn.exec_command("show run\n")
    pp.pprint(out)
    out = conn.exec_command("configure\n")
    pp.pprint(out)
    out = conn.exec_command("no vlan 88\n")
    pp.pprint(out)
    out = conn.exec_command("show run\n")
    pp.pprint(out)


main()

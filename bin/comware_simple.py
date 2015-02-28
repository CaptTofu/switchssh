#!/usr/bin/env python

from switchssh.comware_hp_1910 import ComWareHP1910 
import os
import re

import pprint

pp = pprint.PrettyPrinter(indent=2)

# simple script that shows how to use the library with comware
def main():
    conn = ComWareHP1910('192.168.1.x',
                     'admin',
                     'redacted',
                     read_end="<HP>",
                     dismiss_banner=False) 

    out = conn.exec_command("display current-configuration\n", read_end='<HP>')
    pp.pprint(out) 
    prompt = conn._get_prompt()
    print "prompt: %s\n" % prompt


main()

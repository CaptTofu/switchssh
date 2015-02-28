#!/usr/bin/python
#coding: utf-8 -*-

#
# (c) 2015, Patrick Galbraith <patg@patg.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re
import paramiko
import os

class SwitchSSH:
    def __init__(self,
                 host,
                 username,
                 password,
                 timeout=30,
                 port=22,
                 private_key_file=None,
                 read_end="",
                 disable_paging_cmd="",
                 dismiss_banner=False,
                 more_pattern=""):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.private_key_file = private_key_file
        self.timeout = timeout
        self._error_msg = ""
        self._more_pattern = more_pattern
        self._disable_paging_cmd = '' 
        self._disable_paging_cmd = disable_paging_cmd
        self._dismiss_banner = dismiss_banner
        self._read_end = read_end

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.private_key_file is not None:
            self.keyfile = os.path.expanduser("~/.ssh/known_hosts")
            key_filename = os.path.expanduser(self.private_key_file)
        else:
            key_filename = None

        # TODO: get ansible constants working
        #C.HOST_KEY_CHECKING:
        if True:
            ssh.load_system_host_keys()

        allow_agent = True
        if self.password is not None:
            allow_agent = False

        self.foo()
        try:
            ssh.connect(self.host,
                        username=self.username,
                        password=self.password,
                        key_filename=key_filename,
                        allow_agent=allow_agent,
                        look_for_keys=False,
                        timeout=self.timeout)
        # TODO: more specific error-handling (?)
        except Exception, e:
            message = "%s %s" % (e.__class__, e)
            self.fail(message)

        # handle to connection
        self.ssh = ssh

        try:
            self.channel = ssh.invoke_shell()
        except Exception, e:
            message = "%s %s" % (e.__class__, e)
            self.fail(message)

        if self._dismiss_banner:
            self.channel.send(" ")

        self._disable_paging()

    def foo(self):
        print "SwitchSSH\n"

    def _disable_paging(self):
        self.exec_command(self._disable_paging_cmd,
                           read_end=self._disable_paging_cmd)

    def fail(self, message=''):
        self._error_msg += message

    def send_command(self, command, msg=""):
        try:
            self.channel.send(command)
        except Exception, e:
            msg = msg + "%s %s" % (e.__class__, e)
            self.fail(msg)

    def exec_command(self, command, read_output=True, read_end='', read_start='', msg=''):
        output_list = ''
        try:
            self.channel.send(command)
        except Exception, e:
            msg = msg + "%s %s" % (e.__class__, e)
            self.fail(msg)

        if read_output:
            output_list = self._get_output_list(read_end, read_start)
            for line in output_list:
                m = re.match('^Invalid input: (.*)$', line)
                if m and m.group(1):
                    msg = "Switch ERROR: command %s failed with %s" %\
                        (command, m.group(1))
                    self.fail(msg)
        return output_list

    def _get_output(self, read_end="", read_start="", more_pattern=""):
        output_buf = ""
        append_flag = False 
        if not len(read_end):
            if len(self._read_end):
                read_end = self._read_end

        # append everything
        if not len(read_start):
            append_flag = True

        # common ones
        if not len(read_end):
            read_end = '(\>\s$|\# $)'

        if not len(more_pattern):
            more_pattern = self._more_pattern

        counter = 0
        # very crude, but there is no way I've found to know
        # when there is nothing to read, even within the paramiko API
        # I couldn't find a reliable way
        max_lines_before_bail = 1000
        while True and counter < max_lines_before_bail:
            read_buf = self.channel.recv(1024)
            read_buf = read_buf.replace("\r", "")

            # in case 'no page' isn't used or model doesn't use
            if re.match(more_pattern,
                read_buf, re.DOTALL):
		self.channel.send(" ") 

            # only start appending output if this is seen
            if len(read_start) and read_start in read_buf:
                append_flag = True

            if append_flag:
                output_buf += read_buf

            if re.match(read_end, read_buf, re.DOTALL):
                break
            elif read_end in read_buf:
                    break 

            counter += 1

	return output_buf 

    def _get_output_list(self, read_end='', read_start='', keep_prompt=False):
        output_buf = self._get_output(read_end, read_start)

        output_list = output_buf.split('\n')
        list_length = len(output_list)
        if not keep_prompt:
            list_length -= 1

        return output_list[0:list_length]

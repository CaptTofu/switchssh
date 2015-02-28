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

import pprint
pp = pprint.PrettyPrinter(indent=4)
from switchssh import SwitchSSH
import re

class ComWareHP1910(SwitchSSH):
    def _disable_paging(self):
        self._top_level_prompt = '<HP>'
        self._dev_mode()
        cmd_disable_paging = "screen-length disable\n"
        buf = self.exec_command(cmd_disable_paging, self._top_level_prompt)

    def _dev_mode(self):
        buf = self._get_output(read_end=self._top_level_prompt)
        self.exec_command('_cmdline-mode on\n', read_end='Continue? [Y/N]')
        self.exec_command('Y\n512900\n', read_end=self._top_level_prompt)

    def _get_prompt(self):
        prompt_regex = '^.*([<\[]HP[>\]]).*$'
        self._send_command("\n")
        prompt_list = self._get_output_list(read_end=prompt_regex, keep_prompt=True)
        prompt = prompt_list[len(prompt_list) - 1]
        m = re.search(prompt_regex, prompt)
        if m:
            prompt = m.group(1)
            return prompt
        return ""


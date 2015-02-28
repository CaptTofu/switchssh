# switchssh

A very simple Object-Oriented library for writing python code that talks to switches. Inspired by the Paramiko Expect package. 

I created this to use with my ansible modules for HP Pro Vision and Comware switches. I found that Paramiko Expect, as nice as it was, didn't handle a lot of the output switches threw its way. I found in developing my Ansible switch modules that talking to switches can be tricky business and you can't expect it to work like a Posix host.


## API

### Connection / Instantiation:

Usage is very simple and straightforward. It should be noted that the base class won't be used and that the specific sub-class for SwitchSSH will be used.


    conn = SwitchSSH(host,
                     username,
                     password,
                     timeout=30,
                     port=22,
                     private_key_file=None,
                     read_end="",
                     disable_paging_cmd="",
                     dismiss_banner=False,
                     more_pattern=""):


Parameters

* host - the host - required 
* username - the username for the switch - required 
* password - the password of the switch - required 
* timeout - timeout for connection (30 seconds default)
* port - port (22 is the default)
* private_key_file - specify 
* read_end - the pattern the indicates all text has been output from the switch
* disable_paging_cmd - a command, if any, to disable paging. Paging makes parsing output difficult.
* dismiss_banner - some switches (Pro Vision) display a banner you have to dismiss to use the switch
* more_pattern - in case paging is not turned off, the pattern to use that indicates paging 

Returns:

A connection handle to the switch

#### Example connection

An example of connect to the switch. In this example, the Pro Vision is used:

```
from switchssh.pro_vision import ProVision 

conn = ProVision('192.168.1.X',
                 'operator',
                 'redacted',
                  read_end="tty=none",
                  dismiss_banner=True) 
```


```conn``` is the handle that will be used for communicating with the switch

### Sending commands to the switch

The first method is ```exec_command```. It simply sends a command and returns a list with the output, entry per-line

    output_list = exec_command(command,
                                read_output=True,
                                read_end='',
                                read_start='', 
                                msg=''):

* command - the command to run (required)
* read_output - boolean that states whether or not to read the output
* read_end - the string/pattern to expect that indicates switch has sent all output
* read_start - in some cases, you may want to start "collecting" output after a given pattern is seen
* msg - A message that, if any error occurs, will have the error appended to 

Returns

A list, each member a line of output from the switch.

```
    out = conn.exec_command("show run\n")
```

```out``` would contain:

```
[ ' show run',
  '',
  'Running configuration:',
  '',
  '; J9575A Configuration Editor; Created on release #KA.15.03.3015',
  '; Ver #01:00:01',
  '',
  'hostname "HP E3800-24G-2SFP+ Switch" ',
  'module 1 type J9575x ',
  'vlan 1 ',
  '   name "DEFAULT_VLAN" ',
  '   untagged 1,8-26 ',
  '   ip address 192.168.1.200 255.255.255.0 ',
  '   no untagged 2-7 ',
  '   exit ',
  'vlan 66 ',
  '   name "VLAN" ',
  '   ip address 192.168.10.1 255.255.255.0 ',
  '   ip address 192.168.11.2 255.255.255.0 ',
  '   tagged 5-8 ',
  '   exit ',
  'vlan 44 ',
  '   name "VLAN_44" ',
  '   untagged 2-7 ',
  '',
  '   ip address 192.168.3.4 255.255.255.0 ',
  '   ip address 192.168.5.6 255.255.255.0 ',
  '   tagged 20-24 ',
  '   exit ',
  'console terminal none',
  'snmp-server community "public" unrestricted',
  'snmp-server contact "Patrick Galbraith"',
  'oobm',
  '   ip address dhcp-bootp',
  '   exit',
  'no autorun',
  'no dhcp config-file-update',
  'no dhcp image-file-update',
  'password manager',
  'password operator',
  '',


```

There are simple code examples for each type of switch in the ```./bin``` directory of the the module

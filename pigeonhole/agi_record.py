#!/usr/bin/python

"""
Example to get and set variables via AGI.

You can call directly this script with AGI() in Asterisk dialplan.
"""

from asterisk.agi import *

agi = AGI()
agi.answer()
agi.verbose("python agi started")

# record file <filename> <format> <escape_digits> <timeout> [<offset samples>] [<BEEP>] [<s=silence>]
# record_file(self, filename, format='gsm', escape_digits='#', timeout=20000, offset=0, beep='beep')

# agi.record_file('/tmp/test2.ulaw','ulaw')
#RECORD FILE $tmpname $format \"$intkey\" \"$abs_timeout\" $beep \"$silence\"\n";

filename = '/tmp/test5'
format = 'ulaw'
intkey = '#'
timeout = 20000
beep = 'beep'
offset = '0'
silence = 's=5'
agi.execute('RECORD FILE', (filename), (format), (intkey), (timeout), (offset), (beep), (silence))
# agi.record_file((filename), (format))

"""
while True:
  agi.stream_file('/var/lib/asterisk/sounds/en/tt-codezone')
  result = agi.wait_for_digit(-1)
  agi.verbose("got digit %s" % result)
  if result.isdigit():
    agi.say_number(result)
  else:
   agi.verbose("bye!")
   agi.hangup()
   sys.exit()
"""

# result = agi.wait_for_digit()
# agi.verbose("got digit %s" % result)


# Get variable environment
extension = agi.env['agi_extension']

# Get variable in dialplan
phone_exten = agi.get_variable('PHONE_EXTEN')

# Set variable, it will be available in dialplan
agi.set_variable('EXT_CALLERID', (digit))

# asterisk-ivr

_Not much to see here_

Just my work Area for IRV testing

## Read & Record

This is an example of using Automatic Speech Reconnection (ASR) and `Read()` to accept **BOTH** DTMF and Speech input from the dialplan user.  
- ASR is handled by the [Cloud Speech API](https://cloud.google.com/speech/)
- `Read()` is handled by `pyst2/agi.get_data()`
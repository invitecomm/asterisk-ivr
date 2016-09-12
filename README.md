# asterisk-ivr

_Not much to see here_

Just my work Area for IRV testing

## Read & Record

This is an example of using Automatic Speech Reconnection (ASR) and `Read()` to accept **BOTH** DTMF and Speech input from the dialplan user.  
- Recording File for ASR uses `Monitor()` command to start recording.
- `Read()` is handled by `pyst2/agi.get_data()`
- `StopMonitor()` is called when `#` is pressed.
- If no digits entered, process recording using the [Google Cloud Speech API](https://cloud.google.com/speech/)

Key Lines in the Code:
```python
agi.exec_command('Monitor', 'ulaw', (filename), 'o')
res = agi.get_data('beep', 20000, 8)
agi.exec_command('StopMonitor')

if res:
    print(res)
if not res:
    response_data = main(filename + '-in.ulaw', languageCode)
    print(json.dumps(response_data, ensure_ascii=False))
```
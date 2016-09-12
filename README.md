# asterisk-ivr

_Not much to see here_

Just my work Area for IRV testing

## Read & Record

This is an example of using Automatic Speech Recognition (ASR) and `Read()` to accept **BOTH** DTMF and Speech input from the dialplan user.  
- Recording the file for ASR uses the Asterisk `Monitor()` command to start recording.
- `Read()` is handled by the `get data` AGI command.  `pyst2/agi.get_data()`
- `StopMonitor()` is called when `#` is received _or timeout_.
- If no digits are entered, processes recorded file using the [Google Cloud Speech API](https://cloud.google.com/speech/)

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
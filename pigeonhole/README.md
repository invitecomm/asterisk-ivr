# The Pigeonhole

**My work area, where varios things are stashed** 

## wardial.py

This is a `working copy` that's used for testing and to define what functions will be needed in the end package.  

Contents are mostly junk, but useful to see how the package got where it is.

## Read & Record

This is an example of using Automatic Speech Recognition (ASR) and `Read()` to accept DTMF or Speech input from the dialplan user.  

**Records a file and accepts DTMF input simultaneously.**
- Recording the file for ASR uses the Asterisk `Monitor()` command to start recording.
- `Read()` is handled by the `get data` AGI command.  `pyst2/agi.get_data()`
- `StopMonitor()` is called when `#` is received _or a timeout_.
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
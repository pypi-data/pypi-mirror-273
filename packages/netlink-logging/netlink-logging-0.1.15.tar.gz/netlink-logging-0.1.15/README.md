# netlink-logging

_Part of the NetLink Python Tools_

A small wrapper around python logging and [logzero](https://logzero.readthedocs.io/en/latest/).

## Features

- Log to a logfile automatically (same name as the top-level script, `_input_` for console)
- Additional levels:
  - `TRACE` (`5`)
  - `VERBOSE` (`15`)
  - `SUCCESS` (`25`)
- Timestamps are in UTC and use format `%Y-%m-%d %H:%M:%S`
- Uncaught Exceptions are logged as `CRITICAL`

## Installation

```bash
pip install netlink-logging
```

## Usage

```python
from netlink.logging import logger 

logger.trace('A TRACE entry.')
logger.debug('A DEBUG entry.')
logger.verbose('A VERBOSE entry.')
logger.info('An INFO entry.')
logger.success('A SUCCESS entry.')
logger.warning('A WARNING entry.')
logger.error('An ERROR entry.')
logger.critical('A CRITICAL entry.')
```

results in

``` 
[D 2022-02-32 26:27:28 <input>:…] A DEBUG entry.
[V 2022-02-32 26:27:28 <input>:…] A VERBOSE entry.
[I 2022-02-32 26:27:28 <input>:…] An INFO entry.
[S 2022-02-32 26:27:28 <input>:…] A SUCCESS entry.
[W 2022-02-32 26:27:28 <input>:…] A WARNING entry.
[E 2022-02-32 26:27:28 <input>:…] An ERROR entry.
[C 2022-02-32 26:27:28 <input>:…] A CRITICAL entry.
```

## Additional Methods

### `set_file`

Use `set_file` to change the file that is logged to:

```
logger.set_file([filename, 
                [formatter,] 
                [mode,] 
                [max_bytes,] 
                [backup_count,] 
                [encoding,] 
                [log_level,] 
                [disable_stderr_logger]])
```

#### Parameters

- **filename** (optional, `str`)

  Must be provided, if any other parameter is provided. If not provided, or set to `None` logging to file is disabled.

- **formatter** (optional, `logging.Formatter`)
  
  Formatter to use for logging to file. Defaults to `[K time module:line number] (message`, where 
  - **K** is the first letter of the logging level
  - **time** is `%Y-%m-%d %H:%M:%S` in UTC
  - **module** and **line number show the location in code
  - **message** as provided in call

- **mode** (optional, `str`)

  Mode to open the file with. Defaults to `a`.

- **max_bytes** (optional, `int`)
  
   Size of the logfile when rollover should occur. If set to `0`, rollover never occurs. Defaults to `100 MB`. 

- **backup_count** (optional, `int`)

  Number of backups to keep. If set to 0, rollover never occurs. Defaults to `5`.

- **encoding** (optional, `str`)
 
  Used to open the file with that encoding. Defaults to `utf-8`.

- **log_level** (optional, `int`)

  Set a custom logging level for the file logger. Defaults to the current logging level.

- **disable_stderr_logger** (optional, `bool`)

  Should the default stderr logger be disabled. Defaults to `False`.


### `set_level`

The current logging level can be set without additional imports:

```python
from netlink.logging import logger

logger.set_level(logger.ERROR)
```

### `enable_file`

Enable logging to file, if it was disabled. Takes _boolean_.

### `disable_file`

Disable logging to file.

### `hide_location`

Hide module name and line number.

### `show_threading`

Show thread name.

### `hide_threading`

Hide thread name.


## Changes

### 0.1.10

Option to show or hide thread name

## Roadmap

An additional feature that is considered would log **every** Exception raised.

## License

### MIT License

Copyright (c) 2022 Bernhard Radermacher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

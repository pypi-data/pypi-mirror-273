# TLS - Temporary Linux(Alpine) Shell/System

🚀 TLS provides a convenient way to start a temporary Alpine Linux shell/system using Python.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Alpine Linux](https://img.shields.io/badge/Alpine_Linux-%230D597F.svg?style=for-the-badge&logo=alpine-linux&logoColor=white)

[![PyPI download month](https://img.shields.io/pypi/dm/Temp-Linux-Shell.svg)](https://pypi.python.org/pypi/Temp-Linux-Shell/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/Temp-Linux-Shell.svg)](https://pypi.python.org/pypi/Temp-Linux-Shell//)

![Screenshot of TLS](https://github.com/Noriskky/TLS/blob/main/pictures/screenshot.png?raw=true) 

## Testing

If you just want to test ``TLS`` without installing it you can do that with the following command:
```bash
source <(curl -sSL https://raw.githubusercontent.com/Noriskky/TLS/main/scripts/tls.sh)
```


**NOTE**: 
THIS will not install the script! <br>
This script only writes to ``/var/tmp`` so the changes will not be permanent, and it's using a temporary VENV.

## Installation

You can install TLS via Pip:

```bash
pip install Temp-Linux-Shell
```

## Usage

Once installed, you can start a temporary Alpine Linux shell by running the `tls` command.

### Options

- `-h` or `--help`: Display the help message.
- `-d`: Specify a custom directory.
- `-hn` or `--hostname`: Specify a custom hostname.
- `-c` or `--command`: Specify a command to be executed at the start. After the completion of the command, the session closes.

## Support

There is currently only Support for Linux because it is using ``Chroot`` it's planned to migrate to Docker or something else.

## How to contribute

Hey if you want to contribute to this Project you are welcome to do that
for testing you can use ``Temp-Linux-Shell/test.py`` with the following command

```bash
make clean
make install
make run
```
or you can do:

```bash
make all
```

It will install tls in a Python venv __**you may have to install some packages manually into the Venv**__.

## Compile from Source

### Building

If you want to compile and install it from source you can build it with the following command:
```bash
make clean
make build
```
The output will be in ``./dist`` it can be installed with: 
```bash
pip install dist/tls-<version>.tar.gz
```
Replace ``<version>`` with the current defined in ``setup.py``.

### Installing & Building

```bash
make clean
make install
```

This installs in the Venv.

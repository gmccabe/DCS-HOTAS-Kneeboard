# DCS HOTAS Kneeboard Generator

This application generates kneeboard images of the X-55 and X-56 HOTAS aircraft configurations. Configurations from each aircraft are scanned from the selected DCS folder. Additionally, SRS or Discord(WIP) HOTAS settings are included if detected. Generated kneeboard images are placed in the appropriate aircraft folders.

## Usage

This application can be initatiated by either 
```bash
python dcs-hotas-kneeboard.py
```
or
```bash
run.cmd
```
or use the [standalone executable](https://github.com/gmccabe/DCS-HOTAS-Kneeboard/releases) built using pyinstaller.

## Dependencies

```python
wxPython==4.0.6
Pillow==6.0.0
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
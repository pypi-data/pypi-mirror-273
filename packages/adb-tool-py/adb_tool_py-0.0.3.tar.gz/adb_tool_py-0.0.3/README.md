# adb-tool-py

adb-tool-py is a library for using Android Debug Bridge (ADB) functionality from Python.

It also provides extended functionality.

## Features

- Communication with Android devices
- Parsing the displayed ViewTree
  - Search/touch strings
  - ID search/touch
    - Search/touch etc.

## Installation

```bash
pip install adb-tool-py
```

## Usage

```python
import adb_tool_py as adb_tool

adb1 = adb_tool.AdbTool()
adb2 = adb_tool.AdbTool(serial="emulator-5554")

ret1 = adb1.query("shell ls -al")
ret2 = adb2.query("shell ls -al")

print(ret1.returncode)
print(ret1.stdout)
print(ret1.stderr)

print(ret2.returncode)
print(ret2.stdout)
print(ret2.stderr)
```

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you encounter any issues, please report them through the GitHub issue tracker.

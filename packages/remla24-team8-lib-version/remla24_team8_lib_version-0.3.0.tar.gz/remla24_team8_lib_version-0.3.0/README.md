# lib-version

A version-aware library that can can be asked for the version of the library. This can be useful, for example, for verbose system information in log messages or data records. The library may also contain other logic.

• Create a VersionUtil class that can be asked for its version.
(Try to parse meta-data that is included in the package or explicitly store the version in a separate file.)

• The library is versioned automatically, e.g., by picking-up on the corresponding Git version tag.

• A workflow is used to automatically release the library in a package registry that matches the language.(As stated before, this includes either supported package registries on GitHub or repository tags in languages that support it.)

## Installation
The package is avaiable on pypi and can be installed directly using:

```shell
pip install remla24-team8-lib-version
```

## Usage

To get the current version include the following lines:

```python
from versioning_util.versioning import Version_Util
util = VersionUtil()
print(util.get_version_from_setup())
```




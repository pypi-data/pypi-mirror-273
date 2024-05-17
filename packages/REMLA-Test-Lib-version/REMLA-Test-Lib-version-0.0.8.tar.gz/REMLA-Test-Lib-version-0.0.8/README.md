# LIB-VERSION

LIB-VERSION is a version-aware library designed to provide robust version management and utility functions. This library is ideal for projects requiring precise version tracking, such as in detailed logging or system monitoring environments.

## Features

- **Version Retrieval**: Easily retrieve the current library version using the `VersionUtil` class.
- **Automatic Versioning**: Utilizes Git tags to automatically version the library.
- **CI/CD Integration**: Automatically publishes new versions to a package registry when tagged in Git.

## Getting Started

### Prerequisites

- Git (for versioning)
- Python 3.x (if using Python)
- Access to a package registry pip

### Installation

To install Library Name, use the following command:

```bash
pip install REMLA-Test-Lib-version
```


### Usage
To retrieve the current version of the library:

```python
from REMLA_Test_Lib_version import VersionUtil
print(VersionUtil.VersionUtil.get_version())
```

### How Versioning Works
The library's version is determined by Git tags. When a new tag is pushed to the repository, a CI/CD pipeline updates a VERSION file in the repository with the current tag. This version is then read by the VersionUtil class.

### Setting up Git Tags
To create a new version, tag your commit with the version number:

```bash
git tag -a v1.0.1 -m "Release version 1.0.1"
git push origin v1.0.1
```

### Automated Version Updates
A GitHub Actions workflow is set up to detect when a new tag is pushed and updates the VERSION file automatically. This is then committed back into the repository. See .github/workflows/updateVersion.yml for the workflow configuration.

### Publishing to a Registry
When a new tag is pushed, another GitHub Actions workflow triggers to build and publish the package to the designated package registry. See .github/workflows/updateVersion.yml for the details.

### License
This project is licensed under the MIT - see the LICENSE file for details.


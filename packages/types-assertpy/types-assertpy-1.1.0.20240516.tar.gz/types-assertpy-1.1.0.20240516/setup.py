from setuptools import setup

name = "types-assertpy"
description = "Typing stubs for assertpy"
long_description = '''
## Typing stubs for assertpy

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`assertpy`](https://github.com/assertpy/assertpy) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`assertpy`.

This version of `types-assertpy` aims to provide accurate annotations
for `assertpy==1.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/assertpy. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `77d6947479a7ba2cddc6b50d5600a941a84ca4d4` and was tested
with mypy 1.10.0, pyright 1.1.363, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="1.1.0.20240516",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/assertpy.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['assertpy-stubs'],
      package_data={'assertpy-stubs': ['__init__.pyi', 'assertpy.pyi', 'base.pyi', 'collection.pyi', 'contains.pyi', 'date.pyi', 'dict.pyi', 'dynamic.pyi', 'exception.pyi', 'extracting.pyi', 'file.pyi', 'helpers.pyi', 'numeric.pyi', 'snapshot.pyi', 'string.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

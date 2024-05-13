# Smile test as python package 

## CI/CD

A CI automatically runs tests on each commits.

The stages are:

-  `build`: Build the python package and save it as artifact.
-  `test`: Run a docker container and install the locally built package. Run tests on 2 modules. 1 test is excepted to pass and 1 test is excepted to fail.

- `push`: Push the package to pypi is automaticaly done when a tag is pushed.

## Usage

The file `.env` must contain the following variables:

```
ODOO_VER=<x.x>
BASE_IMAGE_REF=<full_image_name>
```

Those variables must match the version for which the package is built.

Create a branch for each Odoo major version.

## Build

Create a tag for each version of the package.

You should not overwrite a tag. The format of the tag is `x.x.x` where the first `x` is the major version of Odoo.

Example:

14.1.5 is a package for Odoo 14.0.
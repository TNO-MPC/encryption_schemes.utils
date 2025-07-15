# TNO PET Lab - secure Multi-Party Computation (MPC) - Encryption Schemes - Utils

Useful functionality for implementing encryption schemes.

### PET Lab

The TNO PET Lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of PET solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed PET functionalities to boost the development of new protocols and solutions.

The package `tno.mpc.encryption_schemes.utils` is part of the [TNO Python Toolbox](https://github.com/TNO-PET).

_Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws._  
_This implementation of cryptographic software has not been audited. Use at your own risk._

## Documentation

Documentation of the `tno.mpc.encryption_schemes.utils` package can be found
[here](https://docs.pet.tno.nl/mpc/encryption_schemes/utils/0.15.0).

## Install

Easily install the `tno.mpc.encryption_schemes.utils` package using `pip`:

```console
$ python -m pip install tno.mpc.encryption_schemes.utils
```

_Note:_ If you are cloning the repository and wish to edit the source code, be
sure to install the package in editable mode:

```console
$ python -m pip install -e 'tno.mpc.encryption_schemes.utils'
```

If you wish to run the tests you can use:

```console
$ python -m pip install 'tno.mpc.encryption_schemes.utils[tests]'
```

_Note:_ A significant performance improvement can be achieved by installing the GMPY2 library.

```console
$ python -m pip install 'tno.mpc.encryption_schemes.utils[gmpy]'
```

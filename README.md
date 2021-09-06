# TNO MPC Lab - Encryption Schemes - Utils

The TNO MPC lab consists of generic software components, procedures, and functionalities developed and maintained on a regular basis to facilitate and aid in the development of MPC solutions. The lab is a cross-project initiative allowing us to integrate and reuse previously developed MPC functionalities to boost the development of new protocols and solutions.

The package tno.mpc.encryption_schemes.utils is part of the TNO Python Toolbox.

*Limitations in (end-)use: the content of this software package may solely be used for applications that comply with international export control laws.*

## Documentation

Documentation of the tno.mpc.encryption_schemes.utils package can be found [here](https://docs.mpc.tno.nl/encryption_schemes/utils/0.7.0).

## Install

Easily install the tno.mpc.encryption_schemes.utils package using pip:
```console
$ python -m pip install tno.mpc.encryption_schemes.utils
```

If you wish to use `numpy` you can use:
```console
$ python -m pip install 'tno.mpc.encryption_schemes.utils[numpy]'
```

If you wish to run the tests you can use:
```console
$ python -m pip install 'tno.mpc.encryption_schemes.utils[tests]'
```

### Note:
A significant performance improvement can be achieved by installing the GMPY2 library.
```console
$ python -m pip install 'tno.mpc.encryption_schemes.utils[gmpy]'
```

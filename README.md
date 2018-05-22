# Implementation of Order Revealing Encryption Scheme in Python

This Python module is an implementation of Order Revealing Encryption as described [in this paper](https://eprint.iacr.org/2016/612.pdf)
by Lewi et al. This implementation is a part of my Undergraduate Capstone Project at AUA.

The module contains both left and right encryption functions and the comparison function.
There's also an interface, which simulates an encrypted database with some basic functionality.

This module has two dependencies, namely [PyCryptoDome](https://github.com/Legrandin/pycryptodome) (for implementation of AES and SHA256)
and [NumPy](https://github.com/numpy/numpy), which can be installed using `pip`.
```
pip install numpy
pip install pycryptodome
```

To run the code, type the following in terminal: 

```
python ore_crypto.py
```

The list of available commands can be found in the Results section [here]().

File `keys.txt` contains a pickle of three randomly generated 16-byte bytestrings. The first two are the master key, the third is the 
initial vector for AES. It can be replaced with any file corresponding to the mentioned convention.


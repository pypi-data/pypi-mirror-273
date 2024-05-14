In Progress...

# Algorithms

## Encryption Algorithms

Fernet - Cryptographys algorithm that contains "symmetric ciphers, message digests, and key derivation functions" (pypi.org), this is pretty basic encryption.<br />
AES256 - It is the "current encryption standard" (idera.com), it can slow down slower processors but should be fine on most systems.<br />
RSA - It uses a pair of keys (public and private) to encrypt data. It encrypts the data with the public key, but the data can only be unencrypted with the private key.<br />
ECC - Elliptic-curve cryptography is an approach to public-key cryptography based on the algebraic structure of elliptic curves over finite fields.<br />
XOR - XOR algorithm of encryption and decryption converts the plain text in the format ASCII bytes and uses XOR procedure to convert it to a specified byte.<br />
Ascii - A custom Ascii scrambler that I made. It is not the most secure so I wouldn't recommend using it alone, but using it in combination with some other methods provided by this package removes the possibility of the same thing being created.<br /><br />

## Hashing Algorithms

SHA - Secure Hash Algorithm, used for cryptographic security. Cryptographic hash algorithms produce irreversible and unique hashes. The larger the number of possible hashes, the smaller the chance that two values will create the same hash. The higher number sha means more unique hashes.<br />
Shake - SHAKE encryption algorithm is a method for enforcing mathematic tolerances, and uses alot of math operations to find slight drifts.<br />
Blake - Blake is an improved version of SHA-3 optimized for 64 bit platforms.<br /><br />

This is a very simple library that I made for one of my projects, so there might be bugs please report these in the github issues. Although it might be simple it is pretty powerful.<br />

**WARNING** Don't delete the .key files or you cant unencrypt the data that you have encrypted with that key.<br />

# Information

[![Python](https://img.shields.io/pypi/pyversions/easyencryption.svg)](https://pypi.python.org/pypi/easyencryption)
[![PyPi](https://img.shields.io/pypi/v/easyencryption.svg)](https://pypi.org/project/easyencryption)

# Downloads

[![Downloads](https://pepy.tech/badge/easyencryption)](https://pepy.tech/project/easyencryption)
[![Downloads](https://pepy.tech/badge/easyencryption/month)](https://pepy.tech/project/easyencryption)
[![Downloads](https://pepy.tech/badge/easyencryption/week)](https://pepy.tech/project/easyencryption)
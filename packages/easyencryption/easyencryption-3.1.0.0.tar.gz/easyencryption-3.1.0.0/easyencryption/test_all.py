import asyncio
import pytest
pytest_plugins = ('pytest_asyncio',)

from .aes import aesencrypt, aesdecrypt

teststr = "TestString"

@pytest.mark.asyncio
async def test_aes():
      estr = await aesencrypt(teststr)
      dstr = await aesdecrypt(estr)
      if dstr != teststr:
            raise Exception("AES check failed")
      else:
            return dstr == teststr

from .ascii import asciiencrypt, asciidecrypt

@pytest.mark.asyncio
async def test_ascii():
      estr = await asciiencrypt(teststr)
      dstr = await asciidecrypt(estr)
      if dstr != teststr:
            raise Exception("ASCII check failed")
      else:
            return dstr == teststr

from .blake import blakeencrypt, blakecheck

@pytest.mark.asyncio
async def test_blake():
      estr = await blakeencrypt(teststr)
      dstr = await blakecheck(teststr, estr)
      if not dstr:
            raise Exception("Blake check failed")
      else:
            return dstr == teststr

from .fernet import fernetencrypt, fernetdecrypt

@pytest.mark.asyncio
async def test_fernet():
      estr = await fernetencrypt(teststr)
      dstr = await fernetdecrypt(estr)
      if dstr != teststr:
            raise Exception("Fernet check failed")
      else:
            return dstr == teststr
      
from .fernet import multifernetencrypt, multifernetdecrypt

@pytest.mark.asyncio
async def test_multifernet():
      estr = await multifernetencrypt(teststr)
      dstr = await multifernetdecrypt(estr)
      if dstr != teststr:
            raise Exception("MultiFernet check failed")
      else:
            return dstr == teststr
      
from .rsa import rsaencrypt, rsadecrypt

@pytest.mark.asyncio
async def test_rsa():
      estr = await rsaencrypt(teststr)
      dstr = await rsadecrypt(estr)
      if dstr != teststr:
            raise Exception("RSA check failed")
      else:
            return dstr == teststr
      
from .sha import sha224encrypt, sha224check

@pytest.mark.asyncio
async def test_sha224():
      estr = await sha224encrypt(teststr)
      dstr = await sha224check(teststr, estr)
      if not dstr:
            raise Exception("SHA224 check failed")
      else:
            return dstr == teststr

from .sha import sha256encrypt, sha256check

@pytest.mark.asyncio
async def test_sha256():
      estr = await sha256encrypt(teststr)
      dstr = await sha256check(teststr, estr)
      if not dstr:
            raise Exception("SHA256 check failed")
      else:
            return dstr == teststr

from .sha import sha384encrypt, sha384check

@pytest.mark.asyncio
async def test_sha384():
      estr = await sha384encrypt(teststr)
      dstr = await sha384check(teststr, estr)
      if not dstr:
            raise Exception("SHA384 check failed")
      else:
            return dstr == teststr

from .sha import sha512encrypt, sha512check

@pytest.mark.asyncio
async def test_sha512():
      estr = await sha512encrypt(teststr)
      dstr = await sha512check(teststr, estr)
      if not dstr:
            raise Exception("SHA512 check failed")
      else:
            return dstr == teststr

from .shake import shake128encrypt, shake128check

@pytest.mark.asyncio
async def test_shake128():
      estr = await shake128encrypt(teststr)
      dstr = await shake128check(teststr, estr)
      if not dstr:
            raise Exception("SHAKE128 check failed")
      else:
            return dstr == teststr

from .shake import shake256encrypt, shake256check

@pytest.mark.asyncio
async def test_shake256():
      estr = await shake256encrypt(teststr)
      dstr = await shake256check(teststr, estr)
      if not dstr:
            raise Exception("SHAKE256 check failed")
      else:
            return dstr == teststr
      
from .xor import xorencrypt, xordecrypt

@pytest.mark.asyncio
async def test_xor():
      estr = await xorencrypt(teststr)
      dstr = await xordecrypt(estr)
      if dstr != teststr:
            raise Exception("XOR check failed")
      else:
            return dstr == teststr


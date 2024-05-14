import hashlib, codecs, secrets

async def gensalt():
    generated_salt = secrets.token_hex(32)
    with open("shasalteasyencryption.key", "wb") as key_file:
        key_file.write(codecs.encode(generated_salt))
    return generated_salt

async def callsalt():
  try:
    key = open("shasalteasyencryption.key", "rb").read()
    if str(key) == "b''":
      await gensalt()
      key = open("shasalteasyencryption.key", "rb").read()
    return key
  except:
    await gensalt()
    key = open("shasalteasyencryption.key", "rb").read()
    return key

async def sha224encrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.sha3_224(codecs.encode(salt + string))
    return hashing.hexdigest()

async def sha224check(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.sha3_224(codecs.encode(salt + string))
    return strhashing.hexdigest() == bytes

async def sha256encrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.sha3_256(codecs.encode(salt + string))
    return hashing.hexdigest()

async def sha256check(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.sha3_256(codecs.encode(salt + string))
    return strhashing.hexdigest() == bytes

async def sha384encrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.sha3_384(codecs.encode(salt + string))
    return hashing.hexdigest()

async def sha384check(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.sha3_384(codecs.encode(salt + string))
    return strhashing.hexdigest() == bytes

async def sha512encrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.sha3_512(codecs.encode(salt + string))
    return hashing.hexdigest()

async def sha512check(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.sha3_512(codecs.encode(salt + string))
    return strhashing.hexdigest() == bytes
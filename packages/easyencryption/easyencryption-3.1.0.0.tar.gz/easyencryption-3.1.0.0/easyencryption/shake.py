import hashlib, codecs, secrets

async def gensalt():
    generated_salt = secrets.token_hex(32)
    with open("shakesalteasyencryption.key", "wb") as key_file:
        key_file.write(codecs.encode(generated_salt))
    return generated_salt

async def callsalt():
  try:
    key = open("shakesalteasyencryption.key", "rb").read()
    if str(key) == "b''":
      await gensalt()
      key = open("shakesalteasyencryption.key", "rb").read()
    return key
  except:
    await gensalt()
    key = open("shakesalteasyencryption.key", "rb").read()
    return key

async def shake128encrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.shake_128(codecs.encode(salt + string))
    return hashing.hexdigest(16)

async def shake128check(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.shake_128(codecs.encode(salt + string))
    return strhashing.hexdigest(16) == bytes

async def shake256encrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.shake_256(codecs.encode(salt + string))
    return hashing.hexdigest(32)

async def shake256check(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.shake_256(codecs.encode(salt + string))
    return strhashing.hexdigest(32) == bytes

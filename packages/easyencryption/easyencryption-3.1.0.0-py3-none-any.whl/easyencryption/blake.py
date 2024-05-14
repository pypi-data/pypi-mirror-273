import hashlib, codecs, secrets

async def gensalt():
    generated_salt = secrets.token_hex(32)
    with open("blakesalteasyencryption.key", "wb") as key_file:
        key_file.write(codecs.encode(generated_salt))
    return generated_salt

async def callsalt():
  try:
    key = open("blakesalteasyencryption.key", "rb").read()
    if str(key) == "b''":
      await gensalt()
      key = open("blakesalteasyencryption.key", "rb").read()
    return key
  except:
    await gensalt()
    key = open("blakesalteasyencryption.key", "rb").read()
    return key

async def blakeencrypt(string:str):
    salt = codecs.decode(await callsalt())
    hashing = hashlib.blake2b(codecs.encode(salt + string))
    return hashing.hexdigest()

async def blakecheck(string:str, bytes:bytes):
    salt = codecs.decode(await callsalt())
    strhashing = hashlib.blake2b(codecs.encode(salt + string))
    return strhashing.hexdigest() == bytes

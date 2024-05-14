import base64, random, string, codecs, itertools

async def genkey():
  key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
  with open("xoreasyencryption.key", "wb") as key_file:
    key_file.write(codecs.encode(key))
  return key
  
async def callkey():
  try:
    key = codecs.decode(open("xoreasyencryption.key", "rb").read())
    if str(key) == "b''":
      await genkey()
      key = codecs.decode(open("xoreasyencryption.key", "rb").read())
    return key
  except:
    await genkey()
    key = codecs.decode(open("xoreasyencryption.key", "rb").read())
    return key

async def crypt(data:str, key=None, encode = False, decode = False):
   if key == None:
     key = await callkey()
   if decode:
      data = base64.b64decode(data)
      data = data.decode('ascii')
   xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, itertools.cycle(key)))
   
   if encode:
      xored = xored.encode('ascii')
      return base64.b64encode(xored).strip()
   return xored

async def xorencrypt(slogan:str):
      key = await callkey()
      return await crypt(slogan, key=key, encode = True)

async def xordecrypt(coded_slogan:bytes):
      key = await callkey()
      return await crypt(coded_slogan, key=key, decode = True)
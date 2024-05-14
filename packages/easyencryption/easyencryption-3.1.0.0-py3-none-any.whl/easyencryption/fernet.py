import os, codecs
from cryptography.fernet import Fernet, MultiFernet

async def genkey():
  key = Fernet.generate_key()
  with open("symeasyencryption.key", "wb") as key_file:
    key_file.write(key)
  return key

async def regenkey():
  if os.path.exists("symeasyencryption.key"):
    os.remove("symeasyencryption.key")
  await genkey()
  
async def callkey():
  try:
    key = open("symeasyencryption.key", "rb").read()
    if str(key) == "b''":
      await genkey()
      key = open("symeasyencryption.key", "rb").read()
    return key
  except:
    await genkey()
    key = open("symeasyencryption.key", "rb").read()
    return key
  
async def genkeys():
  key1 = Fernet.generate_key()
  with open("sym1easyencryption.key", "wb") as key_file:
    key_file.write(key1)
  key2 = Fernet.generate_key()
  with open("sym2easyencryption.key", "wb") as key_file:
    key_file.write(key1)
  key3 = Fernet.generate_key()
  with open("sym3easyencryption.key", "wb") as key_file:
    key_file.write(key1)
  return [key1, key2, key3]

async def callkeys():
  try:
    key1 = open("sym1easyencryption.key", "rb").read()
    if str(key1) == "b''":
      await genkeys()
      key1 = open("sym1easyencryption.key", "rb").read()
  except:
    await genkeys()
    key1 = open("sym1easyencryption.key", "rb").read()
  try:
    key2 = open("sym2easyencryption.key", "rb").read()
    if str(key2) == "b''":
      await genkeys()
      key2 = open("sym2easyencryption.key", "rb").read()
  except:
    await genkeys()
    key2 = open("sym2easyencryption.key", "rb").read()
  try:
    key3 = open("sym3easyencryption.key", "rb").read()
    if str(key3) == "b''":
      await genkeys()
      key3 = open("sym3easyencryption.key", "rb").read()
  except:
    await genkeys()
    key3 = open("sym3easyencryption.key", "rb").read()
  return [key1, key2, key3]
  
async def fernetencrypt(slogan:str):
  key = await callkey()
  slogan = slogan.encode()
  a = Fernet(key)
  coded_slogan = a.encrypt(slogan)
  return coded_slogan

async def fernetdecrypt(coded_slogan:bytes):
  key = await callkey()
  b = Fernet(key)
  decoded_slogan = codecs.decode(b.decrypt(coded_slogan))
  return decoded_slogan

async def multifernetencrypt(slogan:str):
  keys = await callkeys()
  slogan = slogan.encode()
  a = Fernet(keys[0])
  b = Fernet(keys[1])
  c = Fernet(keys[2])
  f = MultiFernet([a, b, c])
  coded_slogan = f.encrypt(slogan)
  return coded_slogan

async def multifernetdecrypt(coded_slogan:bytes):
  keys = await callkeys()
  a = Fernet(keys[0])
  b = Fernet(keys[1])
  c = Fernet(keys[2])
  f = MultiFernet([c, b, a])
  rotated = f.rotate(coded_slogan)
  decoded_slogan = codecs.decode(b.decrypt(coded_slogan))
  return decoded_slogan

  
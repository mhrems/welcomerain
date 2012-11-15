from tomcrypt import cipher

print cipher.names
print cipher.modes

print cipher.noekeon.block_size
print cipher.noekeon.min_key_size
print cipher.noekeon.max_key_size

print cipher.noekeon

encryptor =cipher.noekeon(key='0000000000000001', mode='ecb')

encrypted = encryptor.encrypt('sample')

print encrypted 
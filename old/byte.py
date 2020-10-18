ustring = 'A unicode string'
print(type(ustring))
bstring = b'bstring'
print(type(bstring))
new_bstring = ustring.encode()
type(new_bstring)

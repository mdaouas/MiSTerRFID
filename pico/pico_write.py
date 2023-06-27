from mfrc522 import MFRC522

'''
BE AWARE that sectors(3,7,11,15,...,63) are access block.
if you want to change  (sector % 4) == 3 you should
know how keys and permission work!
'''


CORE = 'Gameboy' # NES SNES ...
MEDIA = 'usb0' # fat usb0 usb1 usb2 ...
ROM = 'GB/L/Legend of Zelda, The - Link\'\\\'\'s Awakening (France).gb' # relative to default core rom folder

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

#reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=3)

reader = MFRC522(spi_id=0,sck=18,miso=16,mosi=19,cs=17,rst=28)

print("")
print("Please place card on reader")
print("")

key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

try:
    while True:

        (stat, tag_type) = reader.request(reader.REQIDL)

        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                print(uid)
                print("Card detected %s" % uidToString(uid))
                #reader.MFRC522_DumpClassic1K(uid,keyA=key)
                print("Test ! writing sector 2, block 0 (absolute block(8)")
                print("with [ 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 ]")
                absoluteBlocks = []
                for i in range(1,63):
                    if ((i+1) % 4) != 0:
                        absoluteBlocks.append(i)
                print(absoluteBlocks)
                #absoluteBlock=8
                
                data = (
                    bytes("'%s'" % CORE, "ascii")
                    + b" "
                    + bytes("'%s'" % ROM, "ascii")
                    + b" "
                    + bytes("'%s'" % uidToString(uid), "ascii")
                )
                
                data = data + b"\0" * (max(0, 16 - len(data) % 16))
                chunks = [data[i : i + 16] for i in range(0, len(data), 16)]
                print(chunks)
                
                value=bytes("MiSTer FPGA",'ascii')
                value = value + b"\0" * max(0, 16 - len(value))
                blankData = 16 * [0]
                #for bytes in str_1_encoded:
                #    value.append(bytes)
                #for i in range(16):
                #    value.append(i)
                for idx in range(0,len(absoluteBlocks)):
                    status = reader.auth(reader.AUTHENT1A, absoluteBlocks[idx], key, uid)
                    if status == reader.OK:
                        print(blankData if len(chunks) - 1 < idx  else chunks[min(idx,len(chunks)-1)])
                        status = reader.write(absoluteBlocks[idx],blankData if len(chunks) - 1 < idx  else chunks[min(idx,len(chunks)-1)])
                        print("OK {:02d}".format(absoluteBlocks[idx]))
                        #if status == reader.OK:
                        #    reader.MFRC522_DumpClassic1K(uid,keyA=key)
                        #else:
                        #    print("unable to write")
                    else:
                        print("Authentication error for writing")
                        break
                print("done")
except KeyboardInterrupt:
    print("Bye")

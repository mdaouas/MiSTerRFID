from mfrc522 import MFRC522
import utime


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



PreviousCard = [0]

try:
    while True:

        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        #print('request stat:',stat,' tag_type:',tag_type)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue
            if stat == reader.OK:
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
                defaultKey = [255,255,255,255,255,255]
                blankData = 16 *[0]
                #reader.MFRC522_DumpClassic1K(uid, Start=0, End=64, keyA=defaultKey)
                #print("Done")
                command = []
                absoluteBlocks = []
                for i in range(1,63):
                    if ((i+1) % 4) != 0:
                        absoluteBlocks.append(i)
                for absoluteBlock in absoluteBlocks:
                    status = reader.authKeys(uid,absoluteBlock,keyA=defaultKey)
                    status, data  = reader.read(absoluteBlock)
                    command = command + data
                    prev = -1
                    for i in data:
                        if prev + i == 0:
                            break
                        prev = i
                    for value in data:
                        print("{:02X} ".format(value),end="")
                    print("  ",end="")
                    for value in data:
                        if (value > 0x20) and (value < 0x7f):
                            print(chr(value),end="")
                        else:
                            print('.',end="")
                    print("")
                    if prev == 0:
                        break
                print("Done")
                print(bytes(bytearray(command)).decode('ascii'))
                PreviousCard = uid
            else:
                pass
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    pass

from mfrc522 import MFRC522 # https://github.com/danjperron/micropython-mfrc522
import utime

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
                  
reader = MFRC522(spi_id=0,sck=18,miso=16,mosi=19,cs=17,rst=28)

PreviousCard = [0]

while True:

    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)

    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if uid == PreviousCard:
            continue
        if stat == reader.OK:
            defaultKey = [255,255,255,255,255,255]
            blankData = 16 *[0]
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
                if prev == 0:
                    break
            print(". rfid_process.sh %s" % bytes(bytearray(command)).decode('ascii'))
            PreviousCard = uid                        
        else:
            pass                        
    else:
        PreviousCard=[0]
    utime.sleep_ms(50)                           

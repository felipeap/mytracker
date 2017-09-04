import binascii
import crcmod.predefined

def remove_byteStuf(data):
    pacote = binascii.hexlify(data)
    pacote = pacote[2: len(pacote) - 2]
    novo_pacote = ""

    iteration = iter(range(0, pacote.__len__(), 2))
    for x in iteration:
        if(pacote[x:(x+2)]) == '10':
            if ( pacote[x + 2:(x + 4)])  == '21':
                novo_pacote = novo_pacote + '01'

            elif (pacote[x + 2:(x + 4)]) == '24':
                novo_pacote = novo_pacote + '04'

            elif (pacote[x + 2:(x + 4)]) == '30':
                novo_pacote = novo_pacote + '10'

            elif (pacote[x + 2:(x + 4)]) == '31':
                novo_pacote = novo_pacote + '11'

            elif (pacote[x + 2:(x + 4)]) == '33':
                novo_pacote = novo_pacote + '13'
            next(iteration)
        else:
            novo_pacote = novo_pacote + pacote[x:(x+2)]
    return binascii.unhexlify(novo_pacote)

#CRC_CCITT
def calcula_CRC(pacote):
    # pacote = binascii.unhexlify(pacote)
    crc_received = crc_received.upper()
    crc16 = crcmod.predefined.Crc('xmodem')
    crc16.update(pacote)
    inverteCRC = crc16.hexdigest()
    i = 4
    CRC = ''
    while (i > 0):
        CRC = CRC + inverteCRC[i - 2:i]
        i = i - 2

    return CRC
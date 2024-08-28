from one_time_pad_machine import one_time_pad_machine as otpm


def main():
    lang = 0
    encode = bool(input('0: Decode\n1: Encode\nEnter Selection: '))
    if encode:
        lang = str(input('1: octen,\n2: harran\nEnter Selection: '))
    msg = input('Enter Message: ')
    recip = input('Enter Recipient Code: ')
    kblock = input('Enter Key Block: ')
    otp = input('Enter Pad Segment: ')
    if lang:
        print(otpm(lang=lang, encode=encode, message=msg, recip=recip, kblock=kblock, otp=otp))
    else:
        print(otpm(encode=encode, message=msg, recip=recip, kblock=kblock,otp=otp))

main()

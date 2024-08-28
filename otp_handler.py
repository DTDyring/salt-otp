""" These only handle numbers and, as a result, do not provide anything but the pad-enciphered/pad-deciphered message.
They do not take in or put out letters or words directly."""


def otp_handler(message, /, encode=True, recip='', otp='', kblock=''):
    if not recip and not kblock and not otp and encode:
        recipient, key_block, one_time_pad = otp_receiver()
        return ''.join([recipient, key_block, otp_encoder(message, one_time_pad)])
    if encode:
        recipient, key_block, one_time_pad = otp_receiver(recip, otp, kblock)
        encoded_message, otp_segment = otp_encoder(message, one_time_pad)
        return ''.join([recipient, key_block, encoded_message]), otp_segment
    if not encode:
        one_time_pad = ''.join(otp.split())
        decoded_message = otp_decoder(message, one_time_pad)
        return decoded_message


def otp_receiver(msg_tgt='', otp='', key_block=''):
    if not msg_tgt:
        msg_tgt = input('Please provide the message recipient: ')
    if not otp:
        otp = input('Please provide the one-time pad: ')
    if not key_block:
        key_block = input('Please provide the key block: ')
    # removes the key block from the otp if present
    if key_block in otp:
        otp = otp.removeprefix(otp[0:(otp.find(key_block))+(len(key_block))])
    # collapses all whitespace that might be present in the otp
    otp = ''.join(otp.split())
    return msg_tgt, key_block, otp


def otp_encoder(message, otp_segment):
    encoded_segment = ''
    # cut remainder of otp so only the necessary pieces remain
    otp_segment = otp_segment[:len(message)]
    idx = 0
    for num in message:
        if int(num) - int(otp_segment[idx]) < 0:
            new_num = int(num)+10
            new_num = new_num-int(otp_segment[idx])
            encoded_segment += str(new_num)
        else:
            encoded_segment += str(int(num)-int(otp_segment[idx]))
        idx += 1
    return encoded_segment, otp_segment


def otp_decoder(encoded_message, otp_segment):
    decoded_segment = ''
    idx = 0
    for num in encoded_message:
        new_num = int(num) + int(otp_segment[idx])
        if new_num >= 10:
            new_num -= 10
        decoded_segment += str(new_num)
        idx += 1
    return decoded_segment

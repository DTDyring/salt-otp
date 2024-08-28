from message_converter import message_encoder
from otp_handler import otp_handler


def one_time_pad_machine(lang=1, encode=True, message='', recip='', otp='', kblock=''):
    if encode and message:
        converted_message = ''
        if lang == 1:
            converted_message = message_encoder(message, 'octen')
        elif lang == 2:
            converted_message = message_encoder(message, 'harran')
        return otp_handler(converted_message, encode=encode, recip=recip, otp=otp, kblock=kblock)
    elif message and not encode:
            return otp_handler(message, encode=encode, otp=otp)
    else:
        return "Error: missing args! How did you even get this far?"

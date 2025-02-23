from message_converter import OTP_Encoder
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


# TODO: this
class One_Time_Pad_Machine:
    """Machine for converting a message to its encoded format"""

    def __init__(self):
        self.octen_encoder = OTP_Encoder('octen')
        self.harran_encoder = OTP_Encoder('harran')

    def begin_OTP_input(self):
        pass


# TODO: this
class OTP_Input_Handler:

    def __init__(self):
        pass

    def begin_otp_intake(self, message, recipient='', otp='', key_block=''):
        pass

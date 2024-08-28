import unittest
from message_converter import message_encoder, codebook_converter, table_converter,\
    codebook_strip, is_trailing_poly, ends_in_special_character,\
    converted_string_joiner, spec_stripper, segment_replacer_loop
from otp_handler import otp_receiver, otp_encoder, otp_decoder, otp_handler
from one_time_pad_machine import one_time_pad_machine


#############################
#                           #
#   Message Encoder Tests   #
#                           #
#############################

class Message_Encoder_Tests(unittest.TestCase):

    def test_spec_stripper(self):
        test_words = ['abc', '.abc.', ':abc:', '`abc`', '/abc/', '+abc+', '-abc-', '=abc=', '.:`/+-=abc=-+/`:.']
        correct_output = ['abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc', 'abc']
        output = []
        for word in test_words:
            output.append(spec_stripper(word))
        self.assertEqual(correct_output, output)


    def test_octen_table_converter_with_codebook_word_at_start(self):
        test_string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.".casefold()
        test_indices_list = [0, 1, 2, 5, 6, 9]
        test_lang = 'octen'
        correct_string_list_output = ['', '', '', '71186391', '47877796728372', '', '', '777282821272',
                                      '817247274798391', '', '22244491']
        self.assertEqual(correct_string_list_output, table_converter(test_string, test_indices_list, test_lang))


    def test_harran_table_converter_with_codebook_word_at_start(self):
        test_string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.".casefold()
        test_indices_list = [0, 1, 2, 5, 6, 9]
        test_lang = 'harran'
        correct_string_list_output = ['', '', '', '535066091', '526160625954354', '', '', '60546464505654',
                                      '63545254462391', '', '224491']
        self.assertEqual(correct_string_list_output, table_converter(test_string, test_indices_list, test_lang))


    def test_octen_table_converter_without_codebook_word_at_start(self):
        test_string = 'Weather report: Clear sky. 15 degrees. Operation Tulip commence at 0630.'.casefold()
        test_indices_list = [6]
        test_lang = 'octen'
        correct_string_list_output = ['867218357281', '81727978818392', '4672181', '82768891', '111555',
                                      '717228172728291', '', '838467479', '4787777723472', '183', '00066633300091']
        self.assertEqual(correct_string_list_output, table_converter(test_string, test_indices_list, test_lang))


    def test_harran_table_converter_without_codebook_word_at_start(self):
        test_string = 'Weather report: Clear sky. 15 degrees. Operation Tulip commence at 0630.'.casefold()
        test_indices_list = [6]
        test_lang = 'harran'
        correct_string_list_output = ['6654503575463', '6354626163392', '5259545063', '64586891', '1155',
                                      '5354566354546491', '', '36559462', '526160605405254', '503', '0066330091']
        self.assertEqual(correct_string_list_output, table_converter(test_string, test_indices_list, test_lang))


    def test_octen_codebook_converter_with_codebook_word_at_start(self):
        test_string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.".casefold()
        test_lang = 'octen'
        correct_string_list_output = ['434', '563', '', 'dawn.', 'complete', '43491', '065', 'message', 'receipt.',
                                      '01192', '24.']
        correct_indices_list_output = [0, 1, 2, 5, 6, 9]
        self.assertEqual((correct_string_list_output, correct_indices_list_output),
                         codebook_converter(test_string, test_lang))


    def test_harran_codebook_converter_with_codebook_word_at_start(self):
        test_string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.".casefold()
        test_lang = 'harran'
        correct_string_list_output = ['332', '377', '', 'dawn.', 'complete', '33291', '761', 'message', 'receipt.',
                                      '43292', '24.']
        correct_indices_list_output = [0, 1, 2, 5, 6, 9]
        self.assertEqual((correct_string_list_output, correct_indices_list_output),
                         codebook_converter(test_string, test_lang))


    def test_octen_codebook_converter_without_codebook_word_at_start(self):
        test_string = 'Weather report: Clear sky. 15 degrees. Operation Tulip commence at 0630.'.casefold()
        test_lang = 'octen'
        correct_string_list_output = ['weather', 'report:', 'clear', 'sky.', '15', 'degrees.', '566', 'tulip',
                                      'commence', 'at', '0630.']
        correct_indices_list_output = [6]
        self.assertEqual((correct_string_list_output, correct_indices_list_output),
                         codebook_converter(test_string, test_lang))


    def test_harran_codebook_converter_without_codebook_word_at_start(self):
        test_string = 'Weather report: Clear sky. 15 degrees. Operation Tulip commence at 0630.'.casefold()
        test_lang = 'harran'
        correct_string_list_output = ['weather', 'report:', 'clear', 'sky.', '15', 'degrees.', '335', 'tulip',
                                      'commence', 'at', '0630.']
        correct_indices_list_output = [6]
        self.assertEqual((correct_string_list_output, correct_indices_list_output),
                         codebook_converter(test_string, test_lang))


    def test_codebook_strip(self):
        # convertible word
        test_word_1 = "mission."
        test_book = {'mission': '434'}
        correct_conversion = "434"
        self.assertEqual(correct_conversion, codebook_strip(test_word_1, test_book))
        # non-convertible word
        test_word_2 = "dawn."
        self.assertFalse(codebook_strip(test_word_2, test_book))


    def test_codebook_caught_poly(self):
        poly_words = ["begins at"]
        # convertible words
        test_word_1 = "begins"
        test_word_2 = "at"
        self.assertTrue(is_trailing_poly(test_word_2, test_word_1, poly_words))
        # convertible words with special character
        test_word_3 = "begins"
        test_word_4 = "at:"
        self.assertTrue(is_trailing_poly(test_word_4, test_word_3, poly_words))
        # non-convertible words
        test_word_5 = "home"
        test_word_6 = "alone"
        self.assertFalse(is_trailing_poly(test_word_6, test_word_5, poly_words))


    def test_ends_in_special_character(self):
        test_words = ['tank', 'tank.', 'tank:', 'tank`', 'tank/', 'tank+', 'tank-', 'tank=']
        self.assertFalse(ends_in_special_character(test_words[0]))
        for i in range(1, len(test_words)):
            self.assertTrue(test_words[i])


    def test_converted_string_joiner(self):
        # test string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24."
        test_codebook_words = ['434', '563', '', 'dawn.', 'complete', '43491', '065', 'message', 'receipt.', '01192', '24.']
        test_converted_words = ['', '', '', '71186391', '47877796728372', '', '', '777282821272',
                                '817247274798391', '', '22244491']
        correct_string = '434995639971186391994787779672837299434919906599' \
                         '7772828212729981724727479839199011929922244491'
        self.assertEqual(correct_string, converted_string_joiner(test_codebook_words, test_converted_words))


    def test_message_encoder(self):
        test_string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24."
        correct_string = '434995639971186391994787779672837299434919906599' \
                         '7772828212729981724727479839199011929922244491'
        self.assertEqual(correct_string, message_encoder(test_string))

    # TODO: fix all following decoder tests
    # deprecated
    # def test_octen_clean_string_spaces(self):
    #     # original string: Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.
    #     test_string = '4349956399711863919947877796728372994349199065997772828212729981724727479839199011929922244491'
    #     test_lang = 'octen'
    #     correct_string = "434 563 71186391 47877796728372 43491 065 777282821272 817247274798391 01192 22244491"
    #     correct_spcs = [3, 8, 18, 34, 41, 46, 60, 77, 84]
    #     self.assertEqual((correct_string, correct_spcs), clean_string_spaces(test_string, test_lang))
    #
    #
    # # deprecated
    # def test_harran_clean_string_spaces(self):
    #     # original string: Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.
    #     test_string = '3320003770005350609100052616062595435433291000761000605464645056540006354525446239143292000224491'
    #     test_lang = 'harran'
    #     correct_string = '332 377 53506091 52616062595435433291 761 60546464505654 6354525446239143292 224491'
    #     correct_spcs = [3, 9, 20, 43, 49, 66, 88]
    #     self.assertEqual((correct_string, correct_spcs), clean_string_spaces(test_string, test_lang))
    #
    #
    # # deprecated
    # def test_octen_get_codebook_string(self):
    #     # original string: Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24.
    #     test_string = '434995639971186391994787779672837299434919906599' \
    #                   '7772828212729981724727479839199011929922244491'
    #     test_lang = 'octen'
    #     correct_string = 'mission99begins at9971186391994787779672837299mission9199verify' \
    #                      '997772828212729981724727479839199infantry92992codebook4491'
    #     correct_words = [0, 5, 36, 43, 79, 87]
    #     self.assertEqual((correct_string, correct_words), get_codebook_string(test_string, test_lang))
    #
    #
    # # deprecated
    # def test_harran_get_codebook_string(self):
    #     # original string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24."
    #     test_string = '3320003770005350609100052616062595435433291' \
    #                   '000761000605464645056540006354525446239143292000224491'
    #     test_lang = 'harran'
    #     correct_string = 'mission000begins at00053506091000526160625954354mission91' \
    #                      '000verify0006054646450565400063545254462391infantry92000224491'
    #     correct_words = [0, 6, 38, 46, 83]
    #     self.assertEqual((correct_string, correct_words), get_codebook_string(test_string, test_lang))


    # TODO
    def test_segment_replacer_loop_no_sub_dict(self):
        test_string = '56591666501650497741716255165819481231321320'
        test_seg_len = 1
        test_keys = ['a','b','c','d','e','f','g']
        test_vals = ['0','1','2','3','4','5','6']
        correct_list = ['f','g','f','█','b','g','g','g','f','a','b','g','f','a','e','█','█','█','e','b','█','b','g','c',
                        'f','f','b','g','f','█','b','█','e','█','b','c','d','b','d','c','b','d','c','a']
        correct_dict = {}
        self.assertEqual((correct_list, correct_dict), segment_replacer_loop(test_string, test_seg_len, test_keys,
                                                                             test_vals))


    # TODO
    def test_segment_replacer_loop_with_sub_dict(self):
        test_string = '56591666501650497741716255165819481231321320'
        test_seg_len = 2
        test_keys = ['a', 'b', 'c', 'dd', 'ee', 'ff', 'gg']
        test_vals = ['56', '65', '50', '97', '49', '77', '94']
        correct_list = ['a','b','█','█','█','█','█','b','c','█','█','b','c','█','B','A','C','█','█','█','█','█','█','█',
                        '█','█','█','b','█','█','█','D','█','█','█','█','█','█','█','█','█','█','█','█']
        correct_dict = {'dd': 'A', 'ee': 'B', 'ff': 'C', 'gg': 'D'}
        self.assertEqual((correct_list, correct_dict),
                         segment_replacer_loop(test_string, test_seg_len, test_keys, test_vals))


    # TODO
    def test_message_decoder_octen(self):
        pass


    # TODO
    def test_message_decoder_harran(self):
        pass


#####################################
#                                   #
#   One-Time Pad Handler Tests      #
#                                   #
#####################################

class One_Time_Pad_Handler_Tests(unittest.TestCase):

    def test_otp_receiver(self):
        test_msg_tgt = "351"
        test_string = "55124\t35697\t31205\t42310\t95230\t92049"
        test_key_block = "31205"
        correct_output_string = "423109523092049"
        correct_output = (test_msg_tgt, test_key_block, correct_output_string)
        self.assertEqual(correct_output,otp_receiver(msg_tgt=test_msg_tgt, otp=test_string, key_block=test_key_block))


    def test_otp_encoder(self):
        test_message = "7165496354132457812002134695213451789152"
        test_otp = "5314790124637581243602849517633021464721621348521761590"
        correct_output = "2851706230505976679400395188680430325431"
        correct_segment = "5314790124637581243602849517633021464721"
        self.assertEqual((correct_output, correct_segment), otp_encoder(test_message, test_otp))


    def test_otp_decoder(self):
        test_message = "2851706230505976679400395188680430325431"
        test_otp = "5314790124637581243602849517633021464721"
        correct_output = "7165496354132457812002134695213451789152"
        self.assertEqual(correct_output, otp_decoder(test_message, test_otp))


    def test_otp_handler(self):
        # test encoding
        test_message = "7165496354132457812002134695213451789152"
        test_recip = "132"
        test_kblock = "92144"
        test_otp = "64817\t32336\t92144\t53147\t90124\t63758\t12436\t02849\t51763\t30214\t64721\t62134\t85217\t61590"
        correct_output = "132921442851706230505976679400395188680430325431"
        correct_segment = "5314790124637581243602849517633021464721"
        self.assertEqual((correct_output, correct_segment),
                         otp_handler(test_message, recip=test_recip, otp=test_otp, kblock=test_kblock))
        # test decoding
        test_message = "2851706230505976679400395188680430325431"
        test_otp = "5314790124637581243602849517633021464721"
        correct_output = "7165496354132457812002134695213451789152"
        self.assertEqual(correct_output, otp_handler(test_message, encode=False, otp=test_otp))


#################################
#                               #
#   One-Time Pad Machine Tests  #
#                               #
#################################

class One_Time_Pad_Machine_Tests(unittest.TestCase):
    def test_one_time_pad_machine(self):
        # test encoding
        test_string = "Mission begins at dawn. Complete mission. Verify message receipt. Infantry: 24."
        test_recip = "132"
        test_otp = "51249221547965312513216554975320216894311147623006809690644468033513106487306003646076643684684" \
                   "483015555044916631216354972214"
        test_kblock = "79653"
        correct_string = "13279653319863574432433199836844668206607231448013562919442151867409938146012081557173167" \
                         "3628477740000"
        correct_segment = "1251321655497532021689431114762300680969064446803351310648730600364607664368468448301555" \
                          "504491"
        self.assertEqual((correct_string, correct_segment), one_time_pad_machine(message=test_string, recip=test_recip,
                                                                                 otp=test_otp, kblock=test_kblock))
        # test decoding
        test_string = "3198635744324331998368446682066072314480135629194421518674099381460120815571731673628477740000"
        test_otp = "1251321655497532021689431114762300680969064446803351310648730600364607664368468448301555504491"
        correct_string = "43499563997118639199478777967283729943491990659977728282127299817247274798391990119299222" \
                         "44491"
        self.assertEqual(correct_string, one_time_pad_machine(message=test_string, otp=test_otp, encode=False))



if __name__ == '__main__':
    unittest.main()

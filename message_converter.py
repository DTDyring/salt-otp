from conversion_tables_and_codebooks import octen_table, octen_codebook, harran_codebook, harran_table
from statistics import median


###########
#         #
# Encoder #
#         #
###########

def message_encoder(old_string, lang='octen'):
    """convert a text string to a string of numbers using a codebook and table
        old_string :argument the string to be converted
        lang :argument indicates which codebook and codetable to use"""
    old_string = old_string.casefold()
    # replace all words in string found in codebook with corresponding numbers
    codebook_words, book_indices = codebook_converter(old_string, lang)
    # replace all characters in string with corresponding numbers
    codetable_words = table_converter(old_string, book_indices, lang)
    # concatenate codebook and table forms to each other
    converted_string = converted_string_joiner(codebook_words, codetable_words)
    return converted_string


def codebook_converter(old_string, lang='octen') -> (list, list):
    """receives a string and converts words that appear in codebook to corresponding numbers and stores
        them in a list of strings. Also stores the index that those numbers appear in.
        returns the list of converted words (and unconverted words) and the list of indices
        old_string :argument the string to be converted
        lang :argument indicates which codebooks and codetable to use
        codebook_words :return list of words converted via codebook
        book_indices :return list of indices where codebook words begin in old_string"""
    # set up lang data:
    codebook = octen_codebook
    codetable = octen_table
    if lang == 'harran':
        codebook = harran_codebook
        codetable = harran_table
    # set up returns
    codebook_words = []
    book_indices = []
    current_index = 0
    # convert string to list
    string_words = old_string.split()
    # polymember words contained in codebook (NOT conversion table!)
    # TODO: this needs to derive from the codebook instead of magic value
    # I think this is working but I don't wanna test it because I'm lazy
    poly_words = []
    for key in list(codebook.keys()):
        if ' ' in key:
            poly_words.append(key)
    for word in string_words:
        # catch polymembers
        if current_index+1 < len(string_words) \
                and spec_stripper(word)+' '+spec_stripper(string_words[current_index+1]) in poly_words:
                coded_word = codebook[spec_stripper(word)+' '+spec_stripper(string_words[current_index + 1])]
                # catch potential special characters at end of codebook words
                if ends_in_special_character(word):
                    coded_word += codetable[word[-1]]
                codebook_words.append(coded_word)
                book_indices.append(current_index)
        elif is_trailing_poly(word, string_words[current_index - 1], poly_words):
            codebook_words.append('')   # empty string for assembly with later items
            book_indices.append(current_index)
        elif not is_trailing_poly(word, string_words[current_index - 1], poly_words):
            coded_word = codebook_strip(word, codebook)
            if coded_word:
                if ends_in_special_character(word):
                    coded_word += codetable[word[-1]]
                codebook_words.append(coded_word)
                book_indices.append(current_index)
            else:
                codebook_words.append(word)
        current_index += 1
    return codebook_words, book_indices


def table_converter(old_string, book_indices, lang='octen') -> list:
    """receives a string and a list of indices indicating skipped words, then converts them using a codetable
        old_string :argument the string to be converted
        book_indices :argument list of indices which have already been converted by codebook_converter
        lang :argument indicates which codetable to use
        codetable_words :return list of converted segments"""
    codetable = octen_table
    if lang == 'harran':
        codetable = harran_table
    string_words = old_string.split()
    codetable_words = []
    # resolve weird iteration problem in codetable.keys() return
    table_word_keys = []
    for key in codetable.keys():
        if len(key) > 1:
            table_word_keys.append(key)
    # convert words to appropriate counterparts
    for word in string_words:
        converted_word = ''
        if string_words.index(word) not in book_indices:
            if table_strip(word, codetable):
                # catch potential special characters at end of codetable words
                if ends_in_special_character(word):
                    converted_word = table_strip(word, codetable) + codetable[word[-1]]
                else:
                    converted_word = codetable[word]
            else:
                for char in word[::1]:
                    converted_word += codetable[char]
        codetable_words.append(converted_word)
    return codetable_words


def codebook_strip(word : str, book):
    """checks if the string, when stripped of special characters, is in the codebook
        if so, returns the converted string, otherwise False
        word :argument the string being verified
        book :argument the codebook verified against"""
    if spec_stripper(word) in book.keys():
        return book[spec_stripper(word)]
    else: return False


def table_strip(word, table):
    """checks if the string, when stripped of special characters, is in table
        if so, returns the converted string, otherwise False
        word :argument the string being verified
        table :argument the codetable verified against"""
    if spec_stripper(word) in table.keys():
        return table[spec_stripper(word)]
    else: return False


def is_trailing_poly(word : str, old_word : str, poly_words) -> bool:
    """checks if word is the end of a polymember word
        word :argument the current word being verified
        old_word :argument the previous word to concatenate with word
        poly_words :argument the list of polymember words verified against
        bool :return"""
    if spec_stripper(old_word)+ ' '+spec_stripper(word) in poly_words:
        return True
    else:
        return False


def ends_in_special_character(word : str) -> bool:
    """checks for special character at end of given string
        word :argument the string being verified
        bool :return"""
    if word[-1] in ['.', ':', '`', '/', '+', '-', '=']:
        return True
    else: return False


def converted_string_joiner(codebook_words, codetable_words) -> str:
    """concatenates a string of converted words from the two word lists,
        inserting space character 'spc' where necessary
        codebook_words :argument the list of words converted by codebook
        codetable_words :argument the list of words converted by codetable
        joined_string :return the concatenated string of words"""
    # ' ' character for converted space insertion
    spc = octen_table[' ']
    # define return value
    joined_string = ''
    word = 0
    while word < len(codetable_words):
        if word == 0:
            if codetable_words[word] != '':
                joined_string += codetable_words[word]
            else: joined_string += codebook_words[word]
        elif codetable_words[word] == '' and codebook_words[word] != '':
            joined_string += spc+codebook_words[word]
        elif codetable_words[word] != '':
            joined_string += spc + codetable_words[word]
        else: joined_string += codetable_words[word]
        word += 1
    return joined_string


def spec_stripper(word) -> str:
    """strips specific special characters from a string
    word :argument the word to be stripped
    str :return the stripped word"""
    return word.strip('.:`/+-=')


###########
#         #
# Decoder #
#         #
###########


# TODO: TEST EVERYTHING BELOW THIS
def message_decoder(message: str, lang='octen') -> (list, dict, list, dict, list, dict, list, dict):
    """From an encoded message, returns a series of lists and dictionaries which
    message :arg the message to be decoded
    lang :arg the codebook/codetable to use"""
    # get correct codebook/codetable data
    cb_keys, cb_vals = get_dict_lists(lang, is_book=True)
    ct_keys, ct_vals = get_dict_lists(lang)

    # get segment lengths
    w_len = len(cb_vals[0])
    l_len, m_len, s_len = get_segment_lengths(ct_vals)

    # get potential match lists and dicts
    w, w_sd = segment_replacer_loop(message, w_len, cb_keys, cb_vals)
    l, l_sd = segment_replacer_loop(message, l_len, ct_keys, ct_vals)
    m, m_sd = segment_replacer_loop(message, m_len, ct_keys, ct_vals)
    s, s_sd = segment_replacer_loop(message, s_len, ct_keys, ct_vals)

    return w, w_sd, l, l_sd, m, m_sd, s, s_sd


def get_segment_lengths(vals: list) -> (int, int, int):
    """gets longest, shortest, and median length of items in a list
    vals :argument list of values to be assessed
    long :return the length of the longest item in vals
    medium :return the length of neither the shortest nor the longest item in vals
    short :return the length of the shortest item in vals"""
    lens = []
    for _ in vals:
        lens.append(len(_))
    long = max(lens)
    medium = median(lens)
    short = min(lens)
    return long, medium, short


# seg_len informs accuracy
def segment_replacer_loop(string: str, seg_len: int, keys: list, vals: list) -> (list, dict):
    """compares segments from string against items in vals, then matches them to keys,
     using a standard length of a segment.
     string :argument the string to be compared
     seg_len :argument length of a segment to be compared
     keys :argument keys matched to values
     vals :argument values matched to keys
     r_list :return list in parallel to the original string
     sub_dict :return dictionary of keys replaced in the original keys dict for future ease of display"""
    # fills empty indices in r_list
    fill = '█'
    # for segment types with keys of length > 1 e.g. codebook, some medium/long codetable keys (to compare where
    # appropriate)
    # only supports 26 entries
    sub_dict_values = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    sub_dict = {}
    i = 0
    for key in keys:
        if len(key) > 1:
            sub_dict[key] = sub_dict_values[i]
            i += 1
    #debug
    print(sub_dict)
    # first character index for word detection slice
    first = 0
    # last character (and sentinel) for word detection slice
    last = seg_len
    # set up return
    r_list = []
    while last <= len(string)+seg_len-1: # can't have segments that are longer than seg_len after string length
        if string[first:last] in vals:
            # use sub_dict if key is too long
            if keys[vals.index(string[first:last])] in sub_dict.keys():
                r_list.append(sub_dict[keys[vals.index(string[first:last])]])
            else:
                r_list.append(keys[vals.index(string[first:last])])
        else:
            r_list.append(fill)
        first += 1
        last += 1
    while len(r_list) < len(string):
        r_list.append(fill)
    return r_list, sub_dict


# this is easier than grabbing it over and over and over
def get_dict_lists(lang: str, is_book=False) -> (list, list):
    """extracts keys and values of a dict
    codebook :argument the dict to extract data from
    d_keys :return the list of keys in the dict
    d_vals :return the list of values in the dict"""
    d_keys = []
    d_vals = []
    # TODO: make this more responsive to additional tables 13/08/24
    if lang == 'octen':
        if is_book:
            d_keys = list(octen_codebook.keys())
            d_vals = list(octen_codebook.values())
        else:
            d_keys = list(octen_table.keys())
            d_vals = list(octen_table.values())
    elif lang == 'harran':
        if is_book:
            d_keys = list(octen_codebook.keys())
            d_vals = list(octen_codebook.values())
        else:
            d_keys = list(octen_table.keys())
            d_vals = list(octen_table.values)
    return d_keys, d_vals



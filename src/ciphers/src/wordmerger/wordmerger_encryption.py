def wordmerger_encryption(input_text):
    '''wordmerger_encryption combines direkt neighbors of whitespace and replaces them
    :param input_text: string to apply it

    :returns: encrypted text
    '''

    whitespace_list = [pos for pos, char in enumerate(input_text) if char == " "]  # get whitespace positions in text

    for whitespace in whitespace_list:
        plainPair = input_text[whitespace - 1] + input_text[
            whitespace + 1]  # get last letter from word a and first letter from word b
        cipheredPair = "#" # encrypt with "#"
        input_text = input_text[:whitespace - 1] + "§" + input_text[whitespace:]  # replace last character from word A
        input_text = input_text.replace(input_text[whitespace], cipheredPair)  # replace whitespace with wordmerg
        input_text = input_text[:whitespace + 1] + "§" + input_text[
                                                         whitespace + 2:]  # replace first character from word B

    input_text = input_text.replace("§", "")  # remove all template §
    return input_text




if __name__ == "__main__":

    plaintext = "Test message to see if the wordmerging w o r ks as asp ected"
    wordmerger_encryption(plaintext)
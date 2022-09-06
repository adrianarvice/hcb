import string
from random import choice


def polyphonic_encryption(cipher_alphabet, plaintext):
    '''polyphonic_encryption encrypts a text by creating a random correspondence table based on inputs
    :param cipher_alphabet: ciphertext alphabet we want to have (must be a list)
    :param plaintext: key to test the range with

    :returns: encrypted text
    '''

    # remove whitespace and make it uppercase
    plaintext = plaintext.replace(" ", "").upper()

    # get unqiue characters from plain_msg, i.e. create plaintext alphabet
    plain_alphabet = list(set(plaintext))

    # create keys of correspondence table based on predefined cipher_alphabet
    correspondence_table = {}
    for character in cipher_alphabet:
        correspondence_table[character] = []

    # assign randomly values to the correspondence_table
    while plain_alphabet != []:
        for key, val in correspondence_table.items():
            try:
                chosen_elem = choice(plain_alphabet)
                correspondence_table[key] += chosen_elem
                plain_alphabet.remove(chosen_elem)
            except:
                continue

    # inverse correspondence_table to later encrypt with it
    inverse_correspondence_table = {}
    for key in correspondence_table:
        for item in correspondence_table[key]:
            if item not in inverse_correspondence_table:
                inverse_correspondence_table[item] = [key]
            else:
                inverse_correspondence_table[item].append(key)

                # encrypt with inverse_correspondence_table
    ciphertext = ""
    for symbol in plaintext:
        for key, val in inverse_correspondence_table.items():
            if symbol == key:
                ciphertext += choice(val)

    return ciphertext, correspondence_table


if __name__ == "__main__":

    plaintext = "If my algortihmus works correctly you should be able to decrypt the message"
    polyphonic_encryption(cipher_alphabet, plaintext)

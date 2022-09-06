from flask_socketio import emit
from pydoc import plain
from random import randrange, sample, shuffle, random, choice, sample
from math import log, exp, e
import string
import time
import json
import os
import sys

def count_unique_chars(s: str):
    '''count_unique_chars counts every unique character of a string i.e. creates alphabet of it

    :param s: string to count every unique character from
    :returns: returns list of unique strings from s
    '''

    return list(set(s))


def sourcetext_characteristics():
    '''sourcetext_characteristics concatenates default sourcetexts and parses it

    :returns: returns combined sourcetexts without punctuation
    '''

    plainAlphabet = string.ascii_lowercase

    # default sourcetexts
    path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'sourcetexts', 'english'))
    sourcetext = open(path + "/AChristmasCarol.txt").read().lower() + open(
        path + "/AliceInWonderland.txt").read().lower() + open(
        path + "/JekyllAndHyde.txt").read().lower()

    # remove whitespace and punctuation
    parsed_sourcetext = ""
    for i in sourcetext:
        if i in plainAlphabet:
            parsed_sourcetext += i

    sourcetext_alphabet = "".join(count_unique_chars(parsed_sourcetext))
    return parsed_sourcetext, sourcetext_alphabet


def calc_prob_source(sourcetext, n_gram, plainAlphabet):
    '''calc_prob_source calculates the probability of ngrams of sourcetext

    :param sourcetext: string for which we want the probability
    :param n_gram: size of blocks
    :poram plainAlphabet: alphabet of intended language
    :returns: probability analysis of n_gram for sourcetext
    '''

    size_alphabet = len(plainAlphabet)
    upper_bound = n_gram - 1
    specific_gram = [0] * (size_alphabet ** n_gram)

    for i in range(len(sourcetext) - (n_gram - 1)):
        index = 0
        for j in range(0, n_gram):
            index += plainAlphabet.index(sourcetext[i + j]) * (size_alphabet ** (upper_bound - j))

        specific_gram[index] += 1

    for i in range(size_alphabet ** n_gram):
        specific_gram[i] = specific_gram[i] / (len(sourcetext) - (n_gram - 1))

    return specific_gram


def calc_fitness_cipher(text, n_gram, plainAlphabet, sourceFreq):
    '''calc_fitness_cipher calculates fitness of a string based on n_gram

    :param text: string for which we want to calculate the fitness for
    :param n_gram: block size
    :poram plainAlphabet: alphabet of intended language
    :returns: fitness of text
    '''

    fit = -99
    upper_bound = n_gram - 1
    size_alphabet = len(plainAlphabet)

    for i in range(len(text) - (n_gram - 1)):
        specfic_gram = text[i:i + n_gram]

        index = 0
        for j in range(0, upper_bound):
            index += plainAlphabet.index(specfic_gram[j]) * (size_alphabet ** (upper_bound - j))

        index += plainAlphabet.index(specfic_gram[upper_bound])

        y = sourceFreq[index]

        if y == 0:
            fit += -15
        else:
            fit += log(y)

    fit = fit / (len(text) - (n_gram - 1))

    return fit


def create_alphabet(source_chars, cipher_chars):
    '''create_alphabet creates the initial key based on unique chars from ciphertext and sourcetext

    :param source_chars: alphabet of plaintext language
    :param cipher_chars: alphabet of ciphertext
    :returns: initial key as a list
    '''

    cipher_alphabet = {}
    for character in cipher_chars:
        cipher_alphabet[character] = []

    plain_alphabet = list(source_chars)

    # until every letter from plaintext alphabet is assigned
    while plain_alphabet != []:
        for key, val in cipher_alphabet.items():
            try:
                chosen_elem = choice(plain_alphabet)
                cipher_alphabet[key] += chosen_elem
                plain_alphabet.remove(chosen_elem)
            # if plain_alphabet is already empty, but for loop has iterations left
            except:
                continue

    cipher_alphabet_List = []
    for key, val in cipher_alphabet.items():
        for elem in val:
            cipher_alphabet_List.append(elem)

    return cipher_alphabet_List


def decrypt(ciphertext, key):
    '''decrypt provides a possible decryption based on choices

    :param ciphertext: alphabet of plaintext language
    :param key: key to test the range with
    :returns: decrypted text
    '''

    plaintext = ""
    for symbol in ciphertext:
        substitute = symbol.replace(symbol, choice(key[symbol]))
        plaintext += substitute

    return plaintext


def estimate_FitnessRange(ciphertext, key, ngram, plainAlphabet, sourceFreq):
    '''estimate_FitnessRange estimates range of fitness by one key

    :param ciphertext: alphabet of plaintext language
    :param key: key to test the range with
    :param ngram: alphabet of plaintext language
    :param plainAlphabet: alphabet of plaintext language
    :param sourceFreq: alphabet of plaintext language
    :returns: best fitness of the key in n iterations and its text/decryption
    '''

    # split up list in 2er sublists
    split_newKeyList = [key[x:x + 2] for x in range(0, len(key), 2)]

    # append list to alphabet
    alphabet = {}
    for i in range(10):
        alphabet[str(i)] = split_newKeyList[i]

    fit = -99  # initial arbitrary fit
    bestFit = fit
    bestText = ""

    edited_ciphertext = ciphertext[0:500]
    for i in range(25):

        plaintext = decrypt(edited_ciphertext, alphabet)
        fit = calc_fitness_cipher(plaintext, ngram, plainAlphabet, sourceFreq)

        if fit > bestFit:
            bestText = ""
            bestFit = fit
            bestText += plaintext


    return bestFit, bestText


def simulated_annealing(text, key, ngram, plainAlphabet, sourceFreq, max_time, coolingFactor, initial_temperature):
    '''simulated_annealing performs actual decryption process

    :param text: alphabet of plaintext language
    :param key: initial key to modify further
    :param ngram: block size
    :param plainAlphabet: alphabet of plaintext language
    :param sourceFreq: probability of sourcetext
    :param max_time: maximum runtime in minutes
    :param coolingFactor: reduce temperature each iteration by it
    :param initial_temperature: predefined temperature

    :returns: best fitness of the key in n iterations
    '''

    bestkey = key
    bestText = text
    bestFit = -99  # initial arbitrary fit
    temperature = initial_temperature

    size_alphabet = len(plainAlphabet)

    # run loop for max_time minutes
    t_end = time.time() + 60 * max_time
    program_starts = time.time()
    while time.time() < t_end:
        now = time.time()
        duration = now - program_starts
        seconds = int(duration)

        # neighbor keys
        keylist = key[:]
        neighbour_1 = randrange(size_alphabet)
        neighbour_2 = randrange(size_alphabet)
        a, b = neighbour_1, neighbour_2
        keylist[a], keylist[b] = keylist[b], keylist[a]

        # apply key n times to ciphertext, to see range of fitness, i.e. range of possible decryptions
        decrypt = estimate_FitnessRange(text, keylist, ngram, plainAlphabet, sourceFreq)
        fit = decrypt[0]
        plaintext = decrypt[1]

        random_probability = random()
        calculated_probability = exp(-(bestFit - fit) / temperature)

        if fit > bestFit:
            key = keylist[:]
            bestFit = fit
            bestkey = keylist
            bestText = plaintext
            print(fit, seconds)
            # emit('polyphonic_decryption_analyzer', fit)

        elif random_probability < calculated_probability:
            shuffle(key)
            key = keylist[:]

        # shotgun restart if temperature is too low
        if temperature < 110:
            temperature = initial_temperature
            print("RESHUFFLE", fit, seconds)
            shuffle(key)
            # emit('polyphonic_decryption_analyzer', fit)

        # reduce temperature
        temperature *= coolingFactor

    return (bestFit, bestkey, bestText)


def main(ciphertext, n_gram, max_time, coolingFactor, initial_temperature):
    '''main is framework for the decryption, it creates, gets all needed vars for SA

    :param ciphertext: ciphertext to decrypt
    :param n_gram: size of block
    :param max_time: maximum runtime in minutes per n_gram
    :param coolingFactor: reduce temperature each iteration by it
    :param initial_temperature: predefined temperature

    :returns: best decryption based of fitness
    '''

    sourcetext_parsing = sourcetext_characteristics()
    sourcetext = sourcetext_parsing[0]  # sourcetext without punctuation / whitespace
    sourcetext_chars = sourcetext_parsing[1]  # sourcetext alphabet

    ciphertext_parsing = count_unique_chars(ciphertext)
    ciphertext_chars = ciphertext_parsing  # ciphertext alphabet

    upper_bound = n_gram + 1  # so for loop iterates up to n_gram
    bestFit = -99  # arbitrary fit

    initial_key = create_alphabet(sourcetext_chars, ciphertext_chars)

    for ngram in range(2, upper_bound):
        sourceFreq = calc_prob_source(sourcetext, ngram,
                                      sourcetext_chars)  # statistical values of sourcetext in n_gram size
        SA = simulated_annealing(ciphertext, initial_key, ngram, sourcetext_chars, sourceFreq, max_time, coolingFactor,
                                 initial_temperature)
        fit = SA[0]
        key = SA[1]
        plaintext = SA[2]

        if fit > bestFit:
            bestText = plaintext
            print(bestText, bestFit, key)

    return bestText


if __name__ == "__main__":

    # https://mysterytwister.org/challenges/level-2/polyphone-verschluesselung-teil-1
    text = ""

    main(text, 5, 5, 0.9975, 500000.0)

from itertools import product


def n_letter_alphabet(n):
    assert n >0
    alphabet = [chr(ord('A')+i) for i in range(0,n %26 if n >26 else n)]
    if n <=26 : 
        return alphabet
    return alphabet + [chr(ord('a')+i) for i in range(0,n -26)]

#does not give back the empty string
def all_alpha_strings(alphabet,n):
    for k in range(n + 1):
        for s in product(alphabet, repeat=k):
            yield ''.join(s)


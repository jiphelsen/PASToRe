from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple,Union,Literal,Set, Union,List
from util import n_letter_alphabet
import numpy as np

############################ CONFIG ############################
TEST_TRIE=False
NULL_STR = -1
NO_VAL = -2
NULL_STR_TYPE = Literal[-1]
STD_ALPHABET = n_letter_alphabet(26)

BIN_ALPHABET=['0','1']
ALPHABET = STD_ALPHABET

assert ALPHABET is not None and len(ALPHABET)>0
def in_alphabet(c:chr)->bool:
    return c in ALPHABET
alph_ord = lambda alph : lambda c : alph.index(c)
Aord = alph_ord(ALPHABET)
PASToReOutput = Union[Tuple[int,int], Tuple[Literal[NULL_STR_TYPE],str]]
############################

@dataclass
class PASToRe_record:
    key : PASToReOutput
    value: str

    def __str__(self) -> str:
        return f"{self.key} -> {self.value}"

#from geeks for geeks : https://www.geeksforgeeks.org/dsa/trie-insert-and-search/ 
class TrieNode:
    def __init__(self,alphabet_len=len(ALPHABET)) -> None:
        self.children : Union[None, TrieNode] = [None] * alphabet_len
        self.isEndOfWord :bool = False
        self.value :int  = NO_VAL

class Trie:
    def __init__(self,alphabet =None) -> None:
        if alphabet is None:
            alphabet=ALPHABET
        self.alphabet=alphabet
        self.root :TrieNode = TrieNode(len(self.alphabet))

    # Method to insert a key into the Trie
    def insert(self, key : str, value : PASToRe_record) -> None:
        curr = self.root
        for c in key:
            if c not in self.alphabet: raise ValueError(f"invalid symbol {c}")
            index = self.alphabet.index(c) 
            if curr.children[index] is None:
                curr.children[index] = TrieNode(len(self.alphabet))
            curr = curr.children[index]
        curr.isLeaf = True
        curr.value = value

    # Method to search a key in the Trie
    def search(self, key) -> int:
        curr = self.root
        for c in key:
            if c not in self.alphabet: raise ValueError(f"invalid symbol {c}")
            index = self.alphabet.index(c) 
            if curr.children[index] is None:
                raise Exception(f"Failed Trie search for {key}")
            curr = curr.children[index]
        return curr.value

    # Method to check if a prefix exists in the Trie
    def isPrefix(self, prefix):
        curr = self.root
        for c in prefix:
            if c not in self.alphabet: raise ValueError(f"invalid symbol {c}")
            index = self.alphabet.index(c)
            if curr.children[index] is None:
                return False
            curr = curr.children[index]
        return True

    def find_longest_matching_string(self, to_match:str) -> Tuple[str, int]:
        assert len(to_match)>0
        result =""
        c=to_match[0]
        curr=self.root
        for c in to_match: 
            if c not in self.alphabet: raise ValueError(f"invalid symbol {c}")
            index = self.alphabet.index(c)
            if curr.children[index] is None:
                return result,curr.value
            curr = curr.children[index]
            result+= self.alphabet[index]
        return result,curr.value



class PASToRe:
    def __init__(self, alphabet = None) -> None:
        if alphabet is None:
            alphabet = ALPHABET
        self.alphabet= ALPHABET
        self.__string_lookup: TrieNode = Trie(self.alphabet)
        self.__ord_dictionary = []
        self.__decode_dict={}
        self.__count=[]

    def __add_entry(self, key:PASToReOutput,value:str) -> bool : 

        self.__string_lookup.insert(value,len(self.__ord_dictionary))
        self.__ord_dictionary.append(PASToRe_record(key,value))
        self.__decode_dict[key] =value
        self.__count.append(1)
        return True

    def clear(self):
        self.__string_lookup: Trie = Trie(self.alphabet)
        self.__ord_dictionary = []
        self.__decode_dict={}
        self.__count=[]
    def __get_longest_matching_string(self, to_match) -> Tuple[str,PASToRe_record,int]:
        result,idx = self.__string_lookup.find_longest_matching_string(to_match)
        if idx != NO_VAL:
            self.__count[idx]+=1
        return result,idx

    def print_dict(self):
        for k in range(len(self.__ord_dictionary)):
            val = self.__ord_dictionary[k]
            print(f"word {k+1}: {str(val)}")

    def encode(self,stream : str,ouput_type:str = "list") -> Union[str,int]:
        assert len(stream)>0
        S = len(stream)
        i=0
        output =[]
        outputc=0
        entropy=0
        while i<S:
            W,W_idx = self.__get_longest_matching_string(stream[i:])

            if W =="":
                if ouput_type=="list": output.append((NULL_STR,stream[i]))
                outputc+=1
                self.__add_entry((NULL_STR,stream[i]),stream[i])
                i+=1
                continue
            
            
            j = i + len(W)

            if j >= S-1:
                break

            Y,Y_idx = self.__get_longest_matching_string(stream[j:])
            
            if Y != "":
                if ouput_type=="list": output.append((W_idx,Y_idx))
                outputc+=1
                self.__add_entry((W_idx,Y_idx),W+Y)
                i = j+len(Y)
            else :
                if ouput_type == "list": output.append((W_idx,stream[j]))
                outputc+=1
                self.__add_entry((W_idx,stream[j]),stream[j])
                i=j+1
        if ouput_type=="list":return output
        if ouput_type=="count": return outputc
        if ouput_type=="alt_entropy": 
            return np.var(self.__count)
    
    def decode(self, to_decode :List[PASToReOutput])->str:
        result =""
        for key in to_decode:
            result+=self.__decode_dict[key]
        return result
    
    def I_Z(self,stream)->int:
        return self.encode(stream,"count")
    
    #alternative entropy measurement
    def I_Alt(self,stream)->int:
        return self.encode(stream,"alt_entropy") 
        

"""
test from the paper
word 1: (0, A) -> A
word 2: (0, C) -> C
word 3: (0, G) -> G
word 4: (1, 2) -> AC
word 5: (4, 3) -> ACG
word 6: (3, 4) -> GAC
"""

if __name__ == "__main__":
    past = PASToRe(['A','C','G','T'])
    encoded = past.encode("ACGACACGGAC")
    print(encoded)
    past.print_dict()
    print(past.decode(encoded))
    past.clear()# PASToRe always reset after using the class

import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

# NONTERMINALS = """
# S -> NP
# NP -> N A|B|V B|N
# A -> V B|Adv A|A|V|P B|Adv|Conj C
# B -> N A|Det C|P B|Adv A|NP|V|Det
# C -> N NP|N A|Adj C|NP|V B
# """

NONTERMINALS = """
S -> S P S|NP VP
NP -> N|Det NP|NP P NP|N VP|V NP
VP -> V|V NP|VP Conj VP|Adv VP
NP -> P NP|Adj NP
VP -> NP V|VP Adv|Conj NP
VP -> VP Adj|VP VP|Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)
    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
        
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    p = ['.',',',':']
    words = nltk.word_tokenize(sentence)
    words = [ word.lower() for word in words]
    
    for word in words:
        num = [char for char in word if char.isdigit()]
        if word in p:
            words.remove(word)
        
        if len(num) != 0:
            words.remove(word)            
    
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    from nltk.tree import Tree
    frag = []
    
    for t in Tree('S', tree).pos():
        if t[1] == 'N':
            frag.append(Tree('NP',[t[0]]))
    
    return frag


if __name__ == "__main__":
    main()

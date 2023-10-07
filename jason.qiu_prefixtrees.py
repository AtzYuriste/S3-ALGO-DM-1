__license__ = 'Nathalie (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: prefixtrees.py 2023-10-03'

"""
Prefix Trees homework
2023-10 - S3
@author: jason.qiu
"""

from algo_py import ptree

###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

##############################################################################
## Measure

def countwords(T):
    """ count words in the prefix tree T (ptree.Tree)
    return type: int
    """
    
    if not T.children:
        return 1
    else:
        s = countwords(T.children[0])
        for i in range(1, T.nbchildren):
            if T.children[i].key[1]:
                s += 1
            s += countwords(T.children[i])
        return s


def __averagelength(T,l):
    """

    :param T: prefix tree we want to know the average length
    :param l: the length of a word that we will increase by 1 each time
    :return: the sum of length of all the words
    """
    if not T.children:
        return l
    else:
        tot = __averagelength(T.children[0], l+1)
        if T.key[1]:
            tot += l
        for i in range(1,T.nbchildren):
            tot += __averagelength(T.children[i], l+1)
        return tot

def averagelength(T):
    """ average word length in the prefix tree T (ptree.Tree)
    return type: float
    """
    tot = __averagelength(T,0)
    return tot / countwords(T)
    

###############################################################################
## Search and list

def __wordlist(T, s, L):
    """

    T: prefix tree of which we want to generate the list of words
    s: the string we will use to create the words
    L: the list that will contain all the words
    """
    if not T.children:
        L.append(s+T.key[0])
    else:
        if T.key[1]:
            L.append(s+T.key[0])
        for i in range( T.nbchildren):
            __wordlist(T.children[i], s+T.key[0], L)



def wordlist(T):
    """ generate the word list, in alphabetic order, of the prefix tree T (ptree.Tree)
    return type: str list
    """
    L = []
    __wordlist(T, "", L)
    return L

def __longestword(T, l, s):
    """

    :param T: the prefix tree in which we want to know the longest word
    :param l: the number of letter of a word
    :param s: the string we will use to create the word
    :return: a couple (max,longest_word) with the number of letter of the longest word and the longest word
    """
    if not T.children:
        return (l, s+T.key[0])
    else:
        (max_, longest_word) = __longestword(T.children[0], l+1, s+T.key[0])
        for i in range(1,T.nbchildren):
            (count, word) = __longestword(T.children[i], l+1, s+T.key[0])
            if max_ < count:
                max_ = count
                longest_word = word
        return (max_,longest_word)


def longestword(T):
    """ search for the longest word in the prefix tree T (ptree.Tree)
    return type: str    
    """
    (_,w)= __longestword(T, 0, "")
    return w

def __searchword(T, w, l, i):
    """

    :param T: the prefix tree in which we want to search w
    :param w: the word we are searching
    :param l: length of the word
    :param i: index
    :return: true if the word searched is in the ptree and false if not
    """
    if not T.children:
        return i == l-1 and w[i] == T.key[0]
    else:
        if i >= l:
            return False
        else:
            if w[i] == T.key[0]:
                if i == l-1 and T.key[1]:
                    return True
                for j in range(T.nbchildren):
                    if __searchword(T.children[j], w, l, i+1):
                        return True
            else:
                return False


def searchword(T, w):
    """ search for the word w (str) not empty in the prefix tree T (ptree.Tree)
    return type: bool
    """
    for j in range(T.nbchildren):
        if __searchword(T.children[j], w, len(w), 0):
            return True
    return False


def __hangmman(T, pattern, l, i, L, s):
    """
    :param T: the prefix tree
    :param pattern: the pattern
    :param l: length of the word
    :param i: index
    :param L: list of words that match with the pattern
    :param s: string that will carry the words
    """
    if not T.children:
        if pattern[i] == '_' and i == l-1 or T.key[0] == pattern[i] and i == l-1:
            L.append(s+T.key[0])
    else:
        if i == l-1 :
            if T.key[1] and pattern[i] == '_' or pattern[i] == T.key[0]:
                L.append(s+T.key[0])
        elif i < l:
            if pattern[i] == '_' or pattern[i] == T.key[0]:
                    for j in range(T.nbchildren):
                        __hangmman(T.children[j], pattern, l, i+1, L, s+T.key[0])


def hangman(T, pattern):
    """ Find all solutions for a Hangman puzzle in the prefix tree T: 
        words that match the pattern (str not empty) where letters to fill are replaced by '_'
    return type: str list
    """
    L = []
    for j in range(T.nbchildren):
        __hangmman(T.children[j], pattern, len(pattern), 0, L, "")
    return L

###############################################################################
## Build

def buildlexicon(T, filename):
    """ save the tree T (ptree.Tree) in the new file filename (str)
    """
    L = wordlist(T)
    l = len(L)
    fichier = open(filename, 'w')
    for i in range(l-1):
        fichier.write(L[i]+"\n")
    fichier.write(L[l-1])
    fichier.close()

def __insert(T, s, new):
    """
    :param T: the prefix tree in which we want to insert the new child
    :param s: the key of the new child
    :param new: the new child
    """
    i = 0
    while i < T.nbchildren and s > T.children[i].key[0]:
        i += 1
    T.children.insert(i, new)

def __addword(T, w, l, i):
    """
    :param T: the prefix tree in which we want to add the new word
    :param w: the word we want to add
    :param l: the length of the word
    :param i: index
    """
    if not T.children:
        if i == l-1:
            print("pppp")
            newtree = ptree.Tree((w[i], True))
            __insert(T, w[i], newtree)
        elif i < l:
            print("aaaa")
            newtree = ptree.Tree((w[i], False))
            __insert(T, w[i], newtree)
            __addword(newtree, w, l, i+1)
    else:
        ok = True

        for j in range(T.nbchildren):
            if T.children[j].key[0] == w[i] and ok:
                if i == l-1:
                    newtree = ptree.Tree((w[i], True))
                    c = T.children[j].children
                    newtree.children = c
                    T.children.remove(T.children[j])
                    __insert(T, w[i], newtree)

                else:
                    print("caca")
                    __addword(T.children[j], w, l, i+1)
                ok = False

        if ok:
            print("dddd")
            if i == l - 1:
                newtree = ptree.Tree((w[i], True))
                __insert(T, w[i], newtree)
            else:
                newtree = ptree.Tree((w[i], False))
                __insert(T, w[i], newtree)
                __addword(newtree, w, l, i+1)



def addword(T, w):
    """ add the word w (str) not empty in the tree T (ptree.Tree)
    """
    __addword(T, w, len(w), 0)





def buildtree(filename):
    """ build the prefix tree from the lexicon in the file filename (str)
    return type: ptree.Tree
    """
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    Tree = ptree.Tree(('', False))

    for line in lines:
        addword(Tree, line)

    return Tree
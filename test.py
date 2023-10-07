from algo_py import ptree
from importlib.machinery import SourceFileLoader
import datetime


Tree1 = ptree.Tree(('', False),
                   [ptree.Tree(('c', False),
                               [ptree.Tree(('a', False),
                                           [ptree.Tree(('s', False),
                                                       [ptree.Tree(('e', True)),
                                                        ptree.Tree(('t', True),
                                                                   [ptree.Tree(('l', False),
                                                                               [ptree.Tree(('e', True))])])])]),
                                ptree.Tree(('i', False),
                                           [ptree.Tree(('r', False),
                                                       [ptree.Tree(('c', False),
                                                                   [ptree.Tree(('l', False),
                                                                               [ptree.Tree(('e', True))])])]),
                                            ptree.Tree(('t', False),
                                                       [ptree.Tree(('y', True))])]),
                                ptree.Tree(('o', False),
                                           [ptree.Tree(('m', False),
                                                       [ptree.Tree(('e', True))]),
                                            ptree.Tree(('u', False),
                                                       [ptree.Tree(('l', False),
                                                                   [ptree.Tree(('d', True))])])])]),
                    ptree.Tree(('f', False),
                               [ptree.Tree(('a', False),
                                           [ptree.Tree(('m', False),
                                                       [ptree.Tree(('e', True)),
                                                        ptree.Tree(('o', False),
                                                                   [ptree.Tree(('u', False),
                                                                               [ptree.Tree(('s', True))])])]),
                                            ptree.Tree(('n', True),
                                                       [ptree.Tree(('c', False),
                                                                   [ptree.Tree(('y', True))])])])])])


def __nodeTodot(T):
    if not T.key:
        return str(id(T)) + '[label="-"];\n'
    style = " shape = circle" if T.key[1] else ""
    return str(id(T)) + '[label="' + str(T.key[0]) + '"' + style + '];\n'


def __linkToDot(A, B):
    return "   " + str(id(A)) + " -- " + str(id(B)) + ";\n"


def __dot(T):
    s = ""
    for child in T.children:
        s += __nodeTodot(child)
        s += __linkToDot(T, child)
        s += __dot(child)
    return s


def dot_dfs(T):
    s = "graph {\n"
    s += "node [shape=none margin=0 width=0.3];\n"
    s += __nodeTodot(T)
    s += __dot(T)
    s += "}"
    return s


if __name__ == "__main__":
    myfile = "jason.qiu_prefixtrees.py"
    mycode = SourceFileLoader('mycode', myfile).load_module()
    nb1 = mycode.countwords(Tree1)
    average1 = mycode.averagelength(Tree1)
    words = mycode.wordlist(Tree1)
    longest = mycode.longestword(Tree1)
    search = mycode.searchword(Tree1, "c")
    listhang= mycode.hangman(Tree1, "_a__")
    #mycode.buildlexicon(Tree1, "test.txt")
    #print(words)
    #print(longest)
    #print(listhang)
    mycode.addword(Tree1, "abcde")
    mycode.addword(Tree1, "abcdz")
    #T1 = dot_dfs(Tree1)
    builded = mycode.buildtree("test.txt")
    T2 = dot_dfs(builded)
    print(T2)

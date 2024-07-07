from data.token import Token
from data.symbol_table import SymbolTable
from data.grammar import NonTerminalType as N, Terminal as T
from data.derivation_tables import Derivation,DerivationTable,ProductionList
import sys
from sys import argv
import copy

from lexical_analyzer import LexicalAnalyzer

no_principal=None
class Node:
    def __init__(self, node_main):
        self.main = node_main
        self.children = []
        self.no = None
        self.parcial= None
        self.val1= None
        self.val2= None

    def nodemain(self):
        return self.main
    def lchildren(self):
        return self.children
    def nodechildren(self,node):
        self.children.append(node)

    def update_values(self):

        match self.nodemain():
            case N.EXPRESSION:
                if self.children[1].no:
                    self.no= self.children[1].no
                if self.no:
                    self.children[1].parcial=self.children[0].no

            case N.MAYBECOMPARE:
                if len(self.lchildren())==0:
                    self.no= self.parcial
                else:
                    if self.children[0].no:
                        self.no== self.children[0].no
                    if self.parcial:
                        self.children[1].parcial=self.parcial
            case N.COMPARISON:
                self.no= Node(self.lchildren()[0].nodemain())
            case N.NUMEXPRESSION:
                if self.children[0].no:
                    self.children[1].no= self.children[0].no
                if self.children[1].no:
                    self.no== self.children[0].no
            case N.INDEXTERM:
                if len(self.lchildren())==0:
                    self.no= self.parcial
                else:
                    #if self.no:
                    #    self.children[0].val1= self.children[3].no
                    #if self.children[1].no:
                    #    self.children[0].val2=self.parcial
                    if self.children[0].no:
                        self.children[2].parcial=self.children[0].no
                    if self.children[2].no:
                        self.no=self.children[2].no      
            case N.TERM:
                    if self.children[1].no:
                        self.children[1].parcial=self.children[0].no
                    if self.children[1].no:
                        self.no=self.children[1].no   
            case N.MULTUNARY:
                if len(self.lchildren())==0:
                    self.no= self.parcial
                else:
                    if self.children[0].no:
                        self.children[2].parcial= self.children[0].no
                    if self.children[2].no:
                        self.no=self.children[2].no    
            case N.MULDIV:
                self.no= Node(self.lchildren()[0].nodemain())
            case N.ADDSUB:
                self.no= Node(self.lchildren()[0].nodemain())
            case N.UNARYEXPR:
                if len(self.lchildren())==1:
                    if self.children[0].parcial:
                        self.children[0].no=self.children[0].parcial
                        self.no=self.children[0].no
                else:
                    if self.children[1].parcial:
                        self.children[1].no= Node(self.lchildren[0].nodemain())
                        self.children[1].no.nodechildren(0)
                        self.children[1].no.nodechildren(self.children[1].parcial)
                    if self.children[2].no:
                        self.no=self.children[2].no    
            case N.FACTOR:
                if len(self.lchildren())>1:
                    if self.children[1].nodemain()==N.EXPRESSION and self.children[1].no:
                        self.no= self.children[1].no
                self.parcial=Node(self.lchildren()[0].nodemain())
        if (self.no):
            print(self.nodemain())

        for c in self.lchildren():
            c.update_values()


tokens=[T.OPEN_P,T.IDENT,T.GREATER_THAN,T.INT_CONST,T.CLOSE_P,T.REMAINDER,
        T.INT_CONST]

def node_analysis(node):
    print('---------------------')
    print(str(node.nodemain()))
    if len(tokens)==0:
        return
    print(ProductionList[DerivationTable[node.nodemain()][tokens[0]]].tail)
    
    for new_child in ProductionList[DerivationTable[node.nodemain()][tokens[0]]].tail:
        if (new_child in N):
            new_node=Node(new_child)
            node_analysis(new_node)
            node.nodechildren(copy.deepcopy(new_node))
        else:
            tokens.pop(0)
            new_node=Node(new_child)
            node.nodechildren(copy.deepcopy(new_node))

def print_tree(node,depth):
    elbow = "└──"
    pipe = "│  "
    tee = "├──"
    blank = "   "
    last= (depth==0)
    if node:
        print((elbow if last else tee) +  depth*2*'-' + str(node.nodemain()))
        if len(node.lchildren())>0:
            children = node.lchildren()
            for i, c in enumerate(children):
                print_tree(c,depth+1)

    



def generate_tree():


    source_node = Node(N.EXPRESSION)
    node_analysis(source_node)
    print_tree(source_node, 0)
    for i in range (0,300):
        source_node.update_values()
    print_tree(source_node.no, 0)
    print('------------')

    print(source_node.no)

generate_tree()



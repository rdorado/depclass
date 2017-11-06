from nltk import Tree

import time
import nltk
import spacy
import sys
import en_core_web_sm

########################################################################
# class DPTree
class DPTree:

  def __init__(self, word, dep, pos, children=[]):
     self.word = word
     self.dep = dep
     self.pos = pos
     self.children = children

  def print(self):
     print(self.word+" "+self.dep)
     for child in self.children:
       child.print()

########################################################################
# class Parser
class Parser:     
  
  def __init__(self):
    self.nlp = spacy.load('en_core_web_md')

  def parse(self, sentence):
     doc = self.nlp(sentence)
     return to_dp_tree(getRoot(doc))

  def printTree(self, sentence): 
     doc = self.nlp(sentence)
     tree = to_nltk_tree(getRoot(doc))
     if type(tree) is not str: tree.pretty_print()

########################################################################
def tok_format(tok):
    return "_".join([tok.orth_, tok.dep_])

########################################################################
def getRoot(doc):
   for w in doc:
     if w.dep_ == "ROOT": return w

########################################################################
def to_nltk_tree(node): 
    children = [child for child in node.children]   
    if len(children) > 0:       
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

########################################################################
def to_dp_tree(node): 
    children = [child for child in node.children]   
    if len(children) > 0:       
        return DPTree(node.text, node.dep_, node.tag_, [to_dp_tree(child) for child in node.children])
    else:
        return DPTree(node.text, node.dep_, node.tag_)

########################################################################
def search_candidates(node, path_node, resp=[]):

    if compare(node, path_node):
      resp.append(node)

    for node in node.children:
      search_candidates(node, path_node, resp)

    return resp

def prnt(string, node, path_node):
   print( pr1(string,path_node)+" "+pr2(string,path_node)+" "+pr3(string,node,path_node)+" "+string+" "+str(node)+" "+str(path_node) )

def pr1(string, path_node):
   return str(string not in path_node)

def pr2(string, path_node):
   if string not in path_node: return "False"
   return str(path_node[string] == "*")

def pr3(string, node, path_node):
   if string not in path_node: return "False"
   if string == "word": return str(node.word == path_node['word'])
   if string == "dep": return str(node.dep == path_node['dep'])
   if string == "pos": return str(node.pos == path_node['pos'])
   return "False"

########################################################################
def compare(node, path_node):
  wf = False
  wd = False
  wt = False

  prnt('word',node, path_node)
  prnt('dep',node, path_node)
  prnt('pos',node, path_node)

  if 'word' not in path_node or path_node['word'] == "*" or node.word == path_node['word']:      
      wf = True
  if 'dep' not in path_node or path_node['dep'] == "*" or node.dep == path_node['dep']:
      wd = True
  if 'pos' not in path_node or path_node['pos'] == "*" or node.pos == path_node['pos']:
      wt = True
  return (wf and wd and wt)

########################################################################
def search_path(node, path, index):
   if len(path) == index: return True
   if compare(node, path[index]): 
      print(path)
      for child in node.children:
         if search_path(child, path, index+1): return True
   else: return False

########################################################################
def search(root, path):
  candidates = search_candidates(root, path[0])
  for candidate in candidates:
    if search_path(candidate, path, 0):
      return candidate


########################################################################

########################################################################






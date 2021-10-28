import spacy
from spacy import displacy
from spacy.matcher import Matcher
from nltk import Tree


nlp = spacy.load("en_core_web_sm")


class Teapot:
  def __init__(self):
    self.knowledge_graph=[]

  def viewKnowledge(self):
    for knowledge in self.knowledge_graph:
      self.printTree(knowledge)

  def train(self,text):
    parsed_text = self.parseTree(text)
    self.knowledge_graph+=parsed_text

  def reply(self,text):
    parsed_text = self.parseTree(text)

    for sentence in parsed_text:
        reversedSentence=sentence
        bestMatch = self.findBestMatch(sentence)
    self.printTree(sentence)
    self.printTree(bestMatch)

    answer=self.extractAnswer(sentence,bestMatch)[0]

    return answer

  def parseTree(self,text):
    doc =  nlp(text)
    out=[]
    for i,sentence in enumerate(doc.sents):
      tree=self.mapTree(sentence.root)
      out.append(tree)
    return out

  def mapTree(self,tree):
    if(tree!=None):
      wordMapped = self.wordMapping(tree.lemma_)
      if(wordMapped[0]=="<"):
        print(wordMapped)
        tree.lemma_ = wordMapped
    c1 = list(tree.children)
    for i,c in enumerate(c1):
      self.mapTree(c)
    return tree
      
  def wordMapping(self,word):
    word=word.lower()
    if(word=="who"):
      return "<person>"
    if(word=="what"):
      return "<clause>"
    if(word=="when"):
      return "<time>"
    if(word=="where"):
      return "<location>"
    if(word=="why"):
      return "<clause>"
    if(word=="how"):
      return "<clause>"
    return word
    

  def extractAnswer(self,g1,g2):
    if( g1==None or g2==None ):
      return []
    else:
      if(self.wordMapping(g1.lemma_)[0]=="<"):#Extract word
        return [self.convertAnswer(g2,self.wordMapping(g1.lemma_))]
    
    c1 = list(g1.children)
    c2 = list(g2.children)

    out=[]
    for i,c in enumerate(c1):
      if(i<len(c2)):
        out+=self.extractAnswer(c1[i],c2[i])
    return out

  def convertAnswer(self,word,type):
    if(type=="<person>"):
      out=""
      if(word.children!=None):
        for c in word.children:
          out+=" "+c.lemma_
      out += " " + word.lemma_
      return out.strip()
    return word.lemma_


  def findBestMatch(self,g1):
    bestScore = 0
    bestIndex = -1
    for idx,graph in enumerate(self.knowledge_graph):
      score = self.scoreMatch(g1,graph)
      if score>bestScore:
        bestScore = score
        bestIndex = self.knowledge_graph[idx]
    return bestIndex
    
  def scoreMatch(self,g1,g2):
    if( g1==None or g2==None ):
        return 0
    
    score = 0
    
    if(g1.lemma_.lower() == g2.lemma_.lower()):
        score+=1
    
    c1 = list(g1.children)
    c2 = list(g2.children)
    for i,c in enumerate(c1):
      if(i<len(c2)):
        score+=self.scoreMatch(c1[i],c2[i])


    return score

  def printTree(self,node):
    self.to_nltk_tree(node).pretty_print()

  def to_nltk_tree(self,node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.orth_, [self.to_nltk_tree(child) for child in node.children])
    else:
        return node.orth_
  def to_nltk_tree_lemma(self,node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(node.lemma_.lower(), [self.to_nltk_tree(child) for child in node.children])
    else:
        return node.lemma_.lower()




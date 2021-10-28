import spacy
from spacy import displacy
from spacy.matcher import Matcher
from nltk import Tree


nlp = spacy.load("en_core_web_sm")


class Teapot:
  def __init__(self):
    self.knowledge_graph=[]
    self.scripts=[]
    self.mode="qa"
    self.mappedWords={
      "who":"<person>",
      "what":"<clause>",
      "when":"<time>",
      "where":"<location>",
      "why":"<clause>",
      "how":"<clause>"
    }
    self.reverseMappedWords={}

    for key in self.mappedWords:
      value = self.mappedWords[key]
      self.reverseMappedWords[value]=key

  def setMode(self,mode):
    self.mode=mode

  def view(self):
    self.viewKnowledge()
    self.viewScripts()

  def viewScripts(self):
    for script in self.scripts:
      self.printTree(script)

  def viewKnowledge(self):
    for knowledge in self.knowledge_graph:
      self.printTree(knowledge)

  def train(self,text):
    parsed_text = self.parseTree(text)
    self.knowledge_graph+=parsed_text

  def loadScript(self,text):
    for key in self.reverseMappedWords:
      value = self.reverseMappedWords[key]
      text = text.replace(key,value)
    parsed_text = self.parseTree(text)
    self.scripts+=parsed_text
    

  def reply(self,text):
    parsed_text = self.parseTree(text)

    for sentence in parsed_text:
        reversedSentence=sentence
      
        bestMatchArr = self.findBestMatch(sentence)
        bestMatch = bestMatchArr[0]
        bestMatchExtracted = bestMatchArr[1]

        
    answer=bestMatchExtracted

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
      out={}
      out["lemma"]=tree.lemma_
      out["modified"]=self.wordMapping(tree.lemma_)
      out["word"]=tree.orth_

      c1=list(tree.children)
      out["children"]=[]
      for i,c in enumerate(c1):
        out["children"].append(self.mapTree(c))
    else:
      return None
    return out
      
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

  def reverseWordMapping(self,word):
    word=word.lower()
    if(word=="<person>"):
      return "who"
    if(word=="<clause>"):
      return "what"
    if(word=="<time>"):
      return "when"
    if(word=="<location>"):
      return "where"
    if(word=="<clause>"):
      return "why"
    if(word=="<clause>"):
      return "how"
    return word
    


  def convertAnswer(self,word,type):
    if(type=="<person>"):
      out=""
      if(word["children"]!=None):
        for c in word["children"]:
          out+=" "+c["word"]
      out += " " + word["word"]
      return out.strip()
    return word["word"]


  def findBestMatch(self,g1):
    bestScore = 0
    bestIndex = -1
    bestReversed = False
    bestExtracted = {}
    currentExtracted = {}

    g1Reversed = dict(g1)
    g1Reversed["children"] = list(reversed(g1Reversed["children"]))

    self.printTree(g1)
    self.printTree(g1Reversed)

    if(self.mode=="qa"):
      for idx,graph in enumerate(self.knowledge_graph):
        score = self.scoreMatch(g1,graph,currentExtracted)
        if score>bestScore:
          bestScore = score
          bestIndex = self.knowledge_graph[idx]
          bestReversed = False
          bestExtracted = dict(currentExtracted)
        scoreRev = self.scoreMatch(g1Reversed,graph,currentExtracted)
        if scoreRev>bestScore:
          bestScore = scoreRev
          bestIndex = self.knowledge_graph[idx]
          bestReversed = True
          bestExtracted = dict(currentExtracted)
    else:
      for idx,script in enumerate(self.scripts):
        score = self.scoreMatch(g1,script,currentExtracted)
        if score>bestScore:
          bestScore = score
          bestIndex = self.scripts[idx]
          bestReversed = False
          bestExtracted = dict(currentExtracted)
        scoreRev = self.scoreMatch(g1Reversed,script,currentExtracted)
        if scoreRev>bestScore:
          bestScore = scoreRev
          bestIndex = self.scripts[idx]
          bestReversed = True
          bestExtracted = dict(currentExtracted)
        self.printTree(script)
        print(score)
        print(scoreRev)
    return [bestIndex,bestExtracted]
    
  def scoreMatch(self,g1,g2,extract):
    
    if( g1==None or g2==None ):
        return 0
    
    score = 0

    if(g1["modified"][0]=="<"):
      extract[g1["modified"]]=self.convertAnswer(g2,g1["modified"])
      return 1

    if(g2["modified"][0]=="<"):
      extract[g2["modified"]]=self.convertAnswer(g1,g2["modified"])
      return 1

    
    if(g1["modified"] == g2["modified"]):

        score+=1
    
    c1 = g1["children"]
    c2 = g2["children"]
    for i,c in enumerate(c1):
      if(i<len(c2)):
        score+=self.scoreMatch(c1[i],c2[i],extract)
    
    return score

  def printTree(self,node):
    self.to_nltk_tree(node).pretty_print()

  def to_nltk_tree(self,node):
    if node==None:
      return None
    else:
      return Tree(node["modified"], [self.to_nltk_tree(child) for child in node["children"]])
  

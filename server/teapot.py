import spacy
from spacy import displacy
from spacy.matcher import Matcher
from nltk import Tree
import json 

nlp = spacy.load("en_core_web_sm")


class Teapot:
  def __init__(self,id):
    self.id=id
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

    self.specialTokens={
      "<person>":"temp_name",
      "<time>":"temp_time",
      "<location>":"temp_location",
      "<phone_number>":"temp_phone",
    }
    self.specialTokensReversed={}
    for token in self.specialTokens:
      self.specialTokensReversed[self.specialTokens[token]]=token
    
  def setMode(self,mode):
    self.mode=mode


  def save(self):
    file1 = open("models/"+self.id+".json","w")
    dict_out={}
    dict_out["mode"]=self.mode
    dict_out["knowledge_graph"]=self.knowledge_graph
    dict_out["scripts"]=self.scripts
    file1.write(json.dumps(dict_out) )
    file1.close()

  def load(self):
    file1 = open("models/"+self.id+".json","r")
    dict_in = json.load(file1)
    file1.close()
    self.mode=dict_in["mode"]
    self.knowledge_graph=dict_in["knowledge_graph"]
    self.scripts=dict_in["scripts"]
    

  
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
    for key in self.specialTokens:
      value = self.specialTokens[key]
      text = text.replace(key,value)
    parsed_text = self.parseTree(text)
    self.scripts+=parsed_text
    

  def reply(self,text):
    text=text.replace("?","")
    parsed_text = self.parseTree(text)

    answer=""

    for sentence in parsed_text:
        reversedSentence=sentence
      
        bestMatchArr = self.findBestMatch(sentence)
        bestMatch = bestMatchArr[0]
        bestMatchExtracted = bestMatchArr[1]
        sentence_out=dict(sentence)
        sentence_out["children"]=reversed(sentence_out["children"])

        self.printTree(sentence)
        answer+=self.makeSentencePretty(self.constructSentence(sentence_out,bestMatchExtracted))

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
      out["pos"]=tree.pos_
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
    if(word in self.specialTokensReversed):
      word=self.specialTokensReversed[word]
    if(word in self.mappedWords):
      word=self.mappedWords[word]
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
    
  def makeSentencePretty(self,sentence):
    return sentence.capitalize()+"."
    
  def constructSentence(self,graph,entries):
    if(graph==None):
      return ""
    if(graph["modified"] in entries):# Substitute answers
      graph["word"] = entries[graph["modified"]]
    findClause = False
    out1=""
    out2=""

    for idx,child in enumerate(graph["children"]):
      if((graph["pos"]=="VERB" or graph["pos"]=="AUX") and idx>=1):
        findClause=True
      if(child["pos"]=="ADP"):# clause
        findClause=True
      if(findClause):
        out2+=" "+self.constructSentence(child,entries)
      else:
        out1+=" "+self.constructSentence(child,entries)
    if(graph["pos"]=="ADP"):
      return (graph["word"]+out1+out2).strip()
    else:
      return (out1+" "+graph["word"]+out2).strip()



  def findBestMatch(self,g1):
    bestScore = 0
    bestIndex = -1
    bestReversed = False
    bestExtracted = {}
    currentExtracted = {}

    g1Reversed = dict(g1)
    g1Reversed["children"] = list(reversed(g1Reversed["children"]))



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
    return [bestIndex,bestExtracted]
    
  def scoreMatch(self,g1,g2,extract):
    
    if( g1==None or g2==None ):
        return 0
    
    score = 0

    if(g1["modified"][0]=="<"):
      extract[g1["modified"]]=self.constructSentence(g2,{})
      return 1

    if(g2["modified"][0]=="<"):
      extract[g2["modified"]]=self.constructSentence(g1,{})
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
      return Tree(node["modified"]+"("+node["pos"]+")", [self.to_nltk_tree(child) for child in node["children"]])
  

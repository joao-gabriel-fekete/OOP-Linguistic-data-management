from mimetypes import init
import re
import spacy
import pandas as pd
from torch import xlogy
nlp = spacy.load("en_core_web_sm")

sample = "./taggedfiles\CorIFA-UFMG-B1.Ind.E.Abs.2016-2.0912.0519.txt"

class TaggedFile:
    
    def run(self, path):
        #Run all the methods from the object
        self.path = path
        self.mainInfo()
        self.readInText()
        self.clean()
        self.listWordsStructure()
        self.lemmatizeWord()
        self.organize()

    def mainInfo(self):
        #Extract important information from file path
        self.fileID = re.findall(r"CorIFA.*\d{4}", self.path)[0]
        self.register = re.findall(r"\.(\w+)\.\d{4}\-\d{1}", self.fileID)[0]

    def readInText(self):
        #Reads in the text itself
        with open(self.path, 'r') as f:
            self.text = f.read()
            f.close()
    
    def clean(self):
        #Removes unnecessary information the text might contain
        text = self.text
        text = re.sub(r"\<CorIFA.*?>", "", text)
        text = re.sub(r"\.", "", text)
        self.textClean = text

    def listWordsStructure(self):
        #Turns text into a list of strings, each one containing one word or feature
        text = self.textClean
        wordsList = text.splitlines()
        self.wordsList = list(filter(None, wordsList))

    def lemmatizeWord(self):
        wordListFinal = []
        wordList = self.wordsList
        for i in range(len(wordList)):
            targetWord = re.findall(r'(?<=\=)[a-zA-Z]+', wordList[i])
            if "EXTRAWORD" not in targetWord and targetWord:
                targetWord = re.sub(r"[\'|\[|\]]", "", str(targetWord))
                nlp_text = nlp(targetWord)
                for token in nlp_text:
                    lemma = str(token.lemma_)
                wordListFinal.append(re.sub(r"(?<=\=).*", lemma, wordList[i]))
            else:
                wordListFinal.append(wordList[i])

        self.wordsListLemmatized = wordListFinal

    def organize(self):
        df = pd.DataFrame(columns=["fileID", "register", "word", "structure", "lemma"])
        wordlist = self.wordsListLemmatized
        for i in wordlist: 
            information = re.search(r'(?P<word>\w+\s)(?P<structure>.*?\=)(?P<lemma>.*)', i)
            if information != None:     
                word = information.group('word')
                structure = information.group('structure')
                lemma = information.group('lemma')
                rowToAdd = {"fileID":self.fileID, "register":self.register, "word":word, "structure":structure, "lemma":lemma}
                df = df.append(rowToAdd, ignore_index=True)

        self.dfTextFinal = df

#x = TaggedFile()
#x.run(sample)
#print(x.fileID)
#print(x.register)
# print(x.textClean)
# print(x.wordsList)
# print(x.wordsListLemmatized)
#print(x.dfTextFinal.head(20))

class BatchInformation:
    def __init__(self, paths):
        self.filesPathList = paths

    def run(self):
        self.getData()

    def getData(self):
        dfFinal = pd.DataFrame(columns=["fileID", "register", "word", "structure", "lemma"])
        log = []
        flagCerto = 0
        flagErrado = 0
        for i in self.filesPathList:
            x = TaggedFile()
            try:
                x.run(i)
                flagCerto += 1
            except:
                flagErrado += 1
                continue
            df = x.dfTextFinal
            if not df.empty:
                dfFinal = dfFinal.append(df)
            else:
                log.append("There was a problem in file: " + i)
            print("Arquivos rodados certo: "+str(flagCerto))
            print("Arquivos rodados errado: "+str(flagErrado))
            print("\n\n")

        self.log = log
        self.dfFinal = dfFinal

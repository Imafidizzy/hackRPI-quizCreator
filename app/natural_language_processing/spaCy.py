import spacy
import PyPDF2
import docx
import os
from spacy import displacy
from spacy.matcher import Matcher

def getPDFText(filename):
    #Open pdf in read binary format. Then read the file
    pdfFileObj = open(filename, 'rb') 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #if pdf is encrypted, return error
    if(pdfReader.isEncrypted):
        print('Error, cannot process as PDF is encrypted!')
    else:
        return pdfReader.extractText()

def getDOCXText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)

def compileTempString(array):
    tempArray = array
    size = len(tempArray)
    tempString = tempArray[0]
    for x in range(size-1):
        tempString = tempString + " " + tempArray[x + 1]
    return tempString

def spacey(filename):
    nlp = spacy.load("en_core_web_sm")

    test, file_extension = os.path.splitext(filename)
    if(file_extension == '.pdf'):
        text = getPDFText(filename)
    elif(file_extension == '.docx'):
        text = getDOCXText(filename)
    else:
        print('Not a supported file type!')
        return
    
    doc = nlp(text)
    resultsArray = []
    tempString = []
    verbString = []
    for tok in doc:
        #print(tok.lower_, tok.pos_, tok.dep_)
        #TAKE ALL COMPOUND DEPENDENCIES
        if(tok.dep_ == "compound" or (tok.dep_ == "amod" and (tok.pos_ == "NOUN" or tok.pos_ == "PROPN"))):
            tempString.append(tok.lower_)
            continue
        #punctuation in compound dependencies
        elif(tok.dep_ == "punct" and tempString):
            tempString.append(tok.lower_)
            continue
        #If tempString is not empty, it's the last proper noun or noun in the list of compounds
        elif((tok.pos_ == "PROPN" or tok.pos_ == "NOUN") and tempString):
            tempString.append(tok.lower_)
            resultsArray.append(compileTempString(tempString))
            tempString = []
            continue
        #if standalone propernoun or noun
        elif((tok.pos_ == "PROPN" or tok.pos_ == "NOUN") and tok.dep_ == "ROOT"):
            resultsArray.append(tok.lower_)
            continue
        #Verb root to noun/pronoun direct object
        elif(tok.pos_ == "VERB" and tok.dep_ == "ROOT"):
            verbString.append(tok.lower_)
            continue
        #verb was root and noun/pronoun is direct object
        elif(verbString and tok.dep_ == "dobj" and (tok.pos_ == "NOUN" or tok.pos_ == "PROPN")):
            verbString.append(tok.lower_)
            resultsArray.append(compileTempString(verbString))
            verbString = []
            continue
        #verb was root but not noun/pronoun or not direct object
        elif(verbString):
            verbString = []
            continue
        #other
        else:
            continue
    resultsArray = list(dict.fromkeys(resultsArray))
    return resultsArray

    #print(doc)
    #displacy.serve(nlp("The quick brown fox went to work"), style="dep")
    #displacy.serve(doc, style="dep")

def results(filename):
    result = spacey(filename)
    for x in range(len(result)):
        result[x] = 'What is "' + result[x] + '"'
    return(result)

results('../../test/Population_Dynamic_Notes.docx')

#Rulesets
#Can have multiple proper nouns if they're compounded
#Nouns and proper nouns without any dependencies
#dependencies on spaces do not count
#Verb to noun or propernoun that is a direct object


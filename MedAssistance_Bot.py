#Install & download pkgs
#pip install tflearn
#pip download nltk
#pip install nltk

#If gcolab, import the followings, if virtaul env in yor computer, then not necessary

from google.colab import files
import io



#Import libraries

import pandas as pd
import numpy 
import tflearn
import tensorflow
import random
import json
import pickle
import nltk
nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer=LancasterStemmer()


#open the file

with open('intents_Aydin.json')as myFile:
    data=json.load(myFile)
    
#open the pickled file 

try:
    with open ("doc.pickle", "rb") as pickled_file:
        linguisticUnit, labelUnit, text_X,text_Y=pickle.load(pickled_file)
except:

#loop through the data through the json file
  linguisticUnit=[]
  labelUnit=[]
  text_X=[]
  text_Y=[]

  for intent in data["intents"]:
      for pattern in intent["patterns"]:
          tokenized_word= nltk.word_tokenize(pattern)
          linguisticUnit.extend(tokenized_word)
          text_X.append(pattern)
          text_Y.append(intent["tag"])

      if intent["tag"] not in labelUnit:
          labelUnit.append(intent["tag"])
         


  linguisticUnit=[stemmer.stem(w.lower()) for w in linguisticUnit if w != "?"]
  linguisticUnit=sorted(list(set(linguisticUnit)))


  labelUnit=sorted(labelUnit)

  trained_data=[]
  output_data=[]

  out_empty=[0 for _ in range(len(labelUnit))]


  for data, text in enumerate(text_X):
      bag=[]

      tokenized_word=[stemmer.stem(word.lower()) for word in text]

      for word in linguisticUnit:
          if word in tokenized_word:
              bag.append(1)
          else:
            bag.append(0)

      output_row=out_empty[:]
      output_row[labelUnit.index (text_Y[data])]=1

      trained_data.append(bag)
      output_data.append(output_row)

  trained_data=numpy.array(trained_data)
  output_data=numpy.array(output_data)


  with open ("doc.pickle", "wb") as pickled_file:
    pickle.dump((words,labelUnit, training,output), pickled_file)


#tokenize the words in the json file

def words_container(containerUnit,words):
   container=[0 for __ in range(len(words))]  

   tokenized_wrds=nltk.word_tokenize(containerUnit)
   tokenized_wrds=[stemmer.stem(word.lower())for word in tokenized_wrds]

   for tokenizedUNit in tokenized_wrds:
      for unit in enumerate(words):
        if w==tokenizedUNit:
          container[i]=1
          # container[i].apend(1)
   return numpy.array(container)


#create a function that engines the bot

def botEngine():
  print ("Aydın doktoru size ne yemeniz konusunda tavsiyede bulunmaya hazır (kalp ile ilgili bir sorununuz olduğunda")
  print ("Konuşmayı durdurmak istiyorsanız 'TAMAM' yazın")
  while True:
    input_data=input("Sen: ")
    # print('\n')
    if input_data.lower()=="tamam":
      print("Aydin:  Geçmiş Olsun")
      break
    predicted=model.predict ([words_container(input_data,words)])[0]
    results_index=numpy.argmax(predicted)
    taggedUnit=labels[results_index]
    
    if predicted[results_index] > 0.7:
      for tag_data in data['intents']:
        if tag_data['tag']== taggedUnit:
          responseUnit=tag_data['responses']
      print("Aydin:", random.choice(responseUnit))
    else:
      print("Lütfen söylemek istediğinizi basitleştirir misiniz?")


#call the bot function to run the software
botEngine()

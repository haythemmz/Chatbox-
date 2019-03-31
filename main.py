#%%
import numpy as np 
import tensorflow as tf 
import re 
import time 
import pandas as pd 
#%% 
lines = open('movie_lines.txt', encoding='utf-8', errors='ignore').read().split('\n')
conversations = open('movie_conversations.txt', encoding='utf-8', errors='ignore').read().split('\n')

#%%
id_line={}
for line in lines : 
    _line = line.split('+++$+++')
    if len(_line) == 5 :
        id_line[_line[0].replace(" ","")] = _line[4]


#%%

conversation_id = []
for conversation in conversations[:-1] : 
        _conversation=conversation.split('+++$+++')[-1][2:-1].replace("'","").replace(" ","")
        conversation_id.append(_conversation.split(','))
#%%
questions=[]
answers=[]
for conversation in conversation_id :
        for i in range(len(conversation)-1):
                questions.append(id_line[conversation[i]])
                answers.append(id_line[conversation[i+1]])


#%%
def clean_text(text):
        text=text.lower()
        abbr_dict={
        "what's":"what is",
        "what're":"what are",
        "who's":"who is",
        "who're":"who are",
        "where's":"where is",
        "where're":"where are",
        "when's":"when is",
        "when're":"when are",
        "how's":"how is",
        "how're":"how are",
        "i'm":"i am",
        "we're":"we are",
        "you're":"you are",
        "they're":"they are",
        "it's":"it is",
        "he's":"he is",
        "she's":"she is",
        "that's":"that is",
        "there's":"there is",
        "there're":"there are",
        "i've":"i have",
        "we've":"we have",
        "you've":"you have",
        "they've":"they have",
        "who've":"who have",
        "would've":"would have",
        "not've":"not have",
        "i'll":"i will",
        "we'll":"we will",
        "you'll":"you will",
        "he'll":"he will",
        "she'll":"she will",
        "it'll":"it will",
        "they'll":"they will",
        "isn't":"is not",
        "wasn't":"was not",
        "aren't":"are not",
        "weren't":"were not",
        "can't":"can not",
        "couldn't":"could not",
        "don't":"do not",
        "didn't":"did not",
        "shouldn't":"should not",
        "wouldn't":"would not",
        "doesn't":"does not",
        "haven't":"have not",
        "hasn't":"has not",
        "hadn't":"had not",
        "won't":"will not",
        '["\'?,\.<>()=*;%!µ|-]':""}
        for j in abbr_dict.keys():
                text=re.sub(j,abbr_dict[j],text)
        return text
clean_question=[]
for q in questions:
        clean_question.append(clean_text(q))

clean_aswers = []
for a in answers:
        clean_aswers.append(clean_text(a))
#%%

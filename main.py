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
clean_questions=[]
for q in questions:
        clean_questions.append(clean_text(q))

clean_answers = []
for a in answers:
        clean_answers.append(clean_text(a))
#%%
word2count = {}
for question in clean_questions:
    for word in question.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
for answer in clean_answers:
    for word in answer.split():
        if word not in word2count:
            word2count[word] = 1
        else:
            word2count[word] += 1
#%%
threshold=15 
questionswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        questionswords2int[word] = word_number
        word_number += 1

answerswords2int = {}
word_number = 0
for word, count in word2count.items():
    if count >= threshold:
        answerswords2int[word] = word_number
        word_number += 1


#%%
tokens = ['<PAD>', '<EOS>', '<OUT>', '<SOS>']
for token in tokens:
    questionswords2int[token] = len(questionswords2int) + 1
for token in tokens:
    answerswords2int[token] = len(answerswords2int) + 1



#%% 
answersints2word = {w_i: w for w, w_i in answerswords2int.items()}
#%%
for i in range(len(clean_answers)):
    clean_answers[i] += ' <EOS>'

#%%
questions_into_int = []
for question in clean_questions:
    ints = []
    for word in question.split():
        if word not in questionswords2int:
            ints.append(questionswords2int['<OUT>'])
        else:
            ints.append(questionswords2int[word])
    questions_into_int.append(ints)
answers_into_int = []
for answer in clean_answers:
    ints = []
    for word in answer.split():
        if word not in answerswords2int:
            ints.append(answerswords2int['<OUT>'])
        else:
            ints.append(answerswords2int[word])
    answers_into_int.append(ints)


#%%
sorted_clean_questions = []
sorted_clean_answers = []
for length in range(1, 25 + 1):
    for i in enumerate(questions_into_int):
        if len(i[1]) == length:
            sorted_clean_questions.append(questions_into_int[i[0]])
            sorted_clean_answers.append(answers_into_int[i[0]])


#%%
def model_inputs():
    inputs = tf.placeholder(tf.int32, [None, None], name = 'input')
    targets = tf.placeholder(tf.int32, [None, None], name = 'target')
    lr = tf.placeholder(tf.float32, name = 'learning_rate')
    keep_prob = tf.placeholder(tf.float32, name = 'keep_prob')
    return inputs, targets, lr, keep_prob
<<<<<<< HEAD

#%%

=======
#%%
>>>>>>> 43e848966387568375d4040792205e6413dbb8e3
def preprocess_targets(targets, word2int, batch_size):
    left_side = tf.fill([batch_size, 1], word2int['<SOS>'])
    right_side = tf.strided_slice(targets, [0,0], [batch_size, -1], [1,1])
    preprocessed_targets = tf.concat([left_side, right_side], 1)
    return preprocessed_targets

#%%
<<<<<<< HEAD
=======

>>>>>>> 43e848966387568375d4040792205e6413dbb8e3
def encoder_rnn(rnn_inputs, rnn_size, num_layers, keep_prob, sequence_length):
    lstm = tf.contrib.rnn.BasicLSTMCell(rnn_size)
    lstm_dropout = tf.contrib.rnn.DropoutWrapper(lstm, input_keep_prob = keep_prob)
    encoder_cell = tf.contrib.rnn.MultiRNNCell([lstm_dropout] * num_layers)
    encoder_output, encoder_state = tf.nn.bidirectional_dynamic_rnn(cell_fw = encoder_cell,
                                                                    cell_bw = encoder_cell,
                                                                    sequence_length = sequence_length,
                                                                    inputs = rnn_inputs,
                                                                    dtype = tf.float32)
    return encoder_state


#%%
def decode_training_set(encoder_state, decoder_cell, decoder_embedded_input, sequence_length, decoding_scope, output_function, keep_prob, batch_size):
    attention_states = tf.zeros([batch_size, 1, decoder_cell.output_size])
    attention_keys, attention_values, attention_score_function, attention_construct_function = tf.contrib.seq2seq.prepare_attention(attention_states, attention_option = "bahdanau", num_units = decoder_cell.output_size)
    training_decoder_function = tf.contrib.seq2seq.attention_decoder_fn_train(encoder_state[0],
                                                                              attention_keys,
                                                                              attention_values,
                                                                              attention_score_function,
                                                                              attention_construct_function,
                                                                              name = "attn_dec_train")
    decoder_output, decoder_final_state, decoder_final_context_state = tf.contrib.seq2seq.dynamic_rnn_decoder(decoder_cell,
                                                                                                              training_decoder_function,
                                                                                                              decoder_embedded_input,
                                                                                                              sequence_length,
                                                                                                              scope = decoding_scope)
    decoder_output_dropout = tf.nn.dropout(decoder_output, keep_prob)
    return output_function(decoder_output_dropout)

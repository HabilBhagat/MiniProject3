import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
 
def read_article(f_name):
    file = open(f_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []

    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop() 
    
    return sentences

def sentence_similarity(sentence1, sentence2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sentence1 = [w.lower() for w in sentence1]
    sentence2 = [w.lower() for w in sentence2]
 
    all_words = list(set(sentence1 + sentence2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    
    for w in sentence1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)
 
def construct_similarity_matrix(sentences, stop_words):
    
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for id1 in range(len(sentences)):
        for id2 in range(len(sentences)):
            if id1 == id2:
                continue 
            similarity_matrix[id1][id2] = sentence_similarity(sentences[id1], sentences[id2], stop_words)

    return similarity_matrix


def summary_generation(f_name, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    
    sentences =  read_article(f_name)

   
    sentence_similarity_martix = construct_similarity_matrix(sentences, stop_words)

    
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)

    
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    print("Indexes of top ranked_sentence order are ", ranked_sentence)    
    fp1= open("answer.txt","w")
    
    for i in range(top_n):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

    def listToString(summarize_text):  
        str1 = ""   
        for ele in summarize_text:  
            str1 += ele   
        return str1    
    listToString(summarize_text)
    fp1.write(listToString(summarize_text))
    fp1.close()
    print("Summarize Text: \n", ". ".join(summarize_text))
    

    
summary_generation( "recognized.txt", 2)

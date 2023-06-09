#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import os
import math
# load data to pandas data frame
import pandas as pd
import numpy as np
#!pip install gdown
#import gdown


# In[2]:


# Specify the correct file path or URL
file_path = "top_250/教父 (1972) .csv"

# Read the CSV file
doc_data = pd.read_csv(file_path, sep=",", header=0)

# Continue with the rest of your code
review_title = doc_data['Review_Title'].tolist()
review = doc_data['Review'].tolist()

# Print the DataFrame to verify the data was loaded correctly
print(doc_data)


# In[3]:


review


# In[4]:


df = pd.DataFrame(doc_data)

pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("max_colwidth", 100)

print(df)


# In[5]:


# Define function for Lemmatization, remove stopword and feature selection using POS, spacy package
import spacy
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner']) # disable parser, ner for faster loading


# In[6]:


def spacy_preprocess (text,lemma= True, pos= True, pos_select = ["VERB", "NOUN", "ADJ", "ADV", "PART"]):
  # Initialize spacy 'en_core_web_sm' model, keeping only tagger component needed for lemmatization
  # Parse the sentence using the loaded 'en' model object `nlp`
  doc = nlp(text)

  if pos== False:
    if lemma== True: text_preprocess= " ".join([token.lemma_.lower() for token in doc if not nlp.vocab[token.text].is_stop])
    if lemma== False: text_preprocess= " ".join([token.text.lower() for token in doc if not nlp.vocab[token.text].is_stop])
  else:  
    if lemma== True : text_preprocess= " ".join([token.lemma_.lower() for token in doc if (token.pos_ in pos_select and not nlp.vocab[token.text].is_stop)])
    if lemma== False : text_preprocess= " ".join([token.text.lower() for token in doc if (token.pos_ in pos_select  and not nlp.vocab[token.text].is_stop)])
  # nlp.vocab[token.text].is_stop to remove stopwords
  return text_preprocess


# In[7]:


# Pre-processing data with spacy
from tqdm.notebook import tqdm


# In[8]:


# Initialize a clean array
movie_synopses_preprocess=[]
# Pre-processing data with spacy
from tqdm.notebook import tqdm
# We only care VERB NOUN ADJ words from the text
for item in tqdm(review):
  movie_preprocess = spacy_preprocess(str(item), pos_select = ["VERB", "NOUN", "ADJ"])
  movie_synopses_preprocess+= [movie_preprocess]


# In[9]:


# Change data input (movie_synopses or movie_synopses_preprocess) here
# data_input = movie_synopses  # data without preprocess
data_input = movie_synopses_preprocess  # the data after preprocess text.

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words='english', min_df=0.1, max_df=0.8, max_features=None)
# vectorizer = TfidfVectorizer(stop_words='english', max_features=750)

feature_matrix = vectorizer.fit_transform(data_input).astype(float)
feature_names = vectorizer.get_feature_names()  # get feature names
print("Number of features:", len(feature_names))


# In[10]:


# create a dataframe from the array
feature_df = pd.DataFrame(feature_matrix.toarray(),columns=[feature_names])


# In[11]:


# You can observe that each Synopsis of moive can be convert 
feature_df


# In[12]:


from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# In[13]:


colors = ['#48D1CC', '#9ACD32', '#CD5C5C','#CD853F','#FFC0CB','#BC8F8F','#DDA0DD','#E5CF9C']

color_name_to_rgb = {
    'Medium Turquoise': '#48D1CC',
    'Yellow Green': '#9ACD32',
    'Indian Red': '#CD5C5C',
    'Peru': '#CD853F',
    'pink': '#FFC0CB',
    'Rosy Brown': '#BC8F8F',
    'Plum': '#DDA0DD',
    'Mimosa': '#E5CF9C'
}


# In[14]:


# function for K-means clustering
def k_means(feature_matrix, num_clusters=5):
    km = KMeans(n_clusters=num_clusters, n_init=500, random_state = 1,
                max_iter=10000)
    km.fit(feature_matrix)
    clusters = km.labels_
    return km, clusters


# In[15]:


# assume that we want to clustering withy k =3
num_clusters = 3

km_obj, km_clusters = k_means(feature_matrix=feature_matrix,num_clusters=num_clusters)
doc_data['Cluster'] = km_clusters


# In[16]:


get_ipython().system('pip install wordcloud')


# In[17]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


# In[18]:


import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# In[19]:


def generate_wordlist(synopsis_series):
    wordlist = []
    for text in synopsis_series:
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)

        for i, (word, pos) in enumerate(pos_tags):
            if pos in ('NN', 'JJ') and i < len(pos_tags) - 1:
                next_word, next_pos = pos_tags[i + 1]
                if next_pos == 'NN':
                    compound_word = f"\"{word}_{next_word}\""
                    wordlist.append(compound_word)
#                else:
#                    wordlist.append(word)
#            elif pos not in ('NN', 'JJ'):
#                wordlist.append(word)
    return wordlist


# In[20]:



generate_wordlist(doc_data[doc_data['Cluster'] == 0]['Review'])


# In[21]:


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')
nltk.download('words')


# In[22]:


import re

def generate_wordlist_reg(synopsis_series):
    wordlist = []
    pattern = re.compile(r"{<JJ>*<NN.?>}")
    print("0. ")

    for text in synopsis_series:
        words = word_tokenize(text)
        pos_tags = nltk.pos_tag(words)

        chunked_words = nltk.chunk.ne_chunk(pos_tags)
        print("1. ")
        print(f"chunked_words: {chunked_words}")
        for subtree in chunked_words.subtrees(filter=lambda t: t.label() == 'NNP'):
            compound_word = "_".join([word for word, pos in subtree.leaves()])
            if pattern.search(compound_word):
                print("3a. ")

                wordlist.append(f"\"{compound_word}\"")
            else:
                print(f"compound_word {compound_word}")
                print("3b. ")

    print("2. ")
    print(wordlist)
    return wordlist


# In[23]:


doc_data[doc_data['Cluster'] == 0]['Review']


# In[24]:


generate_wordlist_reg(doc_data[doc_data['Cluster'] == 0]['Review'])


# In[25]:


get_ipython().system('pip3 install wget')


# In[26]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

from wordcloud import WordCloud


# In[27]:


# Prepared font
import wget
wget.download("https://drive.google.com/uc?id=1eGAsTN1HBpJAkeVM57_C7ccp7hbgSz3_&export=download","TaipeiSansTCBeta-Regular.ttf")


# In[28]:


def plot_wordcloud_for_cluster(mytitle, seg_list):

  fig, ax = plt.subplots(figsize=(6, 6), dpi=300)  # Create a figure and axes

  # List of colormaps
  colormaps = ['plasma', 'inferno', 'magma', 'viridis', 'cividis', 'twilight', 'tab10']

  # Randomly pick a colormap
  random_colormap = random.choice(colormaps)

  wc = WordCloud(
      width=1500,
      height=1500,
      background_color='white',               #   Background Color
      max_words=200,                    #   Max words
  #    mask=back_image,                       #   Background Image
      max_font_size=None,                   #   Font size
      font_path="TaipeiSansTCBeta-Regular.ttf",
      random_state=50,                    #   Random color
      regexp=r"\w+(?:[-']\w+)*",  # Update the regexp parameter to include hyphens, you can mark out this line to hide the space character.
      contour_width=1,  # adjust the contour width
      contour_color='black',  # adjust the contour color
      colormap=random_colormap,  # choose a different colormap
      prefer_horizontal=0.9)                #   Ratio

  wc.generate(seg_list)
  # Add a border to the plot
  border = patches.Rectangle((0, 0), 1500, 1500, linewidth=2, edgecolor='black', facecolor='none')
  ax.add_patch(border)

  # Plot
  plt.axis("off")
  plt.imshow(wc, interpolation="bilinear")
  plt.title(mytitle, fontsize=24, color='#0a9396', pad=4)

  plt.show()


# In[29]:


this_wordlist = generate_wordlist(doc_data[doc_data['Cluster'] == 0]['Review'])

this_seg_list=' '.join(this_wordlist) # convert list into string seperated with space character
  
this_seg_list 


# In[30]:


#! pip install pillow


# In[31]:


plot_wordcloud_for_cluster(f"Word Cloud for Godfather", this_seg_list)


# In[32]:


pip install wordcloud==1.8.1


# In[ ]:





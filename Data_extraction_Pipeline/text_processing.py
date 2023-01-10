import pandas as pd 
import re
import nltk
from nltk.corpus import stopwords, webtext
from textblob import TextBlob,Word
from nltk.stem import PorterStemmer
import string
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download('webtext')
wt_sentences = webtext.sents('firefox.txt')
wt_words = webtext.words('firefox.txt')


text=['This is introduction to NLP','It is likely to be useful,to people ','Machine learning is the new electrcity','There would be less hype around AI and more action going forward','python is the best tool!','R is good langauage','I like this book','I want more books like this']

df = pd.DataFrame({"tweet":text})
df['tweet'] = df['tweet'].apply(lambda x: x.lower())
# print(df)

txt = 'i am.a software,engineer!!'
print(txt.replace('.',' '))
print(re.sub('[^\w\s]',' ',txt))

# df['tweet'] = df['tweet'].str.replace('[^\w\s]',' ',regex=True)
# print(df)

import string
for c in string.punctuation:
    df['tweet'] = df['tweet'].str.replace(c,' ',regex=True)
# print(df)


#Removing Stop Words
stop = stopwords.words('english')
df['tweet'] = df['tweet'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
#print(df)

#standardizing text
lookup_dict = {'nlp':'natural language processing', 'ur':'your', "wbu" : "what about you"}
def std_text(text):
    new_text = ""
    text = re.sub('[^\w\s]',' ',text)
    words = text.split()
    for x in words:
        if x.lower() in lookup_dict:
            new_text = new_text + " " + lookup_dict[x.lower()]
        else:
            new_text = new_text + " " + x
    return new_text

# print(std_text("nLp is, good, and ur name azad, wbu"))
df['tweet'] = df['tweet'].apply(lambda x: std_text(x))
# print(df)

#correcting speeling
df['tweet'] = df['tweet'].apply(lambda x: str(TextBlob(x).correct()))
print(df)

# df['tweet'] = df['tweet'].apply(lambda x: TextBlob(x).words)
df['tweet'] = df['tweet'].apply(lambda x: nltk.word_tokenize(x))
print(df)

#Stemming the text -> Stemming is a process of extracting a root word
text=['I like fishing','I eat fish','There are many fishes in pound', 'leaves and leaf']
st = PorterStemmer()
df = pd.DataFrame({"tweet":text})
df['tweet'] = df['tweet'].apply(lambda x: " ".join([st.stem(x) for x in x.split()]))
# print(df)

#Lemmatizing -> Lemmatization is a process of extracting a root word by considering the vocabulary
df['tweet'] = df['tweet'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
# print(df)


frequency_dist = FreqDist(wt_words)
# for i,v in frequency_dist.items():
#     print(f"{i}:{v}")
sorted_frenquency_dist = sorted(frequency_dist, key=frequency_dist.__getitem__, reverse=True)
# print(sorted_frenquency_dist[:20])

#Consider words with length greater than 3 and plot
large_words = dict([(k,v) for k,v in frequency_dist.items() if len(k)>3])

frequency_dist = nltk.FreqDist(large_words)
frequency_dist.plot(50,cumulative=False)

wcloud = WordCloud().generate_from_frequencies(frequencies=frequency_dist)
plt.imshow(wcloud, interpolation='bilinear')
plt.axis("off")
plt.show()



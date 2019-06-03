import urllib
import csv
import collections
from bs4 import BeautifulSoup
import io
import re
import string
from nltk.corpus import stopwords
import math
from operator import itemgetter

print('Intializing')
wiki = "https://en.wikipedia.org/wiki/Consulting_firm"
page = urllib.urlopen(wiki)
soup = BeautifulSoup(page,"lxml")
stop_words = set(stopwords.words('english'))
all_p=soup.find_all("p")
final_hash = collections.OrderedDict()

print('Filteration')
#Filteration
with open('index.csv', 'a') as csv_file:
    writer = csv.writer(csv_file)
    for para in all_p:
        words=para.getText().encode('UTF-8').split()

        #stop words removal
        for r in words:
            if not r in stop_words:
                appendFile = open('filteredtext.csv','a')
                appendFile.write(" "+r)
                text_string = para.getText().encode('UTF-8').lower()
        frequency = {}
        #print text_string
        match_pattern = re.findall(r'\b[a-z]{3,15}\b', text_string)
        #print match_pattern
        hashmap={}
        total_term=0

        #term frequency table
        for word in match_pattern:
            count = frequency.get(word,0)
            #print count
            frequency[word] = count + 1
            total_term += frequency[word]
            
        frequency_list = frequency.keys()
        for words in frequency_list:
            hashmap[words]=float(frequency[words])/float(total_term)
            #print float(frequency[words])/float(total_term)
            
        for element in hashmap:
            appendFile = open('tf_hashmap.csv','a')
            appendFile.write(" "+element+" ")
            appendFile.write(str(hashmap[element]))
        
        #entropy calculation
        entropy=0
        words=para.getText().encode('UTF-8').split()
        for ele in frequency_list:
            entropy=entropy-(hashmap[ele]*math.log(hashmap[ele]))
        final_hash[entropy]=para;

print('Sliding Windows Algo')
#sliding window algorithm
start_entropy=max(final_hash.items(), key=itemgetter(0))
k=0
for i in final_hash.items():
    if(i[0]==start_entropy[0]):
        break
    k=k+1
r_limit=k
l_limit=k
n=len(final_hash)
ent=[]                              #all entropy values
ent_f=collections.OrderedDict()     #window waali entropy values
k=0

print('Vector of all entropy values')
#vector of all entropy values
for i in final_hash.items():
    ent.append(i[0])

print('Boundary conditions')
#boundry conditions
while((r_limit < (n-1))  and (l_limit>=1) and ((r_limit-l_limit) <= (n/2))): 
    if(ent[r_limit+1] >= ent[l_limit-1]):
        r_limit=r_limit+1
    else:
        l_limit=l_limit-1

if((r_limit-l_limit+1)<=(n/2)):
    if(r_limit==len(final_hash)-1):
        l_limit=l_limit-((n/2) - (r_limit-l_limit) -1)
    else:
        r_limit=r_limit+ ((n/2)-(r_limit-l_limit) - 1)

nl_limit=l_limit
nr_limit=r_limit

print('ent_f hashmap')
#ent_f hashmap of entropy and <p> in final window
while(nr_limit >= nl_limit):
    ent_f[ent[nl_limit]]=final_hash[ent[nl_limit]]
    nl_limit=nl_limit+1

print('Precision Recall')
#precision recall
thresh=start_entropy[0]/2
ideal_ones=0
for i in final_hash.items():
    if(i[0]>=thresh):
        ideal_ones=ideal_ones+1

sizew=r_limit-l_limit+1
ones_window=0
nl_limit=l_limit
nr_limit=r_limit
while(nr_limit >= nl_limit):
    if(ent[nl_limit]>=thresh):
        ones_window=ones_window+1 
    nl_limit=nl_limit+1

prec=float(ones_window)/float(sizew)
recall=float(ones_window)/float(ideal_ones)
print ("precision ", prec)
print ("recall ", recall)

print 'Removal of irrelevant content'
#removal of irrelevant content
remove_this=[]
i=0
k=0
for i in range(len(final_hash)):
    if(i < l_limit or i > r_limit):
        remove_this.insert(k,str(final_hash[ent[i]]))
        k=k+1

soup_str=str(soup)
f=open("input.html","w+")
f.write(soup_str)

appendFile = open('output.html','a')
for i in range(len(remove_this)):
    if(soup_str.find(remove_this[i])==-1):
        soup_str.replace(remove_this[i],'', 1)

f1=open("output.html","w+")
f1.write(soup_str)
print 'Completed'

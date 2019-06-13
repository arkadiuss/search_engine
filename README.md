# Search Engine

A small "Google" to search articles by a topic implemented using Latent Semntic Indexing (LSA). Project for the computational methods.

## Dataset 

The used dataset is [set of articles from kaggle](https://www.kaggle.com/snapcrack/all-the-news)

## Steps

### Bag of words
At the beginning I create vector builded from all words over the articles.

### Preliminary processing
Nothing special, just removing of obvious things like capital letters or punctuation marks.

### Stemming
Words could be written in different forms. Stemming algorithms cut them all to a common root. I used the PorterStemming.

### Stop words
The prepositions or conjunctions don't contribute a lot to a topic of sentence. I remove them using common list of them.

### Matrix
Now we can create a matrix, in the row we have consecutive articles and columns are made from bag of words. Value in matrix's cell in number of times that this word was used in this article. Let's notice that this is sparse matrix.

### Inverse document frequency
IDF is simple, but a meaningful operation. Using the simple formula we can escalate value of rare words and reduce value of common ones.

### Normalization
It let us autonomize a corelation from a text's length. If it's done in preprocessing it can save some time during searching.   

### Denoising
As a last step I'm using SVD to denoise matrix. It filter noise from them and focus on main topics in articles. It's parametrized operation based on parameter k. We receive different results for different k-values.  
Although the operation was pretty fast, unfortunately for bigger sets of articles (like 50000 of them) I wasn't able to multiply result matrices. Neither as normal matrix (because of memory) nor as sparse ones (because of time). It's clearly visible in the results that for bigger size there is noise because of that.

## Results
Some example queries are put in results folder. It shows that it return articles by topic and the influence of denoising data. 

## Run
If you want to run it please download dataset and put it as csv files in articles folder. Then run processor first and then you can run search.
### Caching
Almost all the computations can be cached. I highly encourage to do that! Examples are shown in the code.

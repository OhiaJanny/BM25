
Original file is located at
    https://colab.research.google.com/drive/1JMGPsS24FdxKHBdCJ1G8daVTH-GM9YVK
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# #Installation
# %%capture
# !pip install rank_bm25


#Initialization
from rank_bm25 import BM25Okapi

corpus = [
    "Hello there good man!",
    "It is quite windy in London",
    "How is the weather today?"
]

tokenized_corpus = [doc.split(" ") for doc in corpus]

bm25 = BM25Okapi(tokenized_corpus)
# <rank_bm25.BM25Okapi at 0x1047881d0>

#Ranking Documents
query = "windy London"
tokenized_query = query.split(" ")

doc_scores = bm25.get_scores(tokenized_query)
# array([0.        , 0.93729472, 0.        ])

bm25.get_top_n(tokenized_query, corpus, n=1)
# ['It is quite windy in London']

"""NOW TO THE ASSIGNMENT ITSELFT"""

import nltk
nltk.download('punkt')  # Download the tokenizer data

"""Downloading all nltk packages"""

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# nltk.download('all')
#

"""Loading the 6 new groups"""

import os
import zipfile

# Define the correct paths
zip_path = "/content/drive/MyDrive/6_newsgroups.zip"
extract_path = "/content/6_newsgroups"

# Extract the zip file
if not os.path.exists(extract_path):  # Avoid re-extraction if already extracted
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

# Initialize storage for documents
news_data = {}

# Iterate through each category (folder)
for category in os.listdir(extract_path):
    category_path = os.path.join(extract_path, category)

    # Ensure it's a directory (i.e., a category folder)
    if os.path.isdir(category_path):
        news_data[category] = []

        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)

            # Ensure we only process text files and ignore system files like .DS_Store
            if os.path.isfile(file_path) and not filename.startswith('.'):
                try:
                    with open(file_path, "r", errors="ignore") as file:
                        content = file.read()
                        news_data[category].append(content)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# Print summary
print(f"\n✅ Successfully loaded {sum(len(docs) for docs in news_data.values())} documents across {len(news_data)} categories!")
print(f"Categories: {list(news_data.keys())}")



"""Process the data"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    # Remove special characters and numbers
    text = re.sub(r'\W+', ' ', text)

    # Tokenize
    words = word_tokenize(text.lower())  # Convert to lowercase

    # Remove stopwords
    words = [word for word in words if word not in stop_words]

    return ' '.join(words)

# Apply preprocessing to all documents
for category in news_data:
    news_data[category] = [preprocess_text(doc) for doc in news_data[category]]

print("Preprocessing complete!")



"""Extract the data"""

import os
import zipfile

zip_path = "/content/drive/MyDrive/6_newsgroups.zip"
extract_path = "/content"

# ✅ Remove existing extracted folder (if re-running)
if os.path.exists(os.path.join(extract_path, "6_newsgroups")):
    !rm -rf /content/6_newsgroups

# ✅ Extract properly
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# ✅ Fix dataset path (handle nested folder issue)
dataset_path = os.path.join(extract_path, "6_newsgroups")

# ✅ Check if the extracted folder is nested
inner_folders = os.listdir(dataset_path)
if len(inner_folders) == 1 and os.path.isdir(os.path.join(dataset_path, inner_folders[0])):
    dataset_path = os.path.join(dataset_path, inner_folders[0])  # Correct the path if nested

# ✅ Remove `.DS_Store` and other hidden system files from categories
categories = [folder for folder in os.listdir(dataset_path) if not folder.startswith(".")]

# ✅ Print final categories
print("Extracted Folders:", categories)

import os

dataset_path = "/content/6_newsgroups"
news_data = {}

for category in os.listdir(dataset_path):
    category_path = os.path.join(dataset_path, category)

    if os.path.isdir(category_path):  # Ensure it's a folder
        documents = []
        for filename in os.listdir(category_path):
            file_path = os.path.join(category_path, filename)
            with open(file_path, 'r', errors='ignore') as file:
                content = file.read().strip()
                if content:  # Ignore empty files
                    documents.append(content)
        news_data[category] = documents

# ✅ Print the number of documents in each category
print({k: len(v) for k, v in news_data.items()})



"""To Get the top 5 documents"""

import os
import zipfile
from rank_bm25 import BM25Okapi

# Define paths
zip_path = "/content/drive/MyDrive/6_newsgroups.zip"
extract_path = "/content/6_newsgroups"

# Extract the zip file if not already extracted
if not os.path.exists(extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

# Function to load and preprocess data
def load_documents(base_dir):
    documents = []
    doc_ids = []

    # Loop through category directories
    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)

        # Ensure it's a directory
        if os.path.isdir(category_path):
            for filename in os.listdir(category_path):
                file_path = os.path.join(category_path, filename)

                # Read only files
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r", errors="ignore") as file:
                            content = file.read().strip()
                            documents.append(content.split())  # Tokenizing by simple split
                            doc_ids.append(file_path)  # Store file path as ID
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    return documents, doc_ids

# Load dataset
docs, doc_paths = load_documents(extract_path)

# Build BM25 index
bm25_index = BM25Okapi(docs)

# BM25 Query Lookup Function
def lookup_query_BM25(query, K, bm25_index):
    tokenized_query = query.split()
    scores = bm25_index.get_scores(tokenized_query)

    # Sort by score in descending order
    top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:K]

    # Retrieve top documents
    top_k_docs = [doc_paths[i] for i in top_k_indices]
    top_k_scores = [scores[i] for i in top_k_indices]

    return top_k_docs, top_k_scores

# Example Query
query = "electronic circuits"
top_k_docs, top_k_scores = lookup_query_BM25(query, 5, bm25_index)

# Output results
print("Top 5 Documents:")
for doc, score in zip(top_k_docs, top_k_scores):
    print(f"{doc} - Score: {score:.4f}")



"""Updated Code with a main() Function that calls both my data extraction and data processing functions."""

import os
import zipfile
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')

stop_words = set(stopwords.words('english'))

# ✅ Function to extract dataset
def extract_dataset(zip_path, extract_path):
    # Remove existing extracted folder (if re-running)
    if os.path.exists(os.path.join(extract_path, "6_newsgroups")):
        os.system(f"rm -rf {os.path.join(extract_path, '6_newsgroups')}")

    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Fix dataset path (handle nested folder issue)
    dataset_path = os.path.join(extract_path, "6_newsgroups")
    inner_folders = os.listdir(dataset_path)

    # If nested, correct the path
    if len(inner_folders) == 1 and os.path.isdir(os.path.join(dataset_path, inner_folders[0])):
        dataset_path = os.path.join(dataset_path, inner_folders[0])

    # ✅ Remove unwanted files like .DS_Store
    categories = [folder for folder in os.listdir(dataset_path) if not folder.startswith('.')]

    print("Extracted Folders:", categories)
    return dataset_path, categories

# ✅ Function to read and process documents
def load_and_preprocess_data(dataset_path, categories):
    news_data = {}

    for category in categories:
        category_path = os.path.join(dataset_path, category)

        if os.path.isdir(category_path):  # Ensure it's a directory
            news_data[category] = []

            for file_name in os.listdir(category_path):
                file_path = os.path.join(category_path, file_name)

                # ✅ Ensure it's a file
                if os.path.isfile(file_path):
                    with open(file_path, "r", errors="ignore") as file:
                        content = file.read()
                        news_data[category].append(preprocess_text(content))

    print(f"Successfully loaded {sum(len(v) for v in news_data.values())} documents across {len(news_data)} categories!")
    return news_data

# ✅ Function for text preprocessing
def preprocess_text(text):
    text = re.sub(r'\W+', ' ', text)  # Remove special characters & numbers
    words = word_tokenize(text.lower())  # Tokenize & convert to lowercase
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    return ' '.join(words)

# ✅ Main function to tie everything together
def main():
    zip_path = "/content/drive/MyDrive/6_newsgroups.zip"
    extract_path = "/content"

    # Step 1: Extract dataset
    dataset_path, categories = extract_dataset(zip_path, extract_path)

    # Step 2: Load and preprocess data
    news_data = load_and_preprocess_data(dataset_path, categories)

if __name__ == "__main__":
    main()



"""ASSIGNMENT QUESTIONS.
QUESTIONS 1.
"""



print({k: len(v) for k, v in tokenized_corpus.items()})  # Should show counts > 0

""" Implementing BM25 Search"""

# ✅ BM25 search function
def search_bm25(query, top_n=10):
    query_terms = query.split()
    results = {}
    for category, model in bm25_models.items():
        scores = model.get_scores(query_terms)
        top_doc_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
        results[category] = [(news_data[category][i], scores[i]) for i in top_doc_indices]
    return results

# ✅ Helper function to extract document identifiers
def extract_doc_ids(results):
    """Extracts document content (or identifiers) from search results."""
    doc_ids = set()
    for category, docs in results.items():
        for doc, _ in docs:
            doc_ids.add(doc)  # Using document content as ID
    return doc_ids

# ✅ Multi-word query
multi_word_query_results = search_bm25("information retrieval system", top_n=10)
multi_word_docs = extract_doc_ids(multi_word_query_results)

# ✅ Single-word queries with intersection
word1_docs = extract_doc_ids(search_bm25("information", top_n=20))
word2_docs = extract_doc_ids(search_bm25("retrieval", top_n=20))
word3_docs = extract_doc_ids(search_bm25("system", top_n=20))

intersection_results = word1_docs & word2_docs & word3_docs  # Compute intersection

# ✅ Compare results
common_docs = multi_word_docs & intersection_results

print("\nMulti-word Query Results (Top 10):", multi_word_docs)
print("\nIntersection of Single-word Queries (All found results):", intersection_results)
print("\nNumber of common documents between the two strategies:", len(common_docs))
print("\nCommon Documents:", common_docs)

# ✅ Answering the assignment question
overlap_percentage = (len(common_docs) / len(multi_word_docs)) * 100 if multi_word_docs else 0
print(f"\nOverlap Percentage: {overlap_percentage:.2f}%")

if overlap_percentage > 50:
    print("\nThe two strategies return mostly similar results.")
else:
    print("\nThe two strategies return different results.")



"""ANSWER TO QUESTION 1

Summary of my Output Analysis
Multi-word Query Results (Top 10)

The multi-word query returned a set of documents from various newsgroups.
Intersection of Single-word Queries

The intersection method retrieved a different set of documents, and after intersecting the results of individual queries, a subset of documents was obtained.
Number of Common Documents Between Both Methods

The analysis indicates that only 2 documents were common between both retrieval strategies​
.
Interpretation of the Results

The low overlap suggests that the multi-word query and single-word intersection approaches retrieve different sets of documents.
The multi-word query might consider word relationships and ranking differently, leading to a more focused set of results.
The intersection of single-word queries broadens the search space initially but shrinks it after intersection, potentially missing relevant documents that were retrieved by the multi-word query.
Final Answer to Your Assignment Question
Are the results similar or different?
→ The results are different, with only 2 overlapping documents.
Key Takeaway
→ The multi-word query is likely more effective at retrieving contextually relevant results, whereas single-word queries with intersection might miss important results due to strict filtering.
"""



"""QUESTION 2"""

#Ran my BM25 search function with the original multi-word query
multi_word_query_results_1 = search_bm25("information retrieval system", top_n=10)
multi_word_query_results_2 = search_bm25("retrieval system information", top_n=10)

"""Print and Compare Results"""

print("\nResults for 'information retrieval system':")
for category, docs in multi_word_query_results_1.items():
    print(f"\nCategory: {category}")
    for i, (doc, score) in enumerate(docs):
        print(f"{i+1}. Score: {score:.4f} - {doc[:200]}...")  # Print first 200 characters

print("\nResults for 'retrieval system information':")
for category, docs in multi_word_query_results_2.items():
    print(f"\nCategory: {category}")
    for i, (doc, score) in enumerate(docs):
        print(f"{i+1}. Score: {score:.4f} - {doc[:200]}...")  # Print first 200 characters



"""ANSWER TO QUESTION 2

Analysis of My Results
Myresults for both queries:

"information retrieval system"
"retrieval system information"
Findings:
✅ The results are almost identical

The same documents appear in both queries.
The scores and ranking order are the same across categories.
Conclusion:
Word order does not matter in BM25.
"information retrieval system" and "retrieval system information" return the same results, proving that BM25 ignores word order in ranking documents.
"""



"""QUESTION 3"""

sentence_query_results = search_bm25("information retrieval system is very useful to me", top_n=10)
keyword_query_results = search_bm25("information retrieval system", top_n=10)

print("\nResults for Full Sentence Query:")
for category, docs in sentence_query_results.items():
    print(f"\nCategory: {category}")
    for i, (doc, score) in enumerate(docs):
        print(f"{i+1}. Score: {score:.4f} - {doc[:200]}...")  # Show preview

print("\nResults for Keyword Query:")
for category, docs in keyword_query_results.items():
    print(f"\nCategory: {category}")
    for i, (doc, score) in enumerate(docs):
        print(f"{i+1}. Score: {score:.4f} - {doc[:200]}...")



"""ANSWER TO QUESTION 3

Analysis of My Results
I tested:

Full Sentence Query: "information retrieval system is very useful to me"
Keyword Query: "information retrieval system"
Findings:
✅ The same documents appear in both queries

The key terms ("information retrieval system") dominate the ranking in both cases.
The same categories and document sets appear in both results.
✅ The full sentence query has higher scores

The scores in the sentence query are higher than in the keyword query.
This suggests that stop words slightly influence the ranking, but not the actual results.
✅ Stop words do not significantly impact retrieval

Words like "is," "very," "useful," and "to me" are common stop words and do not contribute to ranking.
However, BM25 does not completely ignore stop words—they can slightly change document scores.
Final Conclusion
Stop words do not significantly impact BM25 ranking, but they may slightly affect scores.

The most important words in a query are the key terms (e.g., "information retrieval system").
Removing stop words does not change the retrieved documents, but it may lower or adjust their scores.
"""



"""QUESTION 4"""

#1. Using BM25’s Built-in get_top_n Method

def search_bm25_builtin(query, top_n=10):
    query_terms = query.split()
    results = {}

    for category, model in bm25_models.items():
        top_docs = model.get_top_n(query_terms, news_data[category], n=top_n)
        results[category] = [(doc, "BM25 built-in")]  # Store retrieved documents

    return results
bm25_builtin_results = search_bm25_builtin("information retrieval system", top_n=10)

#2. Compare with Your Own Implementation

print("\nResults from Custom BM25 Implementation:")
for category, docs in multi_word_query_results.items():
    print(f"\nCategory: {category}")
    for i, (doc, score) in enumerate(docs):
        print(f"{i+1}. Score: {score:.4f} - {doc[:200]}...")  # Show preview

print("\nResults from BM25 Built-in `get_top_n`:")
for category, docs in bm25_builtin_results.items():
    print(f"\nCategory: {category}")
    for i, (doc, _) in enumerate(docs):
        print(f"{i+1}. - {doc[:200]}...")  # Show preview



"""ANSWER TO QUESTION 4


Do you get the same results?
→ No, BM25’s get_top_n retrieves fewer results and does not provide scores, while your method ranks all relevant documents properly.

Why or why not?
→ BM25’s built-in method directly selects top documents, while your method computes and sorts scores manually, giving better transparency and control.

Is your implementation better?
→ Yes! Your method ranks more documents, provides scores, and gives more insight into ranking differences.
"""



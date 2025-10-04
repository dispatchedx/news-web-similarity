# News Web Similary (Corpus-Based Document Similarity Engine)

This project is a Python-based system designed to scrape news articles from various web sources, process the text data, and build a searchable inverted index based on TF-IDF (Term Frequency-Inverse Document Frequency) weighting. The engine can then be queried to find articles that are semantically similar to a given set of terms.

The project is divided into two main components: a web scraping module built with Scrapy and a data processing and analysis module that uses libraries like NLTK and Scikit-learn.
Theres a more [detailed report with screenshot examples](report.pdf) in greek.
## Features

-   **Web Scraping**: Utilizes the Scrapy framework to crawl news websites like BBC and USA Today, extracting article text from dozens of categories.
-   **Natural Language Processing (NLP)**: Implements a text processing pipeline that includes:
    -   **Tokenization**: Breaking down raw text into individual words (lemmas).
    -   **Punctuation and Stop Word Removal**: Cleaning text by removing punctuation and common words that add little semantic value.
    -   **Part-of-Speech (POS) Tagging**: Identifying the grammatical category of each word and filtering out closed-class words (e.g., determiners, prepositions).
    -   **Lemmatization & Stemming**: Reducing words to their base or root form for accurate frequency counting.
-   **Inverted Index Construction**: Builds an inverted index from the scraped articles, mapping each processed word to the documents it appears in.
-   **TF-IDF Weighting**: Calculates the TF-IDF score for each word in every document, which measures how important a word is to a document in a collection of documents.
-   **Similarity Search**: Provides a search function that takes a query, finds matching articles in the inverted index, and ranks them by summing the TF-IDF scores of the query terms present in each document.
-   **Data Persistence**: The generated inverted index can be saved to and loaded from an XML file for reuse without needing to re-scrape or re-process the data.

## How It Works

1.  **Scraping**: The Scrapy spiders (`Articles.py` and `Bbc.py`) are run to crawl the specified news sites. As each article is parsed, the text is extracted and undergoes initial NLP processing (tokenization, POS tagging, lemmatization). The resulting word frequencies for each article are saved to JSON files.
2.  **Indexing**: The `build_from_scrapy` function reads the JSON output from the spiders. It constructs a global inverted index, first by counting the document frequency for each word (term frequency)  and then calculating the TF-IDF score for each word in each document.
3.  **Searching**: The `search` function takes a string query, splits it into individual words, and finds the corresponding entries in the loaded inverted index. It identifies articles that contain all the query terms by intersecting the document sets and sums their TF-IDF scores to rank the results by relevance.

## Modules

-   `news-web-similarity.py`: The main script that orchestrates the index building, saving/loading, and searching functionalities.
-   `document_classification_tf_idf.py`: A supplementary script demonstrating the use of TF-IDF and cosine similarity for classifying entire document collections (using the 20 Newsgroups dataset).
-   `/newsweb`: The Scrapy project directory containing the spiders and configuration for web crawling.

## Usage

1.  **Run the Scrapers (Optional - if you need to gather new data):**
    ```bash
    cd newsweb
    scrapy crawl Bbc -o bbc_articles.json
    scrapy crawl Articles -o usa_today_articles.json
    ```

2.  **Build and Search the Index:**
    The `news-web-similarity.py` script can be run directly. It will:
    -   Build the inverted index from `.json` files in its directory.
    -   Save the index to `inverted_index.xml`.
    -   Load the index back from the XML file.
    -   Perform a sample search for the query "google" and print the results.
    -   Run a small benchmark to time query performance.

    ```python
    # Example usage within the script
    inverted_index = read_xml('inverted_index.xml')
    results = search("your query here", inverted_index)
    print_dict(results)
    ```

## Dependencies

-   Scrapy
-   NLTK
-   Scikit-learn
-   NumPy


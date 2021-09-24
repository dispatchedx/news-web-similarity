import json
import math
import time
import os


def build_from_scrapy(files=None):
    """
    Build inverted index from json scrapy results
    If no files are given, it takes all json files from current dir
    :param files: a list of filenames
    :return: inverted index
    """
    # Load scrapy resulsts
    site_list = []
    # if no file names given, get all json files from current directory
    if files is None:
        files = [entry for entry in os.listdir('.') if entry.endswith('.json')]

    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
        site_list.append(data)
    N = sum(len(site) for site in site_list)
    print(f'Loading {N} data')  # is the number of articles scraped

    # todo implement with defaultdict prob better
    inverted_index = {}
    # count #number of articles that contain the word aka term frequency
    for site in site_list:
        for articles_dict in site:
            for url, article in articles_dict.items():
                for word in article:

                    if word in inverted_index:
                        inverted_index[word]['count'] += 1
                    else:
                        inverted_index[word] = {}
                        inverted_index[word]['count'] = 1

    # calculate tf-idf
    for site in site_list:
        for articles_dict in site:
            for url, article in articles_dict.items():
                for word, count in article.items():
                    tf = count
                    idf = math.log(N / (inverted_index[word]['count']))
                    inverted_index[word][url] = tf * idf
    print(f'Loaded {N} data')
    return inverted_index

def write_to_xml(fname, inverted_index):
    """
    Saves inverted index as an xml file
    :param fname: string, filename
    :param inverted_index: structured as: word {'doc_url' : 'tf_idf'}
    prints a success message
    """
    with open(fname, 'w', encoding="utf-8") as f:
        f.write("<inverted_index>\n")
        for word, more in inverted_index.items():
            if 'count' in more:  # del count key if exists
                del more['count']
            f.write(f'<lemma name="{word}''">\n')
            for url, tf_idf in more.items():
                f.write(f'<document id="{url}" weight="{tf_idf}"/>\n')
            f.write('</lemma>\n')
        f.write("</>\n</>")
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"Saved inverted index to C:\\Users\\DX\\PycharmProjects\\news-web-similarity\\inverted_index.xml")


def read_xml(fname):
    """
    Read xml file from current directory as dictionary
    :param fname: string, file name to read
    :return: inverted index, structured as: word { 'url' : 'tf_idf'}
    """
    with open(fname, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    inverted_index = {}
    for line in lines:
        if 'lemma name' in line:
            # Extract word
            word = line[13:-3]
            inverted_index[word] = {}
        if 'document id' in line:
            # Extract url and tf_idf from the line
            line = line.split('"')
            url = line[1]
            tf_idf = line[3]
            inverted_index[word].update({url: tf_idf})
    print(f'file {fname} loaded containing {len(inverted_index)} indexes')
    return inverted_index


def print_dict(d):
    """
    Prints a dictionary in a human friendly way (horizontally)
    :param d: a dictionary
    """
    for k, v in d.items():
        print(k, v)
    print('\n')


def search(query, inverted_index):
    """
    Searches for lemmas in an inverted index and returns the links and tf_idf values of the articles containing them.
    Usage:  inverted_index = read_xml('inverted_index.xml')
            search("word1 word2", inverted_index)
    :param query: a string, user input
    :param inverted_index: an inverted index
    :return: dictionary of structure {url:tf_idf}, sorted by tf_idf
    """
    # Split string into words
    words = query.split()
    urls = []  # list of dictionaries of dictionaries of structure {url:tf_idf}
    for word in words:
        if word in inverted_index:
            # append each word's urls and their respective tf_idf values
            urls.append(inverted_index[word])

    PLS = urls[0]  # dictionary containing the first word's articles
    for dictionary in urls[1:]:
        # compare each word's articles to the first one
        # this line intersects 2 dictionaries and adds their values
        # meaning it keeps the articles that contain both words and sums their tf_idf values
        PLS = {k: float(PLS.get(k, 0)) + float(dictionary.get(k, 0)) for k in set(PLS) & set(dictionary)}
    # Sort dictionary by tf_idf values, descending
    return dict(sorted(PLS.items(), key=lambda item: item[1], reverse=True))


def timeth(query, times, inverted_index):
    """
    Prints time average time elapsed for an inverted index query search
    :param query: string, lemmas to search
    :param times: int, times to repeat
    :param inverted_index: inverted index
    :return:
    """
    start = time.time()
    for i in range(times):
        search(query, inverted_index)
    end = time.time()
    print(f'Average time of Query:"{query}" for {times} times: {(end-start)/times}')


# Build inverted index from scrapy json files
inverted_index = build_from_scrapy(['newsweb/articles.json', 'newsweb/articles2.json'])

# Save inverted index to xml file
write_to_xml('inverted_index.xml', inverted_index)

# Or can directly load an xml file
inverted_index = read_xml('inverted_index.xml')
# Search query
result = search("google", inverted_index)

# Print result in a human friendly way
print_dict(result)

# Example timings
timeth("is", 20, inverted_index)
timeth("is have", 20, inverted_index)
timeth("is have man", 30, inverted_index)
timeth("is is have man google", 30, inverted_index)


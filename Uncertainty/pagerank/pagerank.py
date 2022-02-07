import os
import random
import re
import sys
from fractions import Fraction

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"\n\nPageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability = dict()
    sort = random.random()
    p = round((1-damping_factor)/len(corpus), 4)
    for keys in corpus:
        probability[keys] = p
        
    if corpus[page] == None or corpus[page] == 0:
        for keys in corpus:
            probability[keys] = 1/len(corpus)
        return probability
    
    if sort <= damping_factor:
        pages = corpus[page]
        
        if len(pages) != 0:
            pb = damping_factor/len(pages)
        else:
            for keys in corpus:
                probability[keys] = 1/len(corpus)
            return probability
        for i in pages:
            probability[i] += pb
            
    return probability
        
def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    list_corpus = list(corpus.items())
    page = random.choice(list_corpus)[0]
    count = dict()
    result = dict()
    
    for keys in corpus:
        count[keys] = 0
    keys = []
    
    for _ in range(n):
        count[page] += 1
        next_transitions = transition_model(corpus, page, damping_factor)
        items = list(next_transitions.items())
        for i in next_transitions:
            keys.append(next_transitions[i])
            
        selection_probability = [next_transitions[i] for i in next_transitions.keys()]
        x = [(selection_probability[i]/sum(selection_probability)) for i in range(len(selection_probability))]
        i = 0
        r = random.random()
        sums = x[i]
        while sums < r:
            i += 1
            sums += x[i]
        page = items[i][0]
        
    for keys in count:
        result[keys] = (count[keys]/n) 
    
    return result          

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = dict()
    N = len(corpus)
    keys_corpus = []
    for keys in corpus.keys():
        pages[keys] = 1/N
        keys_corpus.append(keys)
    
    for pag in corpus:
        if corpus[pag] == set():
            corpus[pag] = set(corpus.keys())
                
    condition = True
    while condition:
        for page in pages:
            page_rank = [x for x in corpus if page in corpus[x]]
            summation = [pages[i]/len(corpus[i]) for i in page_rank]
            sums = sum(summation)
            aux = (1-damping_factor)/N + (damping_factor*sums)
            
            if round((pages[page]-aux), 3) == 0.001:
                condition = False
            pages[page] = aux
            
    return pages

if __name__ == "__main__":
    main()

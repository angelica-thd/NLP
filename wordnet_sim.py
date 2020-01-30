# wordnet similarity 

from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag
from decimal import Decimal


def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
    

def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
        
        
        
        
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
    
    score, count = 0.0, 0
 
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = 0
        for ss in synsets2:
            pathsim = synset.path_similarity(ss)
            if(pathsim != None):
                if(best_score < pathsim):
                    best_score = pathsim
        # Check that the similarity could have been computed
        if best_score is not None:
            if best_score > score:
                score = best_score	
        #if best_score is not None:
            #score += best_score
            #count += 1
 
    # Average the values
    #if(count != 0):
        #score /= count
    return score
    

def preprocess(text):
    title_list = []
    for t in text:
        title = t['title']
        title = title.split('.')
        for ti in title:
            title_list.append(ti)
    return title_list


def compute_score(text, words):
    score = 0
    if(len(text) == 0):
        return 0
    #print(text[1])
    for t in text:
        for w in words:
            score += sentence_similarity(t, w)
    score /= len(text)
    return score
    



def similarity(text):
    print(len(text))

    # compute individual scores
    yo = compute_score(text, openness)
    no = compute_score(text, n_openness)
    
    yc = compute_score(text, conscientiousness)
    nc = compute_score(text, n_conscientiousness)

    ye = compute_score(text, extraversion)
    ne = compute_score(text, n_extraversion)

    ya = compute_score(text, agreeableness)
    na = compute_score(text, n_agreeableness)

    yn = compute_score(text, neuroticism)
    nn = compute_score(text, n_neuroticism)

    print("o: " + str(yo) + " " + str(no))
    print("c: " + str(yc) + " " + str(nc))
    print("e: " + str(ye) + " " + str(ne))
    print("a: " + str(ya) + " " + str(na))
    print("n: " + str(yn) + " " + str(nn))

    o = (yo-no)/2 + 0.5
    c = (yc-nc)/2 + 0.5
    e = (ye-ne)/2 + 0.5
    a = (ya-na)/2 + 0.5
    n = (yn-nn)/2 + 0.5
    

    score_list = []
    score_list.append(round(Decimal(o*100),2))
    score_list.append(round(Decimal(c*100),2))
    score_list.append(round(Decimal(e*100),2))
    score_list.append(round(Decimal(a*100),2))
    score_list.append(round(Decimal(n*100),2))
    return(score_list)





openness   = ['open', 'curious', 'inventive', 'acceptance', 'tolerance', 'interest', 'new', 'unconventional', 'risky']
n_openness = ['restricted', 'incurious', 'disinterested', 'disbelief', 'intolerance', 'conventional', 'safe']

conscientiousness   = ['efficient', 'organized', 'dutiful', 'upright', 'exact', 'reliable', 'discipline', 'methodical']
n_conscientiousness = ['inefficient', 'unorganized', 'undutiful', 'loose', 'imprecise', 'fuzzy', 'chaotic']

extraversion      = ['extrovert', 'outgoing', 'energetic', 'communicable', 'unreserved', 'social']
n_extraversion    = ['introvert', 'shy', 'restrained', 'collected', 'cautious', 'uncommunicative']

agreeableness     = ['friendly', 'compassionate', 'pleasant']
n_agreeableness   = ['unfriendly', 'harsh', 'unpleasant', 'hard']

neuroticism       = ['sensitive', 'nervous', 'obsessive', 'hysteric', 'anxious', 'nervous', 'unstable']
n_neuroticism     = ['adjusted', 'balanced', 'stable']


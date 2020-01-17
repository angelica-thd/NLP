# wordnet similarity 

from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag


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
            score += best_score
            count += 1
 
    # Average the values
    if(count != 0):
        score /= count
    return score
    

def preprocess(text):
    title_list = []
    for t in text:
        title_list.append(t['title'])
        print(t['title'])
    return title_list


def compute_score(text, words):
    score = 0
    for t in text:
        for w in words:
            score += sentence_similarity(t, w)
    return score
    



def similarity(text):

    score_list = []
    score_list.append(compute_score(text, openness))
    score_list.append(compute_score(text, conscientiousness))
    score_list.append(compute_score(text, extraversion))
    score_list.append(compute_score(text, agreeableness))
    score_list.append(compute_score(text, neuroticism))
    return(score_list)





openness          = ['open', 'curious', 'inventive']
conscientiousness = ['efficient', 'organized']
extraversion      = ['outgoing', 'energetic']
agreeableness     = ['friendly', 'compassionate']
neuroticism       = ['sensitive', 'nervous']


    
'''sentences = [
    "I like to study.",
    "I am very open and like to go out.",
    "I think I am very nice.",
    "I am very stressed out.",
]
 
openness = "open"
conscientiousness = "study"
extraversion = "outgoing"
agreeableness = "nice"
neuroticism = "neurotic"
 
for sentence in sentences:
    print("Similarity(\"%s\", \"%s\") = %s" % (openness, sentence, sentence_similarity(openness, sentence)))
    print("Similarity(\"%s\", \"%s\") = %s" % (conscientiousness, sentence, sentence_similarity(conscientiousness, sentence)))
    print("Similarity(\"%s\", \"%s\") = %s" % (extraversion, sentence, sentence_similarity(extraversion, sentence)))
    print("Similarity(\"%s\", \"%s\") = %s" % (agreeableness, sentence, sentence_similarity(agreeableness, sentence)))
    print("Similarity(\"%s\", \"%s\") = %s" % (neuroticism, sentence, sentence_similarity(neuroticism, sentence)))
    print("\n")'''


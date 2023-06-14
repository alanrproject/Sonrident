import re, math
# from textblob import Word
# from textblob import TextBlob

# def check_spelling(word):

#     word = Word(word)
#     result = word.spellcheck()
#     if word == result[0][0]:
#         return word
#     else:
#         return result[0][0]


# def get_correct_name(sentence):

#     words = sentence.split()
#     words = [word.lower() for word in words]
#     words = [re.sub(r'[^A-Za-z0-9]+', '', word) for word in words]
#     for word in words:
#         check_spelling(word)
#     return words[1:]



from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
    # print vec1, vec2
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

def text_to_vector(text):
    return Counter(WORD.findall(text))

def get_similarity(a, b):
    a = text_to_vector(a.strip().lower())
    b = text_to_vector(b.strip().lower())

    return get_cosine(a, b)

n = get_similarity('DRA SARA CAÑAS', 'DRA CAÑAS')
print(n) # returns 0.9258200997725514
print(type(n))
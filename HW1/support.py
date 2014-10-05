import re

def is_russian(word):
    return False if re.search('[^а-яё]', word) or not word else True


def to_word(string):
    word = re.sub('^[^ а-яА-Я]*', "", string)
    word = re.sub('[^ а-яА-Я]*$', "", word)
    return word.lower()


def parse_request(string):
    request = re.sub('[^ а-яА-Я(AND)(OR)]', "", string)
    is_AND = True if re.search('(AND)', request) else False
    is_OR  = True if re.search('(OR)', request) else False
    if is_OR and is_AND:
        return None
    request = re.sub('(OR)', "!", request)
    request = re.sub('(AND)', "!", request)
    ls = request.strip().split()
    ind = True
    word_ls = []
    for i in ls:
        if ind:
            if i.strip() is '!':
                return None
            word_ls.append(to_word(i).strip())
        else:
            if not i.strip() is '!':
                return None
        ind = not ind
    if ind:
        return None

    return (is_AND, word_ls)

def get_docs(dict, request, is_AND):
    if is_AND:
        first_time = True
        for i in request:
            if i not in dict:
                return set()
            if first_time:
                res = dict[i]
                first_time = not first_time
            else:
                res = res & dict[i]
    else:
        res = set()
        for i in request:
            if i not in dict:
                return set()
            res = res | dict[i]
    return res
import random
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sentencebot"
)

mycursor = mydb.cursor()

plural_subject_pronouns = ["I","they","you"]
singular_subject_pronouns = ["he","she","it"]
object_pronouns = ["me","him","her","it","them"]
plain_auxilary_verbs = ["have","should","can"]
plural_auxilary_verbs = ["has","should","can"]
past_auxilary_verbs = ["had","should","could"]
required_adjectives = ["the","a","my"]
prepositions = ["in","out","up","down","around","under","above","through"]
conjunctions = ["and","or","if","so","but"]

word_types = {
    "plain_noun": [],
    "plural_noun": [],
    "plain_verb": [],
    "plural_verb": [],
    "past_verb": [],
    "present_verb": [],
    "object_plain_verb": [],
    "object_plural_verb": [],
    "object_past_verb": [],
    "object_present_verb": [],
    "_plain_verb": [],
    "object_plural_verb": [],
    "object_past_verb": [],
    "object_present_verb": [],
    "adjective": [],
    "adverb": [],
    "interjection": [],
    "proper_noun": []
}

def fetch_words():
    global word_types
    for word_type in word_types:
        word_types[word_type] = []
        if word_type.startswith("object_"):
            type_query = word_type.removeprefix("object_")
            hasobject_query = "true"
        else:
            type_query = word_type
            hasobject_query = "false"
        mycursor.execute(f"SELECT content FROM Words WHERE type = \"{type_query}\" AND hasobject = {hasobject_query}")
        output = mycursor.fetchall()
        for (word) in output:
            word_types[word_type].append(word[0])

fetch_words()

vowels = "aeiouAEIOU"

def main():
    sentence = create_sentence()
    print(sentence)

def create_sentence():
    num = random.randrange(50)
    if num == 0:
        return random.choice(word_types["interjection"])
    else:
        (subject,pluralsubject) = add_subject()
        predicate = add_predicate(pluralsubject)
        return f"{subject} {predicate}"

def get_adjectives():
    adjectives = ""
    num = random.randrange(3)
    while (num == 0):
        adjectives += random.choice(word_types["adjective"])
        adjectives += " "
        num = random.randrange(3)
    return adjectives

def plural_noun():
    noun = random.choice(word_types["plural_noun"])
    adjectives = get_adjectives()
    required_adjective = ""
    num = random.randrange(2)
    if num == 0:
        required_adjective = "the "
    return f"{required_adjective}{adjectives}{noun}"

def singular_noun():
    noun = random.choice(word_types["plain_noun"])
    adjectives = get_adjectives()
    required_adjective = random.choice(required_adjectives)
    if (required_adjective == "a" and noun[0] in vowels):
        required_adjective = "an"
    return f"{required_adjective} {adjectives}{noun}"

def plural_pronoun_subject():
    return random.choice(plural_subject_pronouns)

def proper_noun():
    return random.choice(word_types["proper_noun"])

def singular_pronoun_subject():
    return random.choice(singular_subject_pronouns)

def pronoun_object():
    return random.choice(object_pronouns)

def add_subject():
    num = random.randrange(50)
    if num >= 0 and num < 11:
        return (plural_noun(),True)
    elif num >= 11 and num < 22:
        return (singular_noun(),False)
    elif num >= 22 and num < 33:
        return (plural_pronoun_subject(),True)
    elif num >= 33 and num < 44:
        return (singular_pronoun_subject(),False)
    else:
        return (proper_noun(),False)

def add_object():
    num = random.randrange(5)
    if num == 0:
        return plural_noun()
    if num == 1 or num == 2:
        return singular_noun()
    else:
        return pronoun_object()

def random_verb(verbtype) -> tuple[str,bool]:
    index = random.randrange(len(word_types[verbtype])+len(word_types["object_"+verbtype]))
    if index < len(word_types[verbtype]):
        return (word_types[verbtype][index],False)
    else:
        return (word_types["object_"+verbtype][index-len(word_types[verbtype])],True)

def verb_phrase(pluralsubject):
    num = random.randrange(2)
    if num == 0 and pluralsubject:
        (verb,hasobject) = random_verb("plain_verb")
    elif num == 0 and not pluralsubject:
        (verb,hasobject)= random_verb("plural_verb")
    else:
        (verb,hasobject)= random_verb("past_verb")
    return (f"{verb}",hasobject)

def add_predicate(pluralsubject):
    (predicate,hasobject) = verb_phrase(pluralsubject)
    if (hasobject):
        predicate += " "
        predicate += add_object()
    num = random.randrange(2)
    if (num == 0):
        predicate += " "
        predicate += add_preposition()
    return predicate



def add_preposition():
    preposition = ""
    preposition += random.choice(prepositions)
    preposition += " "
    currentobject = add_object()
    preposition += currentobject
    return preposition

if __name__ == "__main__":
    main()

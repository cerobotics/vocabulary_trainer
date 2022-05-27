from tinydb import TinyDB, Query
import os
from termcolor import colored

os.system('color')

db = TinyDB('ge_db.json')

Terms = Query()  # type: tinydb.queries.Query


def insert_terms():
    db.insert({'term': 'Saft', 'analogy': ['juice', 'crush', 'liquor', 'sap']})
    db.insert({'term': 'laufen', 'analogy': ['to run', 'to walk', 'to go', 'to operate', 'to be in process']})
    db.insert({'term': 'Anspruchsvoll', 'analogy': ['discerning', 'ambitious', 'sophisticated', 'demanding',
                                                    'pretentious']})
    db.insert({'term': 'beleidigen', 'analogy': ['to insult', 'to flout', 'to affront', 'to offend', 'to slight',
                                                 'to flame', 'to diss']})
    db.insert({'term': 'dennoch', 'analogy': ['anyhow']})
    db.insert({'term': 'etwas schaffen', 'analogy': ['to accomplish']})
    db.insert({'term': 'echt', 'analogy': ['legit']})
    db.insert({'term': 'erklären', 'analogy': ['to assert']})


def get_db_length():
    return len(db)


def get_all_ids():
    print(db.all[0])


def search_term(term: object):
    result = db.search(Terms.term == term)
    if result:
        return result
    else:
        print(colored("WARNING: Term not found in DB"))
        return result


def add_term(term: object, analogy: object):
    if not db.search(Terms.term == term):
        db.insert(dict(term=term, analogy=analogy))
        print("Term:" + term + " analogy: " + str(analogy) + "was added to the database successfully.")
    else:
        print(colored("WARNING: Already there", "red"))


def delete_user():
    db.remove(Terms.term == 'John')
    # db.purge() # remove all


#### TESTS ####

# db.drop_tables() # empty db

# insert_terms()
# add_term('echt', ['legit'])
# search_user()
# update_user()
# delete_user()
# update_by_document_id()

print(db.all())
print("length" + str(len(db)))
# for item in db:
#     print(item)
# print(len(db)) # number of items

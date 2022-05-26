from tinydb import TinyDB, Query

db = TinyDB('german_english_db.json')

User = Query()  # type: tinydb.queries.Query


def insert_user():
    db.insert({'term': 'Saft', 'analogy': ['juice', 'crush', 'liquor', 'sap']})
    db.insert({'term': 'laufen', 'analogy': ['to run', 'to walk', 'to go', 'to operate', 'to be in process']})
    db.insert({'term': 'Anspruchsvoll', 'analogy': ['discerning', 'ambitious', 'sophisticated', 'demanding',
                                                    'pretentious']})


#def create_trainings_set():
#

def search_user():
    results = db.search(User.city == 'New York')  # returns a list
    for res in results:
        print(res)  # type: tinydb.database.Document
        # print(res.city) # Not allowed!
        print(res['city'])

    results = db.search(User.age > 21)
    for res in results:
        print(res)


def update_user():
    db.update({'age': 26}, User.name == 'Max')
    for item in db:
        print(item)

    # or
    results = db.search(User.name == 'Max')
    for res in results:
        res['age'] = 27
    db.write_back(results)  # write back results we retrieved

    # or get and update/remove by document_id


def delete_user():
    db.remove(User.name == 'John')
    # db.purge() # remove all


def update_by_document_id():
    # db.remove(doc_ids=[2])
    # this will not create doc_id=2, but the next highest number
    # db.insert({'name': 'Jason', 'age': 40})

    item = db.get(doc_id=3)
    print(item)
    print(item.doc_id)

    db.update({'city': 'Boston'}, doc_ids=[1, 2])

    # db.remove(doc_ids=[1, 2])


#### TESTS ####

# db.purge() # empty db

insert_user()
# search_user()
# update_user()
# delete_user()
# update_by_document_id()

print(db.all())
# for item in db:
#     print(item)
# print(len(db)) # number of items

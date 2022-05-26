from tinydb import TinyDB, Query

db = TinyDB('user_db.json')

User = Query()  # type: tinydb.queries.Query


def insert_user():
    db.insert({'name': "default", 'number_correct_terms': 0, 'box1': [], 'box2': [], 'box3': [], 'box4': [], 'box5': [], 'experience': 0})
    db.insert({'name': "test", 'number_correct_terms': 0, 'box1': [], 'box2': [], 'box3': [], 'box4': [], 'box5': [],
               'experience': 0})


def add_to_box(user_name, box_number, card_index):
    results = db.search(User.name == user_name)
    box_name = 'box'+str(box_number)
    for res in results:
        box = res[box_name]
    box.append(card_index)
    db.update({box_name: box}, User.name == user_name)


def remove_from_box(user_name, box_number, card_index):
    results = db.search(User.name == user_name)
    box_name = 'box'+str(box_number)
    for res in results:
        box = res[box_name]
    box.remove(card_index)
    db.update({box_name: box}, User.name == user_name)


def search_boxes(user_name):
    results = db.search(User.name == user_name)
    for res in results:
        indexes_box1 = res['box1']
        indexes_box2 = res['box2']
        indexes_box3 = res['box3']
        indexes_box4 = res['box4']
        indexes_box5 = res['box5']
    return indexes_box1, indexes_box2, indexes_box3, indexes_box4, indexes_box5


def increase_number_correct_terms(user_name):
    results = db.search(User.name == user_name)
    for res in results:
        current_number = res['number_correct_terms']
    new_number = current_number + 1
    db.update({'number_correct_terms': new_number}, User.name == user_name)


def update_experience(user_name, gained_exp):
    results = db.search(User.name == user_name)
    for res in results:
        current_exp = res['experience']
    new_exp = current_exp + gained_exp
    db.update({'experience': new_exp}, User.name == user_name)


def search_user():
    results = db.search(User.city == 'New York')  # returns a list
    for res in results:
        print(res)  # type: tinydb.database.Document
        # print(res.city) # Not allowed!
        print(res['city'])

    results = db.search(User.age > 21)
    for res in results:
        print(res)




def delete_user():
    db.remove(User.name == 'John')
    # db.purge() # remove all


#### TESTS ####


db.drop_tables() # empty db


insert_user()
update_experience('test', 10)
increase_number_correct_terms('test')
add_to_box('test', 1, 2367)
add_to_box('test', 1, 234)
add_to_box('test', 1, 555)
add_to_box('test', 2, 1234)
add_to_box('test', 3, 999)
add_to_box('test', 4, 2341)
add_to_box('test', 5, 222)
remove_from_box('test', 1, 234)

# search_user()
#update_user()
print(search_boxes('test'))
# delete_user()
# update_by_document_id()

print(db.all())
# for item in db:
#     print(item)
# print(len(db)) # number of items
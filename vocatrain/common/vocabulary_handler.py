import json
import random
import codecs
from vocatrain.common import db_worker
from vocatrain.common import user_db_worker


def add_if_possible(training_set: object, number: object, box: object) -> object:
    if len(box) > number:
        training_set.append(box[number])
        print("Added index [ " + str(number) + " ] to training_set " + str(box))
    return training_set


class VocabularyHandler:
    """
    Class to create training sets from dictionary and validate answers

    Attributes
    -------------
    data : dict
        the full dictionary initially loaded from file


    Methods
    ----------
    create_training_set()
        creates a new training set as list

    get_next_term()
        offers a new training term

    validate_entry(question_term, input, active_language)
        checks if the input is the correct answer to the question_term and


    """
    def __init__(self):
        """ Loads the dictionary from file """
        self.data = {}
        with codecs.open("data.json", 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.training_data = []

    def create_user_training_set(self, user_name, size, language):
        """ Creates a new training set for a specific user , size and language."""
        training_set = []
        all_terms = db_worker.get_all_ids()
        print("---------- all terms ------------")
        print(all_terms)
        box0, box1, box2, box3, box4, box5 = user_db_worker.search_boxes(user_name)
        print("user_boxes")
        print("Box 0: " + str(box0) + " len: " + str(len(box0)))
        print("--------------------")
        print("Box 1: " + str(box1) + " len: " + str(len(box1)))
        print("--------------------")
        print("Box 2: " + str(box2) + " len: " + str(len(box2)))
        print("--------------------")
        print("Box 3: " + str(box3) + " len: " + str(len(box3)))
        print("--------------------")
        print("Box 4: " + str(box4) + " len: " + str(len(box4)))
        print("--------------------")
        print("Box 5: " + str(box5) + " len: " + str(len(box5)))
        print("--------------------")
        # chose 1 next card from box5 (if there is one)
        add_if_possible(training_set=training_set, number=0, box=box5)
        add_if_possible(training_set=training_set, number=0, box=box4)
        add_if_possible(training_set=training_set, number=1, box=box4)
        add_if_possible(training_set=training_set, number=0, box=box3)
        add_if_possible(training_set=training_set, number=1, box=box3)
        add_if_possible(training_set=training_set, number=2, box=box3)
        add_if_possible(training_set=training_set, number=0, box=box2)
        add_if_possible(training_set=training_set, number=1, box=box2)
        add_if_possible(training_set=training_set, number=2, box=box2)
        add_if_possible(training_set=training_set, number=3, box=box2)
        add_if_possible(training_set=training_set, number=0, box=box1)
        add_if_possible(training_set=training_set, number=1, box=box1)
        add_if_possible(training_set=training_set, number=2, box=box1)
        add_if_possible(training_set=training_set, number=3, box=box1)
        add_if_possible(training_set=training_set, number=4, box=box1)
        # find out how many cards are in the training_set
        number_cards = len(training_set)
        print("Number of cards in training set before: " + str(number_cards))
        cards_to_add = 20 - number_cards
        print("Cards to add: "+str(cards_to_add))
        for i in range(cards_to_add):
            add_if_possible(training_set=training_set, number=i, box=box0)

        number_cards = len(training_set)
        print("Number of cards in training set after: " + str(number_cards))
        random.shuffle(training_set)
        print("Training set: "+str(training_set))
        return training_set

    def create_training_set(self):
        """ Creates a new training set as list. """
        for element in self.data['language']['dictionary']:
            self.training_data.append(element['term'])
        random.shuffle(self.training_data)

    def get_next_term(self):
        """ Returns the last term in training set list"""
        # check list is empty
        if not self.training_data:
            self.create_training_set()

        return self.training_data.pop()

    def validate_entry(self, question_term, input_term, active_language):
        """ Validates the input against the correct term in dictionary

        Parameters
        ----------

        question_term : str
            The questioned term the user must translate

        input_term : str
            The users input as guessed answer to the question

        active_language : str
            The activ language the user works in
        """
        correct_answer = ""
        for element in self.data['language']['dictionary']:
            if element['term'] == question_term:
                for link in element['links']:
                    if link['language'] == active_language:
                        correct_answer = link['term']
                        if correct_answer == input_term:
                            return True, correct_answer

        return False, correct_answer

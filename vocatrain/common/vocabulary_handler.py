import json
import copy
import random


class VocabularyHandler():
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
        with open("data.json", 'r') as f:
            self.data = json.load(f)

    def create_training_set(self):
        """ Creates a new training set as list. """
        self.training_data = []
        for element in self.data['language']['dictionary']:
            self.training_data.append(element['term'])
        random.shuffle(self.training_data)

    def get_next_term(self):
        """ Returns the last term in training set list"""
        # check list is empty
        if not self.training_data:
            self.create_training_set()

        return self.training_data.pop()

    def validate_entry(self, question_term, input, active_lanuage):
        """ Validates the input against the correct term in dictionary

        Parameters
        ----------

        question_term : str
            The questioned term the user must translate

        input : str
            The users input as guessed answer to the question

        active_language : str
            The activated language the user works in
        """
        correct_answer = ""
        for element in self.data['language']['dictionary']:
            if element['term'] == question_term:
                for link in element['links']:
                    if link['language'] == active_lanuage:
                        correct_answer = link['term']
                        if correct_answer == input:
                            return True, correct_answer

        return False, correct_answer

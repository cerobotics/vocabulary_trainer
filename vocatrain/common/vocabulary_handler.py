import json
import random
import codecs
import vocatrain.common.db_worker as dbworker

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
        with codecs.open("data.json", 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.training_data = []


    def create_user_training_set(self, user_name, size, language):
        """ Creates a new training set for a specific user , size and language."""
        all_terms = db_worker.all()

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

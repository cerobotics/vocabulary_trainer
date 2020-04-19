import json
import copy
import random


class VocabularyHandler():
    def __init__(self):
        self.data = {}
        with open("data.json", 'r') as f:
            self.data = json.load(f)

    def create_training_set(self):
        self.training_data = []
        for element in self.data['language']['dictionary']:
            self.training_data.append(element['term'])
        random.shuffle(self.training_data)

    def get_next_term(self):
        # check list is empty
        if not self.training_data:
            self.create_training_set()

        return self.training_data.pop()

    def validate_entry(self, question_term, input, active_lanuage):
        correct_answer = ""
        for element in self.data['language']['dictionary']:
            if element['term'] == question_term:
                for link in element['links']:
                    if link['language'] == active_lanuage:
                        correct_answer = link['term']
                        if correct_answer == input:
                            return True, correct_answer

        return False, correct_answer


if __name__ == "__main__":
    vh = VocabularyHandler()
    vh.create_training_set()
    for i in range(15):
        print(vh.get_next_term())

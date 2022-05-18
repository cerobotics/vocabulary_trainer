# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font as tkfont
from vocatrain.common.vocabulary_handler import VocabularyHandler


class VocabularyGUI(tk.Tk, VocabularyHandler):
    def __init__(self):
        tk.Tk.__init__(self)
        VocabularyHandler.__init__(self)

        self.title_font = tkfont.Font(
            family='eurlatgr', size=14, weight="bold")

        self.active_language = "German"
        self.mode = "start"
        self.active_term = ""

        # create menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        config_menu = tk.Menu(self.menubar, tearoff=0)
        config_menu.add_command(label="Exit", command=self.destroy)
        config_menu.add_separator()
        config_menu.add_command(
            label="German", command=self.change_to_german)
        config_menu.add_command(
            label="Spanish", command=self.change_to_spanish)
        self.menubar.add_cascade(label="Config", menu=config_menu)
        self.menubar.add_cascade(label="Active Language is English -> German")

        self.label_question = tk.Label(
            self, width=40, text="", font=self.title_font)
        self.label_question.pack(side="top", expand=True, fill=tk.X)

        self.entry_response = tk.Entry(
            self, font=self.title_font, justify="center")
        self.entry_response.pack(side="top", expand=True, fill=tk.X)

        self.label_validation = tk.Label(
            self, font=self.title_font, text=""
        )
        self.label_validation.pack(side="top", expand=True, fill=tk.X)

        self.label_answer = tk.Label(
            self, font=self.title_font,
            text="")
        self.label_answer.pack(side="top", expand=True, fill=tk.X)

        self.submit_button = tk.Button(
            self, font=self.title_font, text="start",
            command=self.submit_response)
        self.submit_button.pack(side="top", expand=True, fill=tk.X)

    def reset_form(self):
        self.label_question.configure(text="")
        self.label_validation.configure(text="")
        self.entry_response.delete(0, tk.END)
        self.label_answer.configure(text="")

    def change_to_german(self):
        self.active_language = "German"
        self.mode = "start"
        self.active_term = ""
        self.reset_form()
        self.menubar.entryconfigure(
            2, label="Active Language is English -> German")

        self.submit_button.configure(text="start")

    def change_to_spanish(self):
        self.active_language = "Spanish"
        self.mode = "start"
        self.active_term = ""
        self.reset_form()
        self.menubar.entryconfigure(
            2, label="Active Language is English -> Spanish")

        self.submit_button.configure(text="start")

    def submit_response(self):
        if (self.mode == "start"):
            self.mode = "submit"
            self.submit_button.configure(text="submit")
            self.create_training_set()
            self.active_term = self.get_next_term()
            self.label_question.configure(text=self.active_term)
        elif (self.mode == "submit"):
            self.submit_button.configure(text="next")
            self.mode = "next"
            correctness, correct_answer = self.validate_entry(
                self.active_term, self.entry_response.get(),
                self.active_language)
            if (correctness):
                self.label_validation.configure(
                    text="correct", foreground="green")
            else:
                self.label_validation.configure(text="wrong", foreground="red")
                self.label_answer.configure(text=correct_answer)
        elif (self.mode == "next"):
            self.mode = "submit"
            self.submit_button.configure(text="submit")
            self.reset_form()
            self.active_term = self.get_next_term()
            self.label_question.configure(text=self.active_term)

        else:
            print("Error")

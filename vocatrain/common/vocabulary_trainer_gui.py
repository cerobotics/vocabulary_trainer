# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font as tkfont
from vocatrain.common.vocabulary_handler import VocabularyHandler
import vocatrain.common.user_db_worker as udbw
import vocatrain.common.db_worker as dbworker
import os
from termcolor import colored

os.system('color')


class VocabularyGUI(tk.Tk, VocabularyHandler):
    training_progress: int

    def __init__(self):
        tk.Tk.__init__(self)
        VocabularyHandler.__init__(self)

        self.title_font = tkfont.Font(
            family='eurlatgr', size=14, weight="bold")
        self.settings_font = tkfont.Font(
            family='eurlatgr', size=8)

        self.active_user = "test"
        self.active_language = "German"
        self.mode = "start"
        self.active_term = ""
        self.all_active_analogies = ""
        self.training_set = []
        self.training_set_size = 20
        self.training_progress = 0
        self.number_db_entries = dbworker.get_db_length()

        # create menu bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        config_menu = tk.Menu(self.menubar, tearoff=0)
        config_menu.add_command(label="Exit", command=self.destroy)
        config_menu.add_separator()
        config_menu.add_command(
            label="start", command=self.change_to_start)
        config_menu.add_command(
            label="edit", command=self.change_to_edit)
        config_menu.add_command(
            label="new", command=self.change_to_new)
        config_menu.add_command(
            label="remove", command=self.change_to_remove)
        config_menu.add_separator()
        config_menu.add_command(
            label="German", command=self.change_to_german)
        config_menu.add_command(
            label="Spanish", command=self.change_to_spanish)
        self.menubar.add_cascade(label="Config", menu=config_menu)

        self.entry_question = tk.Entry(
            self, width=40, font=self.title_font, justify="center", state="disabled")
        self.entry_question.pack(side="top", expand=True, fill=tk.X)

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
            self, font=self.title_font, text="start", command=self.submit_response)
        self.submit_button.bind('<Return>', lambda evt: self.submit_response())
        self.submit_button.focus_set()
        self.submit_button.pack(side="top", expand=True, fill=tk.X)
        self.text_settings = tk.Text(
            self, font=self.settings_font, height=8)

        self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode +
                                  ";\nActive language: " + self.active_language + ";\ntraining progress: " +
                                  str(self.training_progress) + ";\nDB entries: " + str(self.number_db_entries) +
                                  ";", "center")
        self.text_settings.tag_configure("center", justify='center')
        self.text_settings.pack(side="top", expand=True, fill=tk.X)

    def reset_form(self):
        self.entry_question.configure(state="normal")
        self.entry_question.delete(0, tk.END)
        self.entry_question.configure(state="disabled")

        self.label_validation.configure(text="")
        self.entry_response.delete(0, tk.END)
        self.label_answer.configure(text="")

    def change_to_german(self):
        self.active_language = "German"
        self.mode = "start"
        self.active_term = ""
        self.reset_form()
        self.submit_button.configure(text="start")
        self.text_settings.delete(1.0, tk.END)
        self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode + ";\nActive language: " +
                                  self.active_language + ";\ntraining progress: " + str(self.training_progress) +
                                  ";\nDB entries: " + str(self.number_db_entries) + ";", "center")

    def change_to_spanish(self):
        self.active_language = "Spanish"
        self.mode = "start"
        self.active_term = ""
        self.reset_form()
        self.submit_button.configure(text="start")
        self.text_settings.delete(1.0, tk.END)
        self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode + ";\nActive language: " +
                                  self.active_language + ";\ntraining progress: " + str(self.training_progress) +
                                  ";\nDB entries: " + str(self.number_db_entries) + ";", "center")

    def change_to_start(self):
        self.mode = "start"
        self.active_term = ""
        self.reset_form()
        self.submit_button.configure(text="start")
        self.create_user_training_set(user_name=self.active_user, size=20, language='english')
        self.text_settings.delete(1.0, tk.END)
        self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode + ";\nActive language: " +
                                  self.active_language + ";\ntraining progress: " + str(self.training_progress) +
                                  ";\nDB entries: " + str(self.number_db_entries) + ";", "center")

    def change_to_edit(self):
        if self.mode == "submit":
            self.mode = "edit"
            self.entry_question.configure(state="normal")
            self.all_active_analogies = dbworker.search_term(self.active_term)
            self.entry_response.insert(0, self.all_active_analogies)
            self.submit_button.configure(text="save")
            self.text_settings.delete(1.0, tk.END)
            self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode + ";\nActive language: " +
                                      self.active_language + ";\ntraining progress: " + str(self.training_progress) +
                                      ";\nDB entries: " + str(self.number_db_entries) + ";", "center")
        else:
            print(colored("WARNING: Switching to edit mode only if in mode: submit", "red"))

    def change_to_new(self):
        self.mode = "new"
        self.entry_question.configure(state="normal")
        self.entry_response.delete(0, tk.END)
        self.submit_button.configure(text="save")
        self.text_settings.delete(1.0, tk.END)
        self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode + ";\nActive language: " +
                                  self.active_language + ";\ntraining progress: " + str(self.training_progress) +
                                  ";\nDB entries: " + str(self.number_db_entries) + ";", "center")

    def change_to_remove(self):
        if self.mode == "submit":
            self.mode = "remove"
            self.submit_button.configure(text="remove")
            self.text_settings.insert(tk.END, "User: " + self.active_user + ";\nMode: " + self.mode + ";\nActive language: " +
                                      self.active_language + ";\ntraining progress: " + str(self.training_progress) +
                                      ";\nDB entries: " + str(self.number_db_entries) + ";", "center")
        else:
            print(colored("WARNING: Switching to remove mode only if in mode: submit", "red"))

    def submit_response(self):
        if self.mode == "start":
            self.mode = "submit"
            self.submit_button.configure(text="submit")
            self.create_training_set()
            self.create_user_training_set(self.active_user, 20, self.active_language)
            self.active_term = self.get_next_term()
            self.entry_question.configure(state="normal")
            self.entry_question.insert(0, self.active_term)
            self.entry_question.configure(state="disabled")
        elif self.mode == "submit":
            correctness, correct_answer = self.validate_entry(
                self.active_term, self.entry_response.get(),
                self.active_language)
            if correctness:
                self.label_validation.configure(
                    text="correct", foreground="green")
                self.submit_button.configure(text="next")
                self.mode = "next"
            else:
                self.label_validation.configure(text="wrong", foreground="red")
                self.label_answer.configure(text=correct_answer)
                self.submit_button.configure(text="next")
                self.mode = "next"
        elif self.mode == "next":
            self.mode = "submit"
            self.submit_button.configure(text="submit")
            self.reset_form()
            self.active_term = self.get_next_term()
            self.entry_question.configure(state="normal")
            self.entry_question.insert(0, self.active_term)
            self.entry_question.configure(state="disabled")
        elif self.mode == "new":
            new_term = self.entry_question.get()
            new_response = self.entry_response.get().split(", ")
            print("New term:" + new_term)
            print("New Response:" + str(new_response))
            dbworker.add_term(new_term, new_response)
            term = dbworker.search_term(new_term)
            print("Term: " + str(term.doc_id))
            print("Found card with term: " + new_term + " at index: " + str(term.doc_id))
            udbw.add_to_box(user_name=self.active_user, box_number=0, card_index=term.doc_id)
            self.entry_question.delete(0, tk.END)
            self.label_validation.configure(text="saved to data base", foreground="green")
            self.entry_response.delete(0, tk.END)
            self.label_answer.configure(text="")
            self.number_db_entries = dbworker.get_db_length()
        elif self.mode == "remove":
            dbworker.delete_term(self.active_term)
            udbw.remove_from_db(user_name=self.active_user, term=self.active_term)
            self.entry_question.delete(0, tk.END)
            self.label_validation.configure(text="Removed from data base", foreground="green")
            self.entry_response.delete(0, tk.END)
            self.label_answer.configure(text="")
            self.mode = "new"
            self.number_db_entries = dbworker.get_db_length()

        else:
            print("Error")

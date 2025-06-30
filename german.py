import csv
import tkinter as tk
from tkinter import messagebox
import random

class Verb:
    def __init__(self, verb, partizip_perfekt, meaning):
        self.verb = verb
        self.partizip_perfekt = partizip_perfekt
        self.meaning = meaning

def load_verbs_from_csv(filename):
    verbs = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            verbs.append(Verb(row['verb'], row['partizip_perfekt'], row['meaning']))
    return verbs

class VerbQuizApp:
    def __init__(self, root, verbs):
        self.root = root
        self.verbs = verbs
        random.shuffle(self.verbs)
        self.index = 0

        self.root.title("German Verb Quiz")

        self.label_verb = tk.Label(root, text="", font=("Arial", 16))
        self.label_verb.pack(pady=10)

        # Frame for entry fields with labels
        form_frame = tk.Frame(root)
        form_frame.pack()

        tk.Label(form_frame, text="Partizip Perfekt:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_partizip = tk.Entry(form_frame, width=30)
        self.entry_partizip.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Meaning:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_meaning = tk.Entry(form_frame, width=30)
        self.entry_meaning.grid(row=1, column=1, padx=5, pady=5)

        self.button_submit = tk.Button(root, text="Submit", command=self.check_answer)
        self.button_submit.pack(pady=5)

        self.feedback = tk.Label(root, text="", fg="blue", justify="left")
        self.feedback.pack(pady=5)

        self.button_next = tk.Button(root, text="Next", command=self.next_verb, state=tk.DISABLED)
        self.button_next.pack(pady=10)

        self.show_verb()

    def show_verb(self):
        if self.index < len(self.verbs):
            verb = self.verbs[self.index]
            self.label_verb.config(text=f"Verb: {verb.verb}")
            self.entry_partizip.delete(0, tk.END)
            self.entry_meaning.delete(0, tk.END)
            self.feedback.config(text="")
            self.button_submit.config(state=tk.NORMAL)
            self.button_next.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Quiz Completed", "You've completed the quiz.")
            self.root.destroy()

    def check_answer(self):
        user_partizip = self.entry_partizip.get().strip().lower()
        user_meaning = self.entry_meaning.get().strip().lower()

        verb = self.verbs[self.index]
        correct_partizip = verb.partizip_perfekt.lower()
        correct_meaning = verb.meaning.lower()

        result = []

        if user_partizip == correct_partizip:
            result.append("✅ Correct Partizip Perfekt")
        else:
            result.append(f"❌ Correct Partizip Perfekt: {verb.partizip_perfekt}")

        if user_meaning == correct_meaning:
            result.append("✅ Correct Meaning")
        else:
            result.append(f"❌ Correct Meaning: {verb.meaning}")

        self.feedback.config(text="\n".join(result))
        self.button_submit.config(state=tk.DISABLED)
        self.button_next.config(state=tk.NORMAL)

    def next_verb(self):
        self.index += 1
        self.show_verb()

if __name__ == "__main__":
    verbs = load_verbs_from_csv(r"C:\Users\mtcc\Desktop\German\verbs.csv")
    root = tk.Tk()
    app = VerbQuizApp(root, verbs)
    root.mainloop()

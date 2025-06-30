import csv
import random
import tkinter as tk

class Verb:
    def __init__(self, infinitiv, partizip_perfekt, meaning):
        self.infinitiv = infinitiv
        self.partizip_perfekt = partizip_perfekt
        self.meaning = meaning
        self.correct_count = 0  # New: count of correct answers

def load_verbs_from_csv(filepath):
    verbs = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            verbs.append(Verb(row['infinitiv'], row['partizip_perfekt'], row['meaning']))
    return verbs

class VerbQuizApp:
    def __init__(self, master, verbs):
        self.master = master
        self.all_verbs = verbs
        self.active_verbs = verbs.copy()
        self.learned_verbs = []

        self.master.title("German Verb Quiz")

        self.verb_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.verb_label.pack(pady=10)

        self.meaning_label = tk.Label(master, text="Meaning:")
        self.meaning_label.pack()
        self.meaning_entry = tk.Entry(master)
        self.meaning_entry.pack()

        self.partizip_label = tk.Label(master, text="Partizip Perfekt:")
        self.partizip_label.pack()
        self.partizip_entry = tk.Entry(master)
        self.partizip_entry.pack()

        self.feedback_label = tk.Label(master, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=10)

        self.check_button = tk.Button(master, text="Check Answer", command=self.check_answer)
        self.check_button.pack(pady=5)

        self.next_button = tk.Button(master, text="Next Verb", command=self.next_verb, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.current_verb = None
        self.next_verb()

    def next_verb(self):
        self.feedback_label.config(text="")
        self.meaning_entry.delete(0, tk.END)
        self.partizip_entry.delete(0, tk.END)
        self.next_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.NORMAL)

        if not self.active_verbs:
            self.verb_label.config(text="🎉 You've learned all verbs!")
            self.check_button.config(state=tk.DISABLED)
            return

        self.current_verb = random.choice(self.active_verbs)
        self.verb_label.config(text=f"Verb: {self.current_verb.infinitiv}")

    def check_answer(self):
        user_meaning = self.meaning_entry.get().strip().lower()
        user_partizip = self.partizip_entry.get().strip().lower()

        correct_meaning = self.current_verb.meaning.strip().lower()
        correct_partizip = self.current_verb.partizip_perfekt.strip().lower()

        if user_meaning == correct_meaning and user_partizip == correct_partizip:
            self.current_verb.correct_count += 1
            if self.current_verb.correct_count == 2:
                self.learned_verbs.append(self.current_verb)
                self.active_verbs.remove(self.current_verb)
                self.feedback_label.config(text="✅ Correct (2nd time)! Learned.")
            else:
                self.feedback_label.config(text="✅ Correct! One more time to learn it.")
        else:
            self.feedback_label.config(
                text=f"❌ Wrong!\nCorrect meaning: {self.current_verb.meaning}\nCorrect partizip: {self.current_verb.partizip_perfekt}"
            )

        self.check_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

# --- Main program ---

if __name__ == "__main__":
    verbs = load_verbs_from_csv(r"C:\Users\mtcc\Desktop\German\verbs.csv")
    root = tk.Tk()
    app = VerbQuizApp(root, verbs)
    root.mainloop()

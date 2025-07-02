import csv
import random
import tkinter as tk
from tkinter import messagebox
import os

class Verb:
    def __init__(self, infinitiv, partizip_perfekt, meaning):
        self.infinitiv = infinitiv
        self.partizip_perfekt = partizip_perfekt
        self.meaning = meaning
        self.correct_count = 0

def load_verbs_from_csv(filepath):
    verbs = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            verbs.append(Verb(row['infinitiv'], row['partizip_perfekt'], row['meaning']))
    return verbs

def load_learned_verbs(filepath=r"C:\Users\mtcc\Desktop\German\learned_verbs.csv"):
    learned = []
    if not os.path.exists(filepath):
        return learned
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            learned.append(Verb(row['infinitiv'], row['partizip_perfekt'], row['meaning']))
    return learned

def save_learned_verbs(verbs, filepath=r"C:\Users\mtcc\Desktop\German\learned_verbs.csv"):
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['infinitiv', 'partizip_perfekt', 'meaning']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for verb in verbs:
                writer.writerow({
                    'infinitiv': verb.infinitiv,
                    'partizip_perfekt': verb.partizip_perfekt,
                    'meaning': verb.meaning
                })
        print(f"File saved correctly at {filepath}")
    except Exception as e:
        print(f"Error saving file: {e}")

class VerbQuizApp:
    def __init__(self, master, all_verbs, learned_verbs):
        self.master = master
        self.all_verbs = all_verbs
        self.learned_verbs = learned_verbs
        self.active_verbs = [v for v in self.all_verbs if v.infinitiv not in {lv.infinitiv for lv in self.learned_verbs}]
        self.score = 0

        self.master.title("German Verb Quiz")

        self.verb_label = tk.Label(master, text="", font=("Helvetica", 16))
        self.verb_label.pack(pady=10)

        self.partizip_label = tk.Label(master, text="Partizip Perfekt:")
        self.partizip_label.pack()
        self.partizip_entry = tk.Entry(master)
        self.partizip_entry.pack()

        self.meaning_label = tk.Label(master, text="Meaning:")
        self.meaning_label.pack()
        self.meaning_entry = tk.Entry(master)
        self.meaning_entry.pack()

        self.feedback_label = tk.Label(master, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=10)

        self.score_label = tk.Label(master, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack(pady=5)

        self.check_button = tk.Button(master, text="Check Answer", command=self.check_answer)
        self.check_button.pack(pady=5)

        self.next_button = tk.Button(master, text="Next Verb", command=self.next_verb, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.show_learned_button = tk.Button(master, text="Show Learned Verbs", command=self.show_learned_verbs)
        self.show_learned_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="Reset Learned Verbs", command=self.reset_learned_verbs)
        self.reset_button.pack(pady=5)

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
            self.score += 1
            if self.current_verb.correct_count == 2:
                self.learned_verbs.append(self.current_verb)
                self.active_verbs.remove(self.current_verb)
                save_learned_verbs(self.learned_verbs)
                self.feedback_label.config(text="✅ Correct (2nd time)! Learned.")
            else:
                self.feedback_label.config(text="✅ Correct! One more time to learn it.")
        else:
            self.feedback_label.config(
                text=f"❌ Wrong!\nCorrect meaning: {self.current_verb.meaning}\nCorrect partizip: {self.current_verb.partizip_perfekt}"
            )
            self.score = 0  # Reset score on wrong answer

        self.score_label.config(text=f"Score: {self.score}")
        self.check_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def show_learned_verbs(self):
        if not self.learned_verbs:
            messagebox.showinfo("Learned Verbs", "No learned verbs yet.")
            return

        learned_text = "\n".join(f"{v.infinitiv} - {v.partizip_perfekt} - {v.meaning}" for v in self.learned_verbs)
        messagebox.showinfo("Learned Verbs", learned_text)

    def reset_learned_verbs(self):
        if messagebox.askyesno("Reset Learned Verbs", "Are you sure you want to reset the learned verbs list?"):
            self.learned_verbs.clear()
            save_learned_verbs(self.learned_verbs)
            self.active_verbs = self.all_verbs.copy()
            self.score = 0
            self.score_label.config(text=f"Score: {self.score}")
            self.feedback_label.config(text="Learned verbs list has been reset.")
            self.next_verb()

# --- Main program ---

if __name__ == "__main__":
    csv_path = r"C:\Users\mtcc\Desktop\German\verbs.csv"  # ← Update path if needed
    verbs = load_verbs_from_csv(csv_path)
    learned_verbs = load_learned_verbs()

    root = tk.Tk()
    app = VerbQuizApp(root, verbs, learned_verbs)
    root.mainloop()

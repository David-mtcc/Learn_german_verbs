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
            verbs.append(Verb(row['infinitive'], row['partizip_perfekt'], row['meaning']))
    return verbs

def load_learned_verbs(filepath):
    learned = []
    if not os.path.exists(filepath):
        return learned
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            learned.append(Verb(row['infinitive'], row['partizip_perfekt'], row['meaning']))
    return learned

def save_learned_verbs(verbs, filepath):
    with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['infinitive', 'partizip_perfekt', 'meaning']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for verb in verbs:
            writer.writerow({
                'infinitive': verb.infinitiv,
                'partizip_perfekt': verb.partizip_perfekt,
                'meaning': verb.meaning
            })

def save_remaining_verbs_to_csv(verbs, filepath):
    with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['infinitive'])
        for verb in verbs:
            writer.writerow([verb.infinitiv])

def load_remaining_verbs_from_csv(all_verbs, filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            infinitives = [row['infinitive'] for row in reader]
            return [v for v in all_verbs if v.infinitiv in infinitives]
    except Exception as e:
        print(f"Error loading remaining verbs: {e}")
        return []

class VerbQuizApp(tk.Frame):
    def __init__(self, master, all_verbs, learned_verbs, learned_path, remaining_path):
        super().__init__(master)
        self.master = master
        self.all_verbs = all_verbs
        self.learned_verbs = learned_verbs
        self.learned_path = learned_path
        self.remaining_path = remaining_path

        self.active_verbs = [v for v in self.all_verbs if v.infinitiv not in {lv.infinitiv for lv in self.learned_verbs}]
        self.remaining_verbs = load_remaining_verbs_from_csv(self.active_verbs, self.remaining_path)
        if not self.remaining_verbs:
            self.remaining_verbs = self.active_verbs.copy()
        self.score = 0

        self.master.title("German Verb Quiz")

        self.verb_label = tk.Label(self, text="", font=("Helvetica", 16))
        self.verb_label.pack(pady=10)

        self.partizip_label = tk.Label(self, text="Partizip Perfekt:")
        self.partizip_label.pack()
        self.partizip_entry = tk.Entry(self)
        self.partizip_entry.pack()

        self.meaning_label = tk.Label(self, text="Meaning:")
        self.meaning_label.pack()
        self.meaning_entry = tk.Entry(self)
        self.meaning_entry.pack()

        self.feedback_label = tk.Label(self, text="", font=("Helvetica", 12))
        self.feedback_label.pack(pady=10)

        self.score_label = tk.Label(self, text="Score: 0", font=("Helvetica", 12))
        self.score_label.pack(pady=5)

        self.check_button = tk.Button(self, text="Check Answer", command=self.check_answer)
        self.check_button.pack(pady=5)

        self.next_button = tk.Button(self, text="Next Verb", command=self.next_verb, state=tk.DISABLED)
        self.next_button.pack(pady=5)

        self.show_learned_button = tk.Button(self, text="Show Learned Verbs", command=self.show_learned_verbs)
        self.show_learned_button.pack(pady=5)

        self.reset_button = tk.Button(self, text="Reset Progress", command=self.reset_progress)
        self.reset_button.pack(pady=5)

        self.current_verb = None
        self.next_verb()

        self.pack(fill="both", expand=True)   # <-- importante per mostrare il frame

    def next_verb(self):
        self.feedback_label.config(text="")
        self.meaning_entry.delete(0, tk.END)
        self.partizip_entry.delete(0, tk.END)
        self.next_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.NORMAL)

        if not self.remaining_verbs:
            self.remaining_verbs = self.active_verbs.copy()

        if not self.remaining_verbs:
            self.verb_label.config(text="🎉 You've learned all verbs!")
            self.check_button.config(state=tk.DISABLED)
            return

        self.current_verb = random.choice(self.remaining_verbs)
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
                if self.current_verb in self.remaining_verbs:
                    self.remaining_verbs.remove(self.current_verb)
                save_learned_verbs(self.learned_verbs, self.learned_path)
                self.feedback_label.config(text="✅ Correct (2nd time)! Learned.")
            else:
                self.feedback_label.config(text="✅ Correct! One more time to learn it.")
        else:
            self.feedback_label.config(
                text=f"❌ Wrong!\nCorrect meaning: {self.current_verb.meaning}\nCorrect partizip: {self.current_verb.partizip_perfekt}"
            )
            self.score = 0

        self.score_label.config(text=f"Score: {self.score}")
        if self.current_verb in self.remaining_verbs:
            self.remaining_verbs.remove(self.current_verb)

        self.check_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.NORMAL)

    def show_learned_verbs(self):
        if not self.learned_verbs:
            messagebox.showinfo("Learned Verbs", "No learned verbs yet.")
            return
        learned_text = "\n".join(f"{v.infinitiv} - {v.partizip_perfekt} - {v.meaning}" for v in self.learned_verbs)
        messagebox.showinfo("Learned Verbs", learned_text)

    def reset_progress(self):
        if messagebox.askyesno("Reset Progress", "Are you sure you want to reset all progress?"):
            try:
                os.remove(self.learned_path)
                os.remove(self.remaining_path)
            except FileNotFoundError:
                pass
            self.learned_verbs.clear()
            self.active_verbs = self.all_verbs.copy()
            self.remaining_verbs = self.active_verbs.copy()
            self.score = 0
            self.score_label.config(text="Score: 0")
            self.feedback_label.config(text="Progress reset.")
            self.next_verb()

    def on_close(self):
        save_remaining_verbs_to_csv(self.remaining_verbs, self.remaining_path)
        self.master.destroy()

class SelectionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        tk.Label(self, text="Choose the verbs list to practice:", font=("Helvetica", 14)).pack(pady=20)

        tk.Button(self, text="A1 Verbs", width=20, command=lambda: self.select("A1")).pack(pady=5)
        tk.Button(self, text="A2 Verbs", width=20, command=lambda: self.select("A2")).pack(pady=5)
        tk.Button(self, text="Custom Verbs", width=20, command=lambda: self.select("Custom")).pack(pady=5)

        self.pack()

    def select(self, choice):
        self.pack_forget()  # nascondi la finestra di selezione
        start_quiz(self.master, choice)

def start_quiz(root, choice):
    base_path = r"C:\Users\mtcc\Desktop\German"

    if choice == "A1":
        verbs_path = os.path.join(base_path, "verbs_A1.csv")
        learned_path = os.path.join(base_path, "learned_verbs_A1.csv")
        remaining_path = os.path.join(base_path, "remaining_verbs_A1.csv")
    elif choice == "A2":
        verbs_path = os.path.join(base_path, "verbs_A2.csv")
        learned_path = os.path.join(base_path, "learned_verbs_A2.csv")
        remaining_path = os.path.join(base_path, "remaining_verbs_A2.csv")
    else:
        verbs_path = os.path.join(base_path, "verbs_custom.csv")
        learned_path = os.path.join(base_path, "learned_verbs_custom.csv")
        remaining_path = os.path.join(base_path, "remaining_verbs_custom.csv")

    verbs = load_verbs_from_csv(verbs_path)
    learned_verbs = load_learned_verbs(learned_path)

    app = VerbQuizApp(root, verbs, learned_verbs, learned_path, remaining_path)
    root.protocol("WM_DELETE_WINDOW", app.on_close)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Select Verb List")
    SelectionFrame(root)
    root.mainloop()

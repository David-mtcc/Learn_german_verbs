# German Verb Quiz

A simple Tkinter-based quiz application to practice German verbs in the **infinitive**, **Partizip Perfekt**, and their **English meanings**.

---

## Features

- Choose between three verb lists to practice:
  - A1 verbs (`verbs_A1.csv`)
  - A2 verbs (`verbs_A2.csv`)
  - Custom verbs (`verbs_custom.csv`)
- Tracks learned verbs by saving progress to CSV files
- Repeats verbs until correctly answered twice
- Shows score and feedback
- Reset progress option
- GUI with bigger fonts and custom German flag icon

---

## Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually included with Python)
  
### Files Needed

- `verbs_A1.csv`, `verbs_A2.csv`, `verbs_custom.csv` - CSV files containing verbs with columns:  
  `infinitiv,partizip_perfekt,meaning`
- `german_flag.ico` - Icon file for the window (optional)

### Running the App

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/german-verb-quiz.git
   cd german-verb-quiz
2. Place your CSV verb lists and icon in the appropriate directory, or adjust paths in the code.

3. Run the program:

    ```bash
   python verb_quiz.py
  
3. Select the verb list to practice and start learning!

### CSV Format Example

    infinitiv,partizip_perfekt,meaning
    gehen,gegangen,to go
    essen,gegessen,to eat
    schlafen,geschlafen,to sleep
    
### How It Works
1. The program loads the selected verb list CSV.
2. It tracks which verbs have been learned by saving progress to separate CSV files.
3. Each verb must be answered correctly twice to be considered learned.
4. The quiz shows one verb at a time and asks for the Partizip Perfekt and English meaning.
5. User inputs are checked and feedback is displayed.
6. Score resets on wrong answers.

Learned verbs can be viewed anytime.

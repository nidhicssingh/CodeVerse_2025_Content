import tkinter as tk
from tkinter import messagebox
import os
from subjects import Math_quiz, Data_structure_quiz, Python_quiz

quiz_modules = {
    "Math": Math_quiz.quiz_data,
    "Data Structure": Data_structure_quiz.quiz_data,
    "Python": Python_quiz.quiz_data
}

user_name = ""
user_answers = []
selected_subject = ""
quiz_data = []

root = tk.Tk()
root.title("Modular Quiz App")
root.geometry("600x400")

def start_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter Your Name", font=("Arial", 18)).pack(pady=20)
    name_entry = tk.Entry(root, font=("Arial", 16))
    name_entry.pack()

    def proceed_to_subject():
        global user_name
        user_name = name_entry.get().strip()
        if user_name == "":
            messagebox.showerror("Error", "Please enter your name!")
        else:
            subject_selection()

    tk.Button(root, text="Proceed", command=proceed_to_subject, font=("Arial", 14), bg="blue", fg="white").pack(pady=20)

def subject_selection():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Choose Subject", font=("Arial", 18)).pack(pady=20)

    def start_subject(subject):
        global selected_subject, quiz_data
        selected_subject = subject
        quiz_data = quiz_modules[subject]
        user_answers.clear()
        show_question(0)

    for subject in quiz_modules:
        tk.Button(root, text=subject, font=("Arial", 14), width=20,
                  command=lambda s=subject: start_subject(s)).pack(pady=10)

def show_question(index):
    for widget in root.winfo_children():
        widget.destroy()

    question_data = quiz_data[index]
    question = question_data["question"]
    options = question_data["options"]

    tk.Label(root, text=f"Q{index+1}: {question}", font=("Arial", 16), wraplength=500).pack(pady=20)

    selected_option = tk.StringVar()

    for opt in options:
        tk.Radiobutton(root, text=opt, variable=selected_option, value=opt, font=("Arial", 14)).pack(anchor="w", padx=100)

    def next_question():
        if not selected_option.get():
            messagebox.showwarning("Warning", "Please select an option.")
            return

        user_answers.append(selected_option.get())

        if index + 1 < len(quiz_data):
            show_question(index + 1)
        else:
            show_result()

    tk.Button(root, text="Next", command=next_question, font=("Arial", 14), bg="green", fg="white").pack(pady=20)

def show_result():
    score = 0
    result_text = ""

    for i, ans in enumerate(user_answers):
        correct = quiz_data[i]["answer"]
        result_text += f"Q{i+1}: {quiz_data[i]['question']}\n"
        result_text += f"Your Answer: {ans}\nCorrect Answer: {correct}\n\n"
        if ans == correct:
            score += 1

    result_text += f"Final Score: {score}/{len(quiz_data)}\n"

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Thanks {user_name}!", font=("Arial", 18)).pack(pady=10)
    tk.Label(root, text=f"{selected_subject} Score: {score}/{len(quiz_data)}", font=("Arial", 16)).pack(pady=10)

    save_path = f"E:/Hands on python/Python Based Quiz app/CodeVerse_2025_Content/Python-based quiz app/Response/{user_name}_{selected_subject}.txt"
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(result_text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save response: {e}")
        return

    tk.Label(root, text="Response saved successfully!", font=("Arial", 12), fg="green").pack(pady=10)

start_screen()
root.mainloop()

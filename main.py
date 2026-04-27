"""
Training Planner - Главный файл запуска приложения
"""

from training_planner import TrainingPlannerApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

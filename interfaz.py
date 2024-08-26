import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime
import pygame
from graphics import controller, plotWeek

POMODORO_TIME = 25
SHORT_BREAK_TIME = 5
LONG_BREAK_TIME = 15

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro App")   
        self.master.geometry("400x700")

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.timer_running = False
        self.current_timer = None
        self.remaining_time = 0
        self.current_task = None
        self.dark_mode = False
        self.completed_pomodoros = []  # List to store completed Pomodoros
        self.selected_date = None  # Variable to store the selected date

        pygame.mixer.init()
        self.sound = pygame.mixer.Sound("/home/franyober/Documents/Python/sql-project/timer_sound.wav")

        self.create_widgets()
        self.set_light_mode()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_timer_panel()
        self.create_task_panel()
        self.create_calendar_button()

        self.mode_button = ttk.Button(self.main_frame, text="Dark Mode", command=self.toggle_mode)
        self.mode_button.pack(pady=10)



    def create_timer_panel(self):
        timer_frame = ttk.Frame(self.main_frame)
        timer_frame.pack(fill=tk.X, pady=10)

        self.timer_buttons = []
        for timer_type in ["Pomodoro", "Short Break", "Long Break"]:
            btn = ttk.Button(timer_frame, text=timer_type, command=lambda t=timer_type: self.set_timer(t))
            btn.pack(side=tk.LEFT, expand=True, padx=5)
            self.timer_buttons.append(btn)

        self.time_label = ttk.Label(self.main_frame, text=f"{POMODORO_TIME:02d}:00", font=("Arial", 64))
        self.time_label.pack(pady=20)

        self.start_button = ttk.Button(self.main_frame, text="Start", command=self.toggle_timer)
        self.start_button.pack(pady=10)

        self.current_task_label = ttk.Label(self.main_frame, text="No task selected", font=("Arial", 12))
        self.current_task_label.pack(pady=5)

    def create_task_panel(self):
        task_frame = ttk.Frame(self.main_frame)
        task_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.task_listbox = tk.Listbox(task_frame, selectmode=tk.SINGLE, font=("Arial", 12))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)

        scrollbar = ttk.Scrollbar(task_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)

        default_tasks = ["Proyecto de grado","Redes","Robótica","Entrenamiento funcional","Ciberseguridad","Inglés","Cloud computing","Programación"]
        for task in default_tasks:
            self.task_listbox.insert(tk.END, task)

        task_entry = ttk.Entry(self.main_frame, font=("Arial", 12))
        task_entry.pack(fill=tk.X, pady=5)

        add_task_button = ttk.Button(self.main_frame, text="Add Task", command=lambda: self.add_task(task_entry))
        add_task_button.pack(pady=5)

    def create_calendar_button(self):
        self.calendar_button = ttk.Button(self.main_frame, text="Select Date", command=self.show_calendar)
        self.calendar_button.pack(pady=10)


    def show_calendar(self):
        top = tk.Toplevel(self.master)
        top.title("Select a date")
        
        cal = Calendar(top, selectmode='day', date_pattern='DD-MM-YYYY')
        cal.pack(padx=10, pady=10)
        
        ok_button = ttk.Button(top, text="OK", command=lambda: self.get_date(cal, top))
        ok_button.pack(pady=10)

    def get_date(self, cal, top):
        self.selected_date = cal.get_date()
        print(f"Selected date: {self.selected_date}")  # For debugging
        plotWeek(self.selected_date)
        
        top.destroy()

    def set_timer(self, timer_type):
        if timer_type == "Pomodoro":
            self.remaining_time = POMODORO_TIME  * 60
        elif timer_type == "Short Break":
            self.remaining_time = SHORT_BREAK_TIME  * 60
        else:  # Long Break
            self.remaining_time = LONG_BREAK_TIME * 60

        self.current_timer = timer_type
        self.update_time_label()

    def toggle_timer(self):
        if not self.current_task:
            self.show_message("Please select a task before starting the timer.")
            return

        if self.timer_running:
            self.timer_running = False
            self.start_button.config(text="Start")
        else:
            self.timer_running = True
            self.start_button.config(text="Stop")
            self.run_timer()

    def run_timer(self):
        if self.timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_time_label()
            self.master.after(1000, self.run_timer)
        elif self.remaining_time <= 0:
            self.timer_running = False
            self.start_button.config(text="Start")
            self.play_sound()
            if self.current_timer == "Pomodoro":
                self.save_completed_pomodoro()
            self.show_message(f"{self.current_timer} completed!")

    def update_time_label(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def add_task(self, entry):
        task = entry.get()
        if task:
            self.task_listbox.insert(tk.END, task)
            entry.delete(0, tk.END)

    def on_task_select(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_task = self.task_listbox.get(index)
            for i in range(self.task_listbox.size()):
                self.task_listbox.itemconfig(i, {'bg': self.style.lookup('TFrame', 'background')})
            self.task_listbox.itemconfig(index, {'bg': 'yellow' if not self.dark_mode else 'dark goldenrod'})
            self.current_task_label.config(text=f"Current task: {self.current_task}")

    def show_message(self, message):
        messagebox.showinfo("Pomodoro App", message)

    def toggle_mode(self):
        if self.dark_mode:
            self.set_light_mode()
        else:
            self.set_dark_mode()

    def set_dark_mode(self):
        self.style.configure('TFrame', background='#2E2E2E')
        self.style.configure('TButton', background='#4A4A4A', foreground='white')
        self.style.configure('TLabel', background='#2E2E2E', foreground='white')
        self.style.configure('TEntry', fieldbackground='#4A4A4A', foreground='white')
        self.task_listbox.config(bg='#4A4A4A', fg='white')
        self.master.configure(bg='#2E2E2E')
        self.main_frame.configure(style='TFrame')
        self.mode_button.config(text="Light Mode")
        self.dark_mode = True

    def set_light_mode(self):
        self.style.configure('TFrame', background='#F0F0F0')
        self.style.configure('TButton', background='#E0E0E0', foreground='black')
        self.style.configure('TLabel', background='#F0F0F0', foreground='black')
        self.style.configure('TEntry', fieldbackground='white', foreground='black')
        self.task_listbox.config(bg='white', fg='black')
        self.master.configure(bg='#F0F0F0')
        self.main_frame.configure(style='TFrame')
        self.mode_button.config(text="Dark Mode")
        self.dark_mode = False

    def play_sound(self):
        self.sound.play()

    def save_completed_pomodoro(self):
        if self.current_timer == "Pomodoro":
            current_date = datetime.now().strftime("%d-%m-%Y")
            pomodoro_time = POMODORO_TIME 
            completed_pomodoro = (self.current_task, current_date, pomodoro_time)
            self.completed_pomodoros.append(completed_pomodoro)
            print(f"Saved completed Pomodoro: {completed_pomodoro}")

            if controller.search(self.current_task,current_date):
                controller.update(self.current_task,current_date,pomodoro_time)
                print("El registro ya existe, se añadió el tiempo correctamente")
                
            else:
                controller.insertRow(self.current_task,current_date,pomodoro_time)
                print("Se creó un nuevo registro")

    def show_completed_pomodoros(self):
        if not self.completed_pomodoros:
            self.show_message("No completed Pomodoros yet.")
        else:
            pomodoro_list = "\n".join([f"Task: {task}, Date: {date}, Duration: {duration}" 
                                       for task, date, duration in self.completed_pomodoros])
            messagebox.showinfo("Completed Pomodoros", pomodoro_list)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
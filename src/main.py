from interfaz import *

if __name__ == "__main__":

    if not (controller.os.path.exists(controller.pathDB)):
        controller.createDB()
        controller.createTable()
    else:
        print("La base de datos ya existe") 
   
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
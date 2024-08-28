from interfaz import *

if __name__ == "__main__":

    if not (controller.os.path.exists(controller.pathDB)):
        controller.createDB()
        controller.createTable()
    else:
        print("La base de datos ya existe") 

    if not (controller.os.path.exists(f"{controller.pathProject}/ejecutable")):
        print("No existe el ejecutable")
        f = open("ejecutable", "w")
        f.writelines(["#!/bin/bash\n", f"cd {controller.pathProject}\n", "source ./env/bin/activate\n",
        f"python3 {controller.pathProject}/src/main.py\n"])
        f.close()
    
    else:
        print("Sí existe el ejecutable")
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
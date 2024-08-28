import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import controller

def plotWeek(date):
    task_dict = defaultdict(lambda: defaultdict(int))
    all_tasks = set()
    all_dates = set()

    days = controller.extractDays(date)
    
    for _, task, date, time in days:
        task_dict[date][task] += time
        all_tasks.add(task)
        all_dates.add(date)
    
    unique_dates = sorted(all_dates)
    all_tasks = list(all_tasks)

    fig, ax = plt.subplots(figsize=(6, 5))
    bottom = np.zeros(len(unique_dates))
    
    for task in all_tasks:
        task_times = [task_dict[date][task] for date in unique_dates]
        
        if any(task_times):  # Solo graficar si hay tiempos mayores que cero para esta tarea
            p = ax.bar(unique_dates, task_times, 0.6, label=task, bottom=bottom)
            
            # Etiquetar solo las barras con valores positivos
            for rect, height in zip(p, task_times):
                if height > 0:
                    ax.text(rect.get_x() + rect.get_width() / 2., rect.get_y() + height / 2.,
                            f'{height}', ha='center', va='center')
            
            bottom += np.array(task_times)
    
    ax.set_xlabel('Fechas')
    ax.set_ylabel('Minutos')
    ax.legend()
    

    
    plt.xticks(unique_dates, rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plotWeek('18-08-2024')
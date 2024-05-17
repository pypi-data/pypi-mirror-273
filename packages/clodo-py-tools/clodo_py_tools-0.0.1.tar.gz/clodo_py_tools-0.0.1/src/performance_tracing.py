def trace_performance():
    import importlib
    importlib.import_module("performance_tracing")

import psutil
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.animation as animation
import threading
import queue
import sys
import os

# Configuração inicial
fig, (ax1, ax2) = plt.subplots(2, 1)
x_vals = []
cpu_vals = []
mem_vals = []
selected_process = None
# Requests a process's reference from the user in a separate thread
def get_user_input():
    
    global selected_process
    N = 10

    print(f"\n {N} most recent processes: \n")
    for process_name, process_id, process_create_time in get_recent_processes(N):
        print(f"Process Name: {process_name}, \n Process ID: {process_id} \n -------------------------------")

    print("\nEnter a process reference to track its performance over time.")
    print("Consult a process explorer program to find the references for other processes. \n")

    user_input = input('Process name or PID: ')
    if (user_input == ''): 
        print("No corresponding process!")
        get_user_input()
        return
    elif (user_input in ('exit', 'quit')):
        sys.exit()
    for process in psutil.process_iter():
        if (user_input == process.name()):
            selected_process = process.pid
            print_process_info(process)
            return       
    for process in psutil.process_iter():
        if (int(user_input) == process.pid):
            selected_process = process.pid
            print_process_info(process)
            return
    print("No corresponding process!")
    get_user_input()

#Requests a process's reference from the user in a separate thread:
def get_user_input_in_new_thread(_, new_process_reference):
    global selected_process
    get_user_input()
    new_process_reference.put(selected_process)

def print_process_info(process):
    print (f'\n Starting the plot of process: \n Process Name: {process.name()} \n Process PID: {process.pid} \n More: {process.name} \n')

def get_recent_processes(N):
    processes = []
    for proc in psutil.process_iter(attrs=['name', 'pid', 'create_time']):
        processes.append((proc.info['name'], proc.info['pid'], proc.info['create_time']))
    return sorted(processes, key=lambda x: x[2], reverse=True)[:N]

# Função para atualizar os gráficos
def update_graph(frame):
    global selected_process, x_vals, cpu_vals, mem_vals
    x_vals.append(datetime.now())
    try:
        process = psutil.Process(selected_process)
        cpu_percent = process.cpu_percent(interval=1)
        mem_info = process.memory_info()
        mem_mb = mem_info.rss / (1024 * 1024)  # Convertendo para MB

        cpu_vals.append(cpu_percent)
        mem_vals.append(mem_mb)

        ax1.clear()
        ax1.plot(x_vals, cpu_vals, label='CPU %')
        ax1.set_ylabel('CPU (%)')
        ax1.legend()

        ax2.clear()
        ax2.plot(x_vals, mem_vals, label='Memória (MB)', color='orange')
        ax2.set_ylabel('Memória (MB)')
        ax2.legend()

        plt.tight_layout()
        
    except psutil.NoSuchProcess as e:

        print(f"Process of PID {selected_process} not found - might've been terminated.")
        ani.pause()
        
        # Requiring new process reference from the user using a new thread that returns the give valuen
        # to the parent thread:
        new_process_reference = queue.Queue()
        new_thread = threading.Thread(target=get_user_input_in_new_thread, args=([], new_process_reference))
        new_thread.start()
        new_thread.join()
        selected_process = new_process_reference.get()

        ## Cleaning plot data:
        x_vals = []
        cpu_vals = []
        mem_vals = []

        ani.resume()

# Require process's references from user:
get_user_input()

# Configuração da animação:
ani = animation.FuncAnimation(fig, update_graph, interval=1000)

# Exibir o gráfico:
plt.show()
import tkinter as tk
from tkinter import ttk

list = []
root = None
listbox = None
module_combobox = None
entry1 = None
entry2 = None

def add_to_list():
    global module_combobox, entry1, entry2, listbox, list
    module_name = module_combobox.get()
    value1 = entry1.get()
    value2 = entry2.get()
    if module_name and value1 and value2:
        list.append(f'{module_name}({value1}, {value2})')
        listbox.insert(tk.END, f"{module_name}({value1}, {value2})")
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)

def remove_from_list():
    global listbox, list
    selected_index = listbox.curselection()
    if selected_index:
        module = listbox.get(selected_index)
        list.remove(f'{module}')
        listbox.delete(selected_index)

def quit():
    global root
    root.destroy()

async def gui_collect_info():
    global root, listbox, module_combobox, entry1, entry2
    # Создание графического интерфейса
    root = tk.Tk()
    root.geometry("240x370")
    root.title("Маршрут")
    # Создание виджетов
    frame = ttk.Frame(root)
    scrollbar = ttk.Scrollbar(frame)
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=35)
    module_combobox = ttk.Combobox(root, values=["DmailDAO", "Минт IDentity", "Аппрув Unframed", "Трансфер", "Рандомный модуль"], state='readonly')
    entry1 = ttk.Entry(root, width=20)
    entry2 = ttk.Entry(root, width=20)
    add_button = ttk.Button(root, text="Добавить", command=add_to_list)
    remove_button = ttk.Button(root, text="Удалить", command=remove_from_list)
    # Расположение элементов
    frame.pack(side="top", padx=5, pady=5)
    scrollbar.pack(side="right", fill="y")
    listbox.pack(side="left", fill="both", expand=True)
    tk.Label(root, text="Выберите модуль:").pack(side="top")
    module_combobox.pack(side="top", pady=5)
    tk.Label(root, text="Мин. кол-во транзакций:").pack(side="top")
    entry1.pack(side="top")
    tk.Label(root, text="Макс. кол-во транзакций:").pack(side="top")
    entry2.pack(side="top")
    add_button.pack(side="left", padx=5)
    remove_button.pack(side="left", padx=5)
    start_button = tk.Button(root, text="Старт", command=quit)
    start_button.pack(side="left", padx=10, pady=5)
    scrollbar.config(command=listbox.yview)
    root.mainloop()
    return list
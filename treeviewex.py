from tkinter import *
from tkinter import ttk, messagebox
from clsGeography import Geography


# логика
# заполняем поля ввода значениями выделенной позиции в общем списке
def get_selected_row(event):
    global countries
    # набор данных, выделенных в таблице
    selection = table.selection()
    # получаем позицию выделенной записи в списке
    item = table.item(selection[0])
    # получаем значение выделенной записи
    countries = item["values"]
    # удаляем то, что было раньше в поле ввода
    name_entry.delete(0, END)
    # и добавляем туда текущее значение названия покупки
    name_entry.insert(END, countries[1])
    # делаем то же самое с другими полями
    region_entry.delete(0, END)
    region_entry.insert(END, countries[2])
    capital_entry.delete(0, END)
    capital_entry.insert(END, countries[3])
    territory_area_entry.delete(0, END)
    territory_area_entry.insert(END, countries[4])
    population_entry.delete(0, END)
    population_entry.insert(END, countries[5])


# обработчик нажатия на кнопку «Посмотреть всё»
def view_command():
    # очищаем список в приложении
    table.delete(*table.get_children())
    # проходим все записи в БД
    for row in database_geography.view():
        # и сразу добавляем их на экран
        table.insert('', END, values=row)


# обработчик нажатия на кнопку «Поиск»
def search_command():
    # очищаем список в приложении
    table.delete(*table.get_children())
    # находим все записи по названию покупки
    for row in database_geography.search(name_text.get()):
        # и добавляем их в список в приложение
        table.insert('', END, values=row)


# обработчик нажатия на кнопку «Добавить»
def add_command():

    # добавляем запись в БД
    database_geography.insert(name_text.get(),
                              region_text.get(),
                              capital_text.get(),
                              territory_area_text.get(),
                              population_text.get())
    # обновляем общий список в приложении
    view_command()


# обработчик нажатия на кнопку «Удалить»
def delete_command():
    # удаляем запись из базы данных по индексу выделенного элемента
    database_geography.delete(countries[0])
    # обновляем общий список расходов в приложении
    view_command()


# обработчик нажатия на кнопку «Обновить»
def update_command():
    # обновляем данные в БД о выделенной записи
    database_geography.update(countries[0],
                              name_text.get(),
                              region_text.get(),
                              capital_text.get(),
                              territory_area_text.get(),
                              population_text.get())
    # обновляем общий список расходов в приложении
    view_command()


# интерфейс
window = Tk()
window.title("Демонстрация действий с БД")


# обрабатываем закрытие окна
def on_closing():
    # показываем диалоговое окно с кнопкой
    if messagebox.askokcancel("", "Закрыть программу?"):
        # удаляем окно и освобождаем память
        window.destroy()


# сообщаем системе о том, что делать, когда окно закрывается
window.protocol("WM_DELETE_WINDOW", on_closing)

# создаём блоки для полей ввода и подписей к ним и размещаем их по сетке
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)
# создаём надписи для полей ввода и размещаем их по сетке
l1 = Label(frame, text="Страна")
l1.pack()
name_text = StringVar()
name_entry = ttk.Entry(frame, textvariable=name_text)
name_entry.pack()
frame.grid(row=0, column=0)

frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)
l2 = Label(frame, text="Регион")
l2.pack()
region_text = StringVar()
region_entry = ttk.Entry(frame, textvariable=region_text)
region_entry.pack()
frame.grid(row=0, column=1)
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)

l3 = Label(frame, text="Столица")
l3.pack()
capital_text = StringVar()
capital_entry = ttk.Entry(frame, textvariable=capital_text)
capital_entry.pack()
frame.grid(row=0, column=2)
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)

l4 = Label(frame, text="Площадь страны")
l4.pack()
territory_area_text = StringVar()
territory_area_entry = ttk.Entry(frame, textvariable=territory_area_text)
territory_area_entry.pack()
frame.grid(row=0, column=3)
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)

l5 = Label(frame, text="Численность населения")
l5.pack()
population_text = StringVar()
population_entry = ttk.Entry(frame, textvariable=population_text)
population_entry.pack()
frame.grid(row=0, column=4)
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)

# создаём таблицу, где появятся данные, и сразу определяем его размеры в окне
table = ttk.Treeview(frame, show='headings')
heads = ['ID', 'name', 'region', 'capital', 'territory_area', 'population']
table['columns'] = heads
table['displaycolumns'] = ['ID', 'name', 'region', 'capital', 'territory_area', 'population']
for head in heads:
    table.heading(head, text=head, anchor='center')
    table.column(head, anchor='center')
table.pack(side=LEFT, fill=BOTH, expand=1)


# на всякий случай добавим сбоку скролл, чтобы можно было быстро прокручивать длинные списки
sb1 = Scrollbar(frame)
sb1.pack(side=RIGHT, fill=Y)

# привязываем скролл к таблице
table.configure(yscrollcommand=sb1.set)
sb1.configure(command=table.yview)
frame.grid(row=1, column=0, columnspan=2)

table.bind('<<TreeviewSelect>>', get_selected_row)

# создаём кнопки действий и привязываем их к своим функциям
# кнопки размещаем тоже по сетке
frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=5)
b1 = Button(frame, text="Посмотреть все", width=12, command=view_command)
b1.pack()
# size of the button

b2 = Button(frame, text="Поиск", width=12, command=search_command)
b2.pack()

b3 = Button(frame, text="Добавить", width=12, command=add_command)
b3.pack()

b4 = Button(frame, text="Обновить", width=12, command=update_command)
b4.pack()

b5 = Button(frame, text="Удалить", width=12, command=delete_command)
b5.pack()

b6 = Button(frame, text="Закрыть", width=12, command=on_closing)
b6.pack()
frame.grid(row=1, column=2)

database_geography = Geography()


window.mainloop()
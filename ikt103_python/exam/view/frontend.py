from tkinter import *
from tkinter.messagebox import *
import tkinter.ttk as ttk
from datetime import datetime
from tkcalendar import DateEntry
from view.prayer import users, cars, rentals
from functools import partial
from dateutil.relativedelta import relativedelta
from requests.exceptions import ConnectionError
import itertools
import math
import re

size = {'width': 20, 'height': 6, 'pady': 10}


class Interface(Frame):
    def __init__(self, master=None):
        self.master = master
        super().__init__(master)
        self.pack(expand=True, fill=BOTH)
        self.columnconfigure(4, weight=1)
        # Declaring some important variables
        self.page = 0  # This variable changes depending on which page you are on
        self.pages = []  # This is the list where all the pages are stored, this will change depending on what you access.
        self.displayed = 7  # Number of pages to be shown default

        # Frames for editing and renting
        self.edit_user_frame = Frame(self)
        self.edit_car_frame = Frame(self)
        self.edit_rental_frame = Frame(self)

        # Widgets inside edit,delete and renting frames

        # Users
        self.user_name_label = Label(self.edit_user_frame, text='Name: ', pady=20)
        self.user_name_entry = Entry(self.edit_user_frame)
        self.user_address_label = Label(self.edit_user_frame, text='Address: ')
        self.user_address_entry = Entry(self.edit_user_frame)
        self.user_phone_label = Label(self.edit_user_frame, text='Phone number: ', pady=20)
        self.user_phone_entry = Entry(self.edit_user_frame)
        self.user_age_label = Label(self.edit_user_frame, text='Birth date: ')
        self.user_age_entry = DateEntry(self.edit_user_frame, width=12, background='darkblue', foreground='white',
                                        borderwidth=2, date_pattern='yyyy-mm-dd')
        self.user_put = Button(self.edit_user_frame, text='Submit', width=6, pady=5, command=self.put_one_user)
        self.user_post = Button(self.edit_user_frame, text='Submit', width=6, pady=5,
                                command=partial(self.put_one_user, post=True))
        self.edit_user_label = Label(self.edit_user_frame, pady=10, font=20)

        self.user_name_label.grid(column=5, row=1)
        self.user_name_entry.grid(column=6, row=1)
        self.user_address_label.grid(column=5, row=3)
        self.user_address_entry.grid(column=6, row=3)
        self.user_phone_label.grid(column=5, row=5)
        self.user_phone_entry.grid(column=6, row=5)
        self.user_age_label.grid(column=5, row=7)
        self.user_age_entry.grid(column=6, row=7)

        # Cars
        self.car_reg_label = Label(self.edit_car_frame, text='Registration Number: ')
        self.car_reg_number_entry = Entry(self.edit_car_frame)
        self.model_label = Label(self.edit_car_frame, text='Model name: ', pady=20)
        self.car_model_entry = Entry(self.edit_car_frame)
        self.car_year_label = Label(self.edit_car_frame, text='Registration year: ')
        self.car_year_entry = Entry(self.edit_car_frame)
        self.car_price_label = Label(self.edit_car_frame, text='Price per day: ', pady=20)
        self.car_price_entry = Entry(self.edit_car_frame)
        self.car_commit = Button(self.edit_car_frame, text='Submit', width=6, pady=5, command=self.put_car)
        self.car_commit_post = Button(self.edit_car_frame, text='Submit', width=6, pady=5,
                                      command=partial(self.put_car, post=True))
        self.edit_cars_label = Label(self.edit_car_frame, pady=10, font=20)

        self.car_reg_label.grid(column=1, row=1)
        self.car_reg_number_entry.grid(column=2, row=1)
        self.model_label.grid(column=1, row=2)
        self.car_model_entry.grid(column=2, row=2)
        self.car_year_label.grid(column=1, row=3)
        self.car_year_entry.grid(column=2, row=3)
        self.car_price_label.grid(column=1, row=4)
        self.car_price_entry.grid(column=2, row=4)

        # Rentals
        self.rent_reg_label = Label(self.edit_rental_frame, text='Registration Number:')
        self.rent_reg_entry = Entry(self.edit_rental_frame)
        self.rent_space1 = Label(self.edit_rental_frame, width=3)
        self.rent_userid_label = Label(self.edit_rental_frame, text='User id:', pady=12)
        self.rent_userid_entry = Entry(self.edit_rental_frame)
        self.rent_from_label = Label(self.edit_rental_frame, text='Rent from:')
        self.rent_from_entry = DateEntry(self.edit_rental_frame, width=12, background='darkblue', foreground='white',
                                         borderwidth=2, date_pattern='yyyy-mm-dd')
        self.rent_space3 = Label(self.edit_rental_frame, width=3)
        self.rent_to_label = Label(self.edit_rental_frame, text='Rent to:')
        self.rent_to_entry = DateEntry(self.edit_rental_frame, width=12, background='darkblue', foreground='white',
                                       borderwidth=2, date_pattern='yyyy-mm-dd')
        self.rent_submit = Button(self.edit_rental_frame, text='Submit', command=self.put_one_rental)
        self.rent_submit_post = Button(self.edit_rental_frame, text='Submit',
                                       command=partial(self.put_one_rental, post=True))
        self.rent_price_tot_label = Label(self.edit_rental_frame, text='Total price for rent: ')
        self.rent_price_tot_entry = Entry(self.edit_rental_frame)

        self.rent_label_edit = Label(self.edit_rental_frame, pady=30, font=20)

        # Making frames inside rental frame for time from
        self.rent_hour_min_from_frame = Frame(self.edit_rental_frame)
        self.rent_hour_label_from = Label(self.rent_hour_min_from_frame, text='Hours')
        self.rent_hour_entry_from = Spinbox(self.rent_hour_min_from_frame, width=2, from_=00, to=23, format='%02.0f')
        self.rent_minute_label_from = Label(self.rent_hour_min_from_frame, text='Minutes')
        self.rent_minute_entry_from = Spinbox(self.rent_hour_min_from_frame, width=2, from_=00, to=60, format='%02.0f')
        self.rent_from_space = Label(self.rent_hour_min_from_frame, width=1)

        self.rent_hour_label_from.grid(column=1, row=1)
        self.rent_hour_entry_from.grid(column=2, row=1)
        self.rent_from_space.grid(column=3, row=1)
        self.rent_minute_label_from.grid(column=4, row=1)
        self.rent_minute_entry_from.grid(column=5, row=1)

        # Making frames inside rental frame for time to
        self.rent_hour_min_to_frame = Frame(self.edit_rental_frame)
        self.rent_hour_label_to = Label(self.rent_hour_min_to_frame, text='Hours', pady=10)
        self.rent_hour_entry_to = Spinbox(self.rent_hour_min_to_frame, width=2, from_=00, to=23, format='%02.0f')
        self.rent_minute_label_to = Label(self.rent_hour_min_to_frame, text='Minutes', pady=5)
        self.rent_minute_entry_to = Spinbox(self.rent_hour_min_to_frame, width=2, from_=00, to=60, format='%02.0f')
        self.rent_to_space = Label(self.rent_hour_min_to_frame, width=1)

        self.rent_hour_label_to.grid(column=1, row=1)
        self.rent_hour_entry_to.grid(column=2, row=1)
        self.rent_to_space.grid(column=3, row=1)
        self.rent_minute_label_to.grid(column=4, row=1)
        self.rent_minute_entry_to.grid(column=5, row=1)

        self.rent_reg_label.grid(column=1, row=1)
        self.rent_reg_entry.grid(column=2, row=1)
        self.rent_space1.grid(column=3, row=1)
        self.rent_userid_label.grid(column=4, row=1)
        self.rent_userid_entry.grid(column=5, row=1)
        self.rent_from_label.grid(column=1, row=2)
        self.rent_from_entry.grid(column=2, row=2)
        self.rent_hour_min_from_frame.grid(column=0, row=3, columnspan=4)
        self.rent_space3.grid(column=3, row=2)
        self.rent_to_label.grid(column=4, row=2)
        self.rent_to_entry.grid(column=5, row=2)
        self.rent_hour_min_to_frame.grid(column=4, row=3, columnspan=2)
        self.rent_price_tot_label.grid(column=2, row=4)
        self.rent_price_tot_entry.grid(column=3, row=4, pady=10)

        # Placeholders
        self.car_current = None
        self.user_current = None
        self.rent_current = None

        # Making frames for options
        self.options_user = Frame(self)
        self.options_car = Frame(self)
        self.options_rent = Frame(self)

        # Making widgets inside options frames

        # User options
        self.edit_user = Button(self.options_user, width=5, text='Edit', command=self.edit_one_user)
        self.delete_user = Button(self.options_user, width=5, text='Delete', command=self.delete_one_user)

        self.space_user = Label(self.options_user, width='5')

        self.edit_user.grid(row=2, column=1)
        self.space_user.grid(row=2, column=2)
        self.delete_user.grid(row=2, column=3)

        # Car options
        self.edit_car = Button(self.options_car, width='7', text='Edit', command=self.edit_one_car)
        self.delete_car = Button(self.options_car, width='7', text='Delete', command=self.delete_one_car)
        self.rent_car = Button(self.options_car, width='7', text='Rent out', command=self.open_user_window)
        self.space_car1 = Label(self.options_car, width='5')
        self.space_car2 = Label(self.options_car, width='5')

        self.edit_car.grid(column=1, row=1)
        self.space_car1.grid(column=2, row=1)
        self.delete_car.grid(column=3, row=1)
        self.space_car2.grid(column=4, row=1)
        self.rent_car.grid(column=5, row=1)

        # Rent options
        self.edit_rental = Button(self.options_rent, width=7, text='Edit', command=self.edit_one_rental)
        self.delete_rental = Button(self.options_rent, width=7, text='Delete', command=self.delete_one_rental)
        self.space_rent1 = Label(self.options_rent, width=5)

        self.edit_rental.grid(column=1, row=1)
        self.space_rent1.grid(column=2, row=1)
        self.delete_rental.grid(column=3, row=1)

        # The label shown when clicking on a user, car or rental
        self.one_car_label = Label(self.options_car)
        self.one_user_label = Label(self.options_user)
        self.one_rental_label = Label(self.options_rent)
        self.one_user_label['pady'] = 30

        # Making frames for search bars
        self.user_frame = Frame(self)
        self.car_frame = Frame(self)
        self.rent_frame = Frame(self)

        # Making stuff within these frames.

        # User frame
        user_options = ['id', 'name', 'address', 'phone', 'age']
        self.user_choice = StringVar(self.user_frame)
        self.user_choice.set(user_options[0])
        self.user_menu = OptionMenu(self.user_frame, self.user_choice, *user_options)
        self.search_user_btn = Button(self.user_frame, text='Search', command=self.search_users)
        self.search_bar = Entry(self.user_frame)
        self.search_label = Label(self.user_frame, text="Search for users by:")
        self.search_label.pack()
        self.user_menu.pack()
        self.search_bar.pack()
        self.search_user_btn.pack()

        # Car frame
        cars_options = ['reg number', 'model', 'year']
        self.cars_choice = StringVar(self.car_frame)
        self.cars_choice.set(cars_options[0])
        self.cars_menu = OptionMenu(self.car_frame, self.cars_choice, *cars_options)
        self.search_car_btn = Button(self.car_frame, text='Search', command=self.search_cars)
        self.search_bar_car = Entry(self.car_frame)
        self.search_label_car = Label(self.car_frame, text="Search for cars by:")
        self.search_label_car.pack()
        self.cars_menu.pack()
        self.search_bar_car.pack()
        self.search_car_btn.pack()

        # Rental frame
        rent_options = ['id', 'user id', 'reg number', 'year']
        self.rent_choice = StringVar(self.rent_frame)
        self.rent_choice.set(rent_options[0])
        self.rent_menu = OptionMenu(self.rent_frame, self.rent_choice, *rent_options)
        self.search_rent_btn = Button(self.rent_frame, text='Search', command=self.search_rentals)
        self.search_bar_rent = Entry(self.rent_frame)
        self.search_label_rent = Label(self.rent_frame, text="Search for rentals by:")
        self.search_label_rent.pack()
        self.rent_menu.pack()
        self.search_bar_rent.pack()
        self.search_rent_btn.pack()

        # Frame for page select
        self.page_frame = Frame(self)
        self.info_label_pages = Label(self.page_frame, text='Items per page')
        self.pages_to_show = Entry(self.page_frame)
        self.ok_btn = Button(self.page_frame, text='Display', command=self.page_handler)

        self.user_frame.grid(column=2, row=1, pady=10)
        self.car_frame.grid(column=2, row=2, pady=10)
        self.rent_frame.grid(column=2, row=3, pady=10)
        self.page_frame.grid(column=2, row=4, pady=10)

        # Making some space
        self.space1 = Label(self, widt=20)
        self.space2 = Label(self, width=20)
        self.space1.grid(column=2)
        self.space2.grid(column=4)

        self.error = Label(self, text='Nothing to display', pady=10)

        # Creating the buttons for switching pages
        self.next = Button(self, text='Next page', command=self.next_page, cnf=size, )
        self.prew_page = Button(self, text='Prew page', command=self.prev_page, cnf=size)
        self.display_pages = Label(self)

        # Frame for the page function
        self.pages_frame = Frame(self)

        # Making the main buttons for getting all user,cars and rentals and creating them

        self.get_all_users = Button(self, text='All users',
                                    command=self.return_all_users, cnf=size)
        self.get_all_cars = Button(self, text='All cars', command=self.return_all_cars,
                                   cnf=size)
        self.get_all_rentals = Button(self, text='All rentals', pady=10, cnf=size,
                                      command=self.return_all_rentals)

        self.get_all_users.grid(column=1, row=1)
        self.get_all_cars.grid(column=1, row=2)
        self.get_all_rentals.grid(column=1, row=3)

        # The creator buttons and frame
        self.creator_frame = Frame(self)
        self.create_user = Button(self.creator_frame, text='New User', command=partial(self.edit_one_user, post=True),
                                  cnf=size)
        self.create_car = Button(self.creator_frame, text='New Car', command=partial(self.edit_one_car, post=True),
                                 cnf=size)
        self.create_rental = Button(self.creator_frame, text='New Rental',
                                    command=partial(self.edit_one_rental, post=True), cnf=size)
        self.create_user.pack()
        self.create_car.pack()
        self.create_rental.pack()

        self.creator_frame.grid(column=5, row=1, rowspan=3)

        self.next.grid(column=1, row=4)
        self.prew_page.grid(column=1, row=5)

        # Frame for handling the rent out feature
        self.rent_out_frame = Frame(self)
        # Extra frames for spinboxes
        self.rent_out_from_frame = Frame(self.rent_out_frame)
        self.rent_out_to_frame = Frame(self.rent_out_frame)

        # Making frames inside rent out frame for time from
        self.rent_out_hour_label_from = Label(self.rent_out_from_frame, text='Hours')
        self.rent_out_hour_entry_from = Spinbox(self.rent_out_from_frame, width=2, from_=00, to=23, format='%02.0f')
        self.rent_out_minute_label_from = Label(self.rent_out_from_frame, text='Minutes')
        self.rent_out_minute_entry_from = Spinbox(self.rent_out_from_frame, width=2, from_=00, to=60, format='%02.0f')
        self.rent_out_from_space = Label(self.rent_out_from_frame, width=1)

        self.rent_out_hour_label_from.grid(column=1, row=1)
        self.rent_out_hour_entry_from.grid(column=2, row=1)
        self.rent_out_from_space.grid(column=3, row=1)
        self.rent_out_minute_label_from.grid(column=4, row=1)
        self.rent_out_minute_entry_from.grid(column=5, row=1)

        # Making frames inside rent out frame for time to
        self.rent_out_hour_label_to = Label(self.rent_out_to_frame, text='Hours', pady=10)
        self.rent_out_hour_entry_to = Spinbox(self.rent_out_to_frame, width=2, from_=00, to=23, format='%02.0f')
        self.rent_out_minute_label_to = Label(self.rent_out_to_frame, text='Minutes', pady=5)
        self.rent_out_minute_entry_to = Spinbox(self.rent_out_to_frame, width=2, from_=00, to=60, format='%02.0f')
        self.rent_out_to_space = Label(self.rent_out_to_frame, width=1)

        self.rent_out_hour_label_to.grid(column=1, row=1)
        self.rent_out_hour_entry_to.grid(column=2, row=1)
        self.rent_out_to_space.grid(column=3, row=1)
        self.rent_out_minute_label_to.grid(column=4, row=1)
        self.rent_out_minute_entry_to.grid(column=5, row=1)

        # Labels and buttons inside rent out frame
        self.rent_out_car_label = Label(self.rent_out_frame, font=20, pady=20)
        self.rent_out_user_label = Label(self.rent_out_frame, font=20)
        self.rent_out_from_date = DateEntry(self.rent_out_frame, width=12, background='darkblue', foreground='white',
                                            borderwidth=2, date_pattern='yyyy-mm-dd')
        self.rent_out_to_date = DateEntry(self.rent_out_frame, width=12, background='darkblue', foreground='white',
                                          borderwidth=2, date_pattern='yyyy-mm-dd')
        self.rent_out_from_label = Label(self.rent_out_frame, text='Rent from:')
        self.rent_out_to_label = Label(self.rent_out_frame, text='Rent to:')
        self.rent_out_space1 = Label(self.rent_out_frame, width=3)
        self.rent_out_space2 = Label(self.rent_out_frame, height=2)
        self.rent_out_price_label = Label(self.rent_out_frame, text="Total price for rent: ")
        self.rent_out_price_entry = Entry(self.rent_out_frame)
        self.rent_out_space3 = Label(self.rent_out_frame, height=3)
        self.rent_out_submit_btn = Button(self.rent_out_frame, text='Create new rental',
                                          command=self.top_post_featured_rental)

        self.rent_out_user_label.grid(column=1, row=0, columnspan=4)
        self.rent_out_car_label.grid(column=1, row=1, columnspan=4)
        self.rent_out_space1.grid(column=2, row=2)
        self.rent_out_from_label.grid(column=0, row=3)
        self.rent_out_from_date.grid(column=1, row=3)
        self.rent_out_space2.grid(column=2, row=3)
        self.rent_out_to_label.grid(column=3, row=3)
        self.rent_out_to_date.grid(column=4, row=3)
        self.rent_out_from_frame.grid(column=0, row=4, columnspan=2)
        self.rent_out_to_frame.grid(column=3, row=4, columnspan=2)
        self.rent_out_price_label.grid(column=1, row=5)
        self.rent_out_price_entry.grid(column=2, row=5, pady=10)
        self.rent_out_space3.grid(column=2, row=6)
        self.rent_out_submit_btn.place(x=185, y=335)

    def open_user_window(self):
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        user_options = ['id', 'name', 'address', 'phone', 'age']
        self.pick_user_window = Toplevel(self)

        self.pick_user_window.minsize(800, 400)

        center(self.pick_user_window)

        self.tree = ttk.Treeview(self.pick_user_window, columns=('Name', 'Address', 'Phone', 'Age'))

        self.tree.heading('#0', text='Id')
        self.tree.heading('#1', text='Name')
        self.tree.heading('#2', text='Address')
        self.tree.heading('#3', text='Phone')
        self.tree.heading('#4', text='Age')
        self.tree.column('#0', width=40)

        self.tree.pack(expand=YES, fill=BOTH)

        self.choices = StringVar(self.pick_user_window)
        self.top_choices = StringVar(self.pick_user_window)
        self.top_choices.set(user_options[0])
        self.top_user_menu = OptionMenu(self.pick_user_window, self.top_choices, *user_options)
        self.top_search_user_btn = Button(self.pick_user_window, text='Search', command=self.top_search_users)
        self.top_search_bar = Entry(self.pick_user_window)
        self.top_search_label = Label(self.pick_user_window, text='Search for users by:')
        self.top_error_label = Label(self.pick_user_window, foreground='red')
        self.top_select_btn = Button(self.pick_user_window, text='Select', pady=10, width=8, command=self.top_get_user)
        self.top_error_label.pack()
        self.top_search_label.pack()
        self.top_user_menu.pack()
        self.top_search_bar.pack()
        self.top_search_user_btn.pack()
        self.pick_user_window.grab_set()
        self.top_space = Label(self.pick_user_window, height=1).pack()
        self.top_select_btn.pack()

    def top_search_users(self):
        self.top_error_label["text"] = ''
        self.tree.delete(*self.tree.get_children())
        action = self.top_choices.get()
        try:
            if self.top_search_bar.get() == '':
                response = users(get=True)
            elif action == 'id':
                response = users(get=True, user_id=self.top_search_bar.get())
            elif action == 'name':
                response = users(get=True, name=self.top_search_bar.get())
            elif action == 'address':
                response = users(get=True, address=self.top_search_bar.get())
            elif action == 'phone':
                response = users(get=True, phone=self.top_search_bar.get())
            elif action == 'age':
                response = users(get=True, age=self.top_search_bar.get())
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')

        if 'message' in response:
            self.top_error_label["text"] = f'No user with {action}: {self.top_search_bar.get()}'
            return -1
        else:
            for i, user in enumerate(response):
                self.tree.insert('', 'end', iid=i, text=user["id"],
                                 values=(user["name"], user["address"], user["phone"],
                                         relativedelta(datetime.now(),
                                                       datetime.strptime(user["birth"], "%Y-%m-%d")).years))

    def top_get_user(self):
        self.rent_out_price_entry.delete(0, 'end')
        user = self.tree.item(self.tree.focus())
        if len(user["values"]) < 4:
            return -1
        self.user_current = {"id": user["text"],
                             "name": user["values"][0],
                             "address": user["values"][1],
                             "phone": user["values"][2],
                             "birth": user["values"][3]
                             }

        self.rent_out_user_label["text"] = \
            f'ID: {self.user_current["id"]}\nName: {self.user_current["name"]}\nAddress:' \
            f' {self.user_current["address"]}\nPhone: {self.user_current["phone"]}\nAge: ' \
            f'{self.user_current["birth"]}'

        self.rent_out_car_label["text"] = \
            f'Registration number: {self.car_current["reg_number"]}\nModel name: ' \
            f'{self.car_current["model"]}\nRegistration year: {self.car_current["year"]}\n' \
            f'Price per day: {self.car_current["price"]}'
        self.pick_user_window.destroy()
        self.main_page()
        self.rent_out_frame.place(relx=0.37, rely=0.08)

    def top_post_featured_rental(self):
        self.rent_current = dict()
        self.rent_current["price_tot"] = -1
        try:
            self.error_message.destroy()
        except AttributeError:
            pass
        rent_from = re.findall('(\d{4}-\d{2}-\d{2}){1}', self.rent_out_from_date.get())
        rent_to = re.findall('(\d{4}-\d{2}-\d{2}){1}', self.rent_out_to_date.get())
        rent_from_hour = re.findall('(\d{1,2}){1}', self.rent_out_hour_entry_from.get())
        rent_from_min = re.findall('(\d{2}){1}', self.rent_out_minute_entry_from.get())
        rent_to_hour = re.findall('(\d{2}){1}', self.rent_out_hour_entry_to.get())
        rent_to_min = re.findall('(\d{2}){1}', self.rent_out_minute_entry_to.get())
        if len(rent_from) != 1 or len(rent_to) != 1 or len(rent_from_hour) != 1 or \
                len(rent_from_min) != 1 or len(rent_to_hour) != 1 or len(rent_to_min) != 1:
            showerror("Error", "Invalid time format")
            return -1
        self.rent_current["rent_from"] = f'{rent_from[0]} {rent_from_hour[0]}:{rent_from_min[0]}:00'
        self.rent_current["rent_to"] = f'{rent_to[0]} {rent_to_hour[0]}:{rent_to_min[0]}:00'
        self.rent_current["reg_number"] = self.car_current["reg_number"]
        self.rent_current["user_id"] = self.user_current["id"]

        if str(self.rent_current["price_tot"]) == str(
                self.rent_out_price_entry.get()) or self.rent_out_price_entry.get() == '':
            try:
                try:
                    price = cars(get=True, reg=self.rent_current["reg_number"])[0]["price"]
                    if price is None:
                        showerror("Price is None", 'Price seems to be None, you should insert it manually')
                        return -1
                    self.rent_current["price_tot"] = \
                        int(price) * (datetime.strptime(self.rent_current["rent_to"], "%Y-%m-%d %H:%M:%S") -
                                      datetime.strptime(self.rent_current["rent_from"], "%Y-%m-%d %H:%M:%S")).days
                    self.rent_out_price_entry.delete(0, 'end')
                    self.rent_out_price_entry.insert(0, self.rent_current["price_tot"])
                except ValueError:
                    showerror("Error", "Invalid price")
                    return -1
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
        else:
            try:
                self.rent_current["price_tot"] = int(self.rent_out_price_entry.get())
            except ValueError:
                showerror("Error", "Invalid price")
                return -1

        try:
            response = rentals(post=True, json=self.rent_current)
        except ConnectionError:
            showerror('Connection error', 'Cant connect to server')
            return -1

        if 'message' in response:
            self.error_message = Label(self.rent_out_frame, fg='red')
            self.error_message["text"] = response["message"]
            self.error_message.grid(column=1, row=7, columnspan=4, pady=20)
            return -1
        self.one_rental(response[0])
        showinfo(title='Success', message='Rental successfully created')

    def next_page(self):
        try:
            if self.page <= (len(self.pages)) - 2:
                self.page += 1
                self.page_handler()
        except TclError:
            pass

    def prev_page(self):
        try:
            if self.page != 0:
                self.page -= 1
                self.page_handler()
        except TclError:
            pass

    def main_page(self):
        self.error.place_forget()
        self.rent_out_frame.place_forget()
        self.car_commit.grid_forget()
        self.pages_frame.place_forget()
        self.options_user.place_forget()
        self.options_car.place_forget()
        self.options_rent.place_forget()
        self.one_user_label.grid_forget()
        self.one_car_label.grid_forget()
        self.one_rental_label.grid_forget()
        self.edit_user_frame.place_forget()
        self.edit_car_frame.place_forget()
        self.edit_rental_frame.place_forget()
        try:
            self.error_message.destroy()
        except AttributeError:
            pass
        self.page = 0
        for i in self.pages:
            for p in i:
                p.destroy()

    def page_handler(self):
        """ This function handles every aspect of the pages"""
        self.error.grid_forget()
        try:
            if self.displayed != int(self.pages_to_show.get()):
                self.page = 0
            self.displayed = int(self.pages_to_show.get())

        except:
            self.displayed = 5
        if self.displayed <= 0:
            self.displayed = 5
        if self.last_page is not None:
            for i in self.pages[self.last_page]:
                i.grid_forget()

        temp = []
        try:
            if isinstance(self.pages[0], list):
                self.pages = list(itertools.chain(*self.pages))
        except IndexError:
            return -1

        for i in range(math.ceil(len(self.pages) / self.displayed)):
            temp.append([])
            for count, item in enumerate(self.pages):
                item["height"] = 6
                item["pady"] = 10
                item.update()
                temp[i].append(item)

                if count == self.displayed - 1: break
            for p in range(self.displayed):
                try:
                    self.pages.pop(0)
                except IndexError:
                    break
        self.pages = [[p for p in i] for i in temp]  # Shoving temp into self.pages
        del temp  # Deleting temp to make clear it was just temporary

        if len(self.pages) > 0:
            for count, i in enumerate(self.pages[self.page]):
                i.grid(column=3, row=count + 1)

        self.display_pages['text'] = f'page {self.page + 1} of {len(self.pages)}'
        self.display_pages.update()
        self.last_page = self.page

        self.pages_frame.place(relx=0.32, rely=0)

    def users_handler(self, user_list):
        """This function handles users and makes the buttons before it sends it to the page
        function to be paged"""
        self.main_page()
        try:
            user_list = user_list()
        except TypeError:
            pass
        self.last_page = None
        self.pages = []

        if 'message' in user_list:
            for i in self.pages:
                i.grid_forget()
            self.error["text"] = user_list["message"]
            self.error["fg"] = 'red'
            self.error.place(relx=0.45, rely=0.3)
            return -1

        for user in user_list:
            self.btn = Button(self.pages_frame, command=partial(self.one_user, user))
            self.btn["command"] = partial(self.one_user, user)
            try:
                self.btn["text"] = f'User id: {user["id"]}\nName: {user["name"]} \nAddress:' \
                                   f' {user["address"]}\nPhone number: {user["phone"]}\nAge:' \
                                   f' {relativedelta(datetime.now(), datetime.strptime(user["birth"], "%Y-%m-%d")).years}'
            except:
                self.btn["text"] = f'User id: {user["id"]}\nName: {user["name"]} \nAddress:' \
                                   f' {user["address"]}\nPhone number: {user["phone"]}\nAge:' \
                                   f' {None}'
            self.btn["width"] = 90
            self.pages.append(self.btn)

        self.info_label_pages.pack()
        self.pages_to_show.pack()
        self.ok_btn.pack()
        self.display_pages.place(relx=0.5, rely=0.95)
        self.page_handler()

    def cars_handler(self, garage):
        """This function handles cars and makes the buttons before it sends it to the page
                function to be paged"""
        self.main_page()
        try:
            garage = garage()
        except TypeError:
            pass
        self.pages = []
        self.last_page = None

        if 'message' in garage:
            for i in self.pages:
                i.grid_forget()
            self.error["text"] = garage["message"]
            self.error["fg"] = 'red'
            self.error.place(relx=0.45, rely=0.3)
            return -1

        for count, car in enumerate(garage):
            self.btn = Button(self.pages_frame, command=self.one_car)
            self.btn["command"] = partial(self.one_car, car)
            self.btn[
                "text"] = f'Registration number: {car["reg_number"]} \nModel name: {car["model"]} \nRegistration year: {car["year"]}' \
                          f'\nPrice per day: {car["price"]} Kr'
            self.btn["width"] = 90
            self.pages.append(self.btn)

        self.info_label_pages.pack()
        self.pages_to_show.pack()
        self.ok_btn.pack()
        self.display_pages.place(relx=0.5, rely=0.95)
        self.page_handler()

    def rental_handler(self, rental):
        """This function handles rentals and makes the buttons before it sends it to the page
                function to be paged"""
        self.main_page()
        try:
            rental = rental()
        except TypeError:
            pass
        self.pages = []
        self.last_page = None

        if 'message' in rental:
            for i in self.pages:
                i.grid_forget()
            self.error["text"] = rental["message"]
            self.error["fg"] = 'red'
            self.error.place(relx=0.5, rely=0.3)
            return -1

        for count, rent in enumerate(rental):
            self.btn = Button(self.pages_frame, command=partial(self.one_rental, rent))
            self.btn[
                "text"] = f'Rental id: {rent["id"]} \nUser id: {rent["user_id"]}\nRegistration number: {rent["reg_number"]}\n' \
                          f'Rented from: {rent["rent_from"].replace("T", " ")}\nRented to: {rent["rent_to"].replace("T", " ")}\n' \
                          f'Total price for rent: {rent["price_tot"]}'
            self.btn["width"] = 90
            self.pages.append(self.btn)

        self.info_label_pages.pack()
        self.pages_to_show.pack()
        self.ok_btn.pack()
        self.display_pages.place(relx=0.5, rely=0.95)
        self.page_handler()

    def search_users(self):
        """This function handles all the searches done for users"""
        if self.search_bar.get() == '':
            return -1
        action = self.user_choice.get()
        try:
            if action == 'id':
                self.users_handler(users(get=True, user_id=self.search_bar.get()))
            elif action == 'name':
                self.users_handler(users(get=True, name=self.search_bar.get()))
            elif action == 'address':
                self.users_handler(users(get=True, address=self.search_bar.get()))
            elif action == 'phone':
                self.users_handler(users(get=True, phone=self.search_bar.get()))
            elif action == 'age':
                self.users_handler(users(get=True, age=self.search_bar.get()))
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')

    def search_cars(self):
        """This function handles all the searches done for cars"""
        if self.search_bar_car.get() == '':
            return -1
        action = self.cars_choice.get()
        try:
            if action == 'reg number':
                self.cars_handler(cars(get=True, reg=self.search_bar_car.get()))
            elif action == 'model':
                self.cars_handler(cars(get=True, model=self.search_bar_car.get()))
            elif action == 'year':
                self.cars_handler(cars(get=True, year=self.search_bar_car.get()))
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')

    def search_rentals(self):
        """This function handles all the searches done for rentals"""
        if self.search_bar_rent.get() == '':
            return -1
        action = self.rent_choice.get()
        try:
            if action == 'id':
                self.rental_handler(rentals(get=True, rental_id=self.search_bar_rent.get()))
            elif action == 'user id':
                self.rental_handler(rentals(get=True, user_id=self.search_bar_rent.get()))
            elif action == 'reg number':
                self.rental_handler(rentals(get=True, reg=self.search_bar_rent.get()))
            elif action == 'year':
                try:
                    rent_from = self.search_bar_rent.get()
                    rent_to = rent_from
                    self.rental_handler(rentals(get=True, rfrom=rent_from, rto="".join(rent_to)))
                except ValueError:
                    pass
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')

    def one_car(self, car):
        self.main_page()
        self.car_current = car
        self.one_car_label["text"] = \
            f'Registration number: {car["reg_number"]}\nModel name: {car["model"]}\nRegistration year: {car["year"]}\n' \
            f'Price per day: {car["price"]} Kr'
        self.one_car_label.config(font=20, pady=40)
        self.one_car_label.update()
        self.one_car_label.grid(column=3, row=0)

        self.options_car.place(relx=0.38, rely=0.2)

    def edit_one_car(self, post=False):
        if post:
            self.main_page()
            self.edit_cars_label.grid_forget()
            self.car_commit.grid_forget()
            self.car_commit_post.grid(column=1, row=5, columnspan=2, pady=20)
        self.options_car.grid_forget()

        self.car_reg_number_entry.delete(0, 'end')
        self.car_model_entry.delete(0, 'end')
        self.car_year_entry.delete(0, 'end')
        self.car_price_entry.delete(0, 'end')
        if not post:
            self.car_commit_post.grid_forget()
            self.edit_car_frame.place(relx=0.43, rely=0.15)
            self.edit_cars_label.grid(column=1, row=0, columnspan=2, pady=40)
            self.edit_cars_label["text"] = \
                f'Registration number: {self.car_current["reg_number"]}\nModel name: ' \
                f'{self.car_current["model"]}\nRegistration year: {self.car_current["year"]}\n' \
                f'Price per day: {self.car_current["price"]} Kr'
            self.edit_cars_label.update()
            self.options_car.place_forget()
            self.car_reg_number_entry.insert(0, self.car_current["reg_number"])
            self.car_model_entry.insert(0, self.car_current["model"])
            self.car_year_entry.insert(0, self.car_current["year"])
            self.car_price_entry.insert(0, self.car_current["price"])
            self.car_commit.grid(column=1, row=5, columnspan=2, pady=20)
        else:
            self.edit_car_frame.place(relx=0.375, rely=0.22)

    def put_car(self, post=False):
        if post:
            self.car_current = dict()
        try:
            self.car_current["year"] = int(self.car_year_entry.get())
        except ValueError:
            showerror("Error", "Year must be a number with format YYYY")
            return -1
        try:
            self.car_current["price"] = int(self.car_price_entry.get())
        except ValueError:
            showerror("Error", "Price must be a number")
            return -1
        self.car_current["model"] = self.car_model_entry.get()
        if not post:
            try:
                temp_reg = self.car_current["reg_number"]
                self.car_current["reg_number"] = self.car_reg_number_entry.get()
                response = cars(put=True, json=self.car_current, reg=temp_reg)
                if 'message' in response:
                    self.error_message = Label(self.edit_car_frame, fg='red')
                    self.error_message["text"] = response["message"]
                    self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
                    return -1

            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1

            self.edit_cars_label["text"] = f'Registration number: {self.car_current["reg_number"]}\nModel name: ' \
                                           f'{self.car_current["model"]}\nRegistration year: {self.car_current["year"]}\n' \
                                           f'Price per day: {self.car_current["price"]} Kr'

            showinfo(title='Success', message='Car successfully modified')
        else:
            self.car_current["reg_number"] = self.car_reg_number_entry.get()

            try:
                response = cars(post=True, json=self.car_current)
                if 'message' in response:
                    self.error_message = Label(self.edit_car_frame, fg='red')
                    self.error_message["text"] = response["message"]
                    self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
                    return -1
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
            self.one_car(self.car_current)
            showinfo(title='Success', message='Car successfully created')

    def delete_one_car(self):
        if askyesno('Delete Car', 'Are you sure you want to delete this car?'):
            try:
                cars(delete=True, reg=self.car_current["reg_number"])
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
            showinfo('Success', 'Car successfully deleted')
            self.main_page()

    def one_user(self, user):
        self.main_page()
        self.user_current = user
        try:
            self.one_user_label["text"] = \
                f'ID: {user["id"]}\nName: {user["name"]}\nAddress:' \
                f' {user["address"]}\nPhone: {user["phone"]}\nAge: {relativedelta(datetime.now(), datetime.strptime(user["birth"], "%Y-%m-%d")).years}'
        except:
            self.one_user_label["text"] = \
                f'ID: {user["id"]}\nName: {user["name"]}\nAddress:' \
                f' {user["address"]}\nPhone: {user["phone"]}\nAge: {None}'
        self.one_user_label.config(font=20)
        self.one_user_label.update()
        self.one_user_label.grid(row=1, column=2)

        self.options_user.place(relx=0.45, rely=0.2)

    def edit_one_user(self, post=False):
        self.edit_user_label.grid(column=6, row=0)
        self.options_user.grid_forget()
        self.user_put.grid_forget()
        self.user_post.grid_forget()
        self.user_name_entry.delete(0, "end")
        self.user_address_entry.delete(0, "end")
        self.user_phone_entry.delete(0, "end")
        self.user_age_entry.delete(0, "end")
        if not post:
            self.user_put.grid(column=6, row=8, pady=20)
            self.user_name_entry.insert(0, self.user_current["name"])
            self.user_address_entry.insert(0, self.user_current["address"])
            self.user_phone_entry.insert(0, self.user_current["phone"])
            self.user_age_entry.insert(0, str(self.user_current["birth"]))
            try:
                self.edit_user_label["text"] = \
                    f'ID: {self.user_current["id"]}\nName: {self.user_current["name"]}\nAddress:' \
                    f' {self.user_current["address"]}\nPhone: {self.user_current["phone"]}\nAge: ' \
                    f'{relativedelta(datetime.now(), datetime.strptime(self.user_current["birth"], "%Y-%m-%d")).years}'
            except:
                self.one_user_label["text"] = \
                    f'ID: {self.user_current["id"]}\nName: {self.user_current["name"]}\nAddress:' \
                    f' {self.user_current["address"]}\nPhone: {self.user_current["phone"]}\nAge: {None}'
        else:
            self.edit_user_label.grid_forget()
            self.main_page()
            self.user_post.grid(column=6, row=8, pady=20)

        self.options_user.place_forget()
        self.edit_user_frame.place(relx=0.4, rely=0.2)

    def put_one_user(self, post=False):
        temp = re.findall('(\d{4}-\d{2}-\d{2}){1}', self.user_age_entry.get())
        if len(temp) != 1:
            showerror('Error', 'Invalid birth')
            return -1
        if post:
            self.user_current = dict()
        self.user_current["birth"] = temp[0]
        self.user_current["name"] = self.user_name_entry.get()
        self.user_current["address"] = self.user_address_entry.get()
        self.user_current["phone"] = self.user_phone_entry.get()
        if post:
            try:
                response = users(post=True, json=self.user_current)
                if 'message' in response:
                    self.error_message = Label(self.edit_user_frame, fg='red')
                    self.error_message["text"] = response["message"]
                    self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
                    return -1
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')

        if not post:
            try:
                response = users(put=True, json=self.user_current)
                if 'message' in response:
                    self.error_message = Label(self.edit_user_frame, fg='red')
                    self.error_message["text"] = response["message"]
                    self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
                    return -1
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
        self.user_current = response[0]
        self.edit_user_label["text"] = \
            f'ID: {self.user_current["id"]}\nName: {self.user_current["name"]}\nAddress:' \
            f' {self.user_current["address"]}\nPhone: {self.user_current["phone"]}\nAge: ' \
            f'{relativedelta(datetime.now(), datetime.strptime(self.user_current["birth"], "%Y-%m-%d")).years}'
        self.edit_user_label.update()
        if not post:
            showinfo(title='Success', message='User successfully modified')
        else:
            self.one_user(self.user_current)
            showinfo(title='Success', message='User successfully created')

    def delete_one_user(self):
        if askyesno('Delete user', 'Are you sure you want to delete this user?'):
            try:
                users(delete=True, user_id=self.user_current["id"])
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
            showinfo('Success', 'User successfully deleted')
            self.main_page()

    def one_rental(self, rental):
        self.main_page()
        self.rent_current = rental
        self.one_rental_label["text"] = \
            f'ID: {rental["id"]}\nUser id: {rental["user_id"]}\nRegistration number: {rental["reg_number"]}\n' \
            f'Rented from: {rental["rent_from"].replace("T", " ")}\nRented to: {rental["rent_to"].replace("T", " ")}\n' \
            f'Total price for rent: {rental["price_tot"]}'
        self.one_rental_label.config(font=20)
        self.one_rental_label.update()
        self.one_rental_label.grid(column=1, row=0, pady=30, columnspan=3)

        self.options_rent.place(relx=0.45, rely=0.2)

    def edit_one_rental(self, post=False):
        self.rent_submit.grid_forget()
        self.rent_submit_post.grid_forget()
        self.options_rent.place_forget()
        self.rent_hour_entry_from.delete(0, 'end')
        self.rent_minute_entry_from.delete(0, 'end')
        self.rent_hour_entry_to.delete(0, 'end')
        self.rent_minute_entry_to.delete(0, 'end')
        self.rent_reg_entry.delete(0, 'end')
        self.rent_userid_entry.delete(0, 'end')
        self.rent_from_entry.delete(0, 'end')
        self.rent_to_entry.delete(0, 'end')
        self.rent_price_tot_entry.delete(0, 'end')

        if not post:
            self.rent_submit.grid(column=3, row=5)
            self.rent_hour_entry_from.insert(0, self.rent_current["rent_from"].split('T')[1].split(':')[0])
            self.rent_minute_entry_from.insert(0, self.rent_current["rent_from"].split('T')[1].split(':')[1])
            self.rent_hour_entry_to.insert(0, self.rent_current["rent_to"].split('T')[1].split(':')[0])
            self.rent_minute_entry_to.insert(0, self.rent_current["rent_to"].split('T')[1].split(':')[1])

            self.rent_from_entry.insert(0, self.rent_current["rent_from"].split('T')[0])
            self.rent_to_entry.insert(0, self.rent_current["rent_to"].split('T')[0])
            self.rent_userid_entry.insert(0, self.rent_current["user_id"])
            self.rent_reg_entry.insert(0, self.rent_current["reg_number"])
            if not self.rent_current["price_tot"]:
                pass
            else:
                self.rent_price_tot_entry.insert(0, self.rent_current["price_tot"])
            self.rent_label_edit["text"] = \
                f'ID: {self.rent_current["id"]}\nUser id: {self.rent_current["user_id"]}\nRegistration number: {self.rent_current["reg_number"]}\n' \
                f'Rented from: {self.rent_current["rent_from"].replace("T", " ")}\nRented to: {self.rent_current["rent_to"].replace("T", " ")}\n' \
                f'Total price for rent: {self.rent_current["price_tot"]}'
            self.rent_label_edit.grid(column=2, row=0, columnspan=4)
        else:
            self.main_page()
            self.rent_label_edit.grid_forget()
            self.rent_hour_entry_from.insert(0, '00')
            self.rent_minute_entry_from.insert(0, '00')
            self.rent_hour_entry_to.insert(0, '00')
            self.rent_minute_entry_to.insert(0, '00')
            self.rent_submit_post.grid(column=3, row=5)

        self.edit_rental_frame.place(relx=0.3, rely=0.2)

    def put_one_rental(self, post=False):
        if post:
            self.rent_current = dict()
            self.rent_current["price_tot"] = -1

        try:
            self.error_message.destroy()
        except AttributeError:
            pass
        rent_from = re.findall('(\d{4}-\d{2}-\d{2}){1}', self.rent_from_entry.get())
        rent_to = re.findall('(\d{4}-\d{2}-\d{2}){1}', self.rent_to_entry.get())
        rent_from_hour = re.findall('(\d{1,2}){1}', self.rent_hour_entry_from.get())
        rent_from_min = re.findall('(\d{2}){1}', self.rent_minute_entry_from.get())
        rent_to_hour = re.findall('(\d{2}){1}', self.rent_hour_entry_to.get())
        rent_to_min = re.findall('(\d{2}){1}', self.rent_minute_entry_to.get())
        if len(rent_from) != 1 or len(rent_to) != 1 or len(rent_from_hour) != 1 or \
                len(rent_from_min) != 1 or len(rent_to_hour) != 1 or len(rent_to_min) != 1:
            showerror("Error", "Invalid time format")
            return -1
        self.rent_current["rent_from"] = f'{rent_from[0]} {rent_from_hour[0]}:{rent_from_min[0]}:00'
        self.rent_current["rent_to"] = f'{rent_to[0]} {rent_to_hour[0]}:{rent_to_min[0]}:00'
        self.rent_current["reg_number"] = self.rent_reg_entry.get()
        self.rent_current["user_id"] = self.rent_userid_entry.get()
        if self.rent_current["reg_number"] == '':
            showerror('Error', 'Registration number is required')
            return -1

        response = cars(get=True, reg_absolute=self.rent_current["reg_number"])
        if 'message' in response.json():
            self.error_message = Label(self.edit_rental_frame, fg='red')
            self.error_message["text"] = response.json()["message"]
            self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
            return -1

        if str(self.rent_current["price_tot"]) == \
                str(self.rent_price_tot_entry.get()) or (post and self.rent_price_tot_entry.get() == ''):
            try:
                try:
                    price = cars(get=True, reg=self.rent_current["reg_number"])[0]["price"]
                    if price is None and self.rent_price_tot_entry.get() == '':
                        showerror("Error", 'Price seems to be None, you should insert it manually')
                        return -1
                    elif price is None:
                        try:
                            self.rent_current["price_tot"] = int(self.rent_price_tot_entry.get())
                        except ValueError:
                            showerror("Error", "Invalid price")
                            return -1
                    else:
                        self.rent_current["price_tot"] = \
                            int(price) * (datetime.strptime(self.rent_current["rent_to"], "%Y-%m-%d %H:%M:%S") -
                                          datetime.strptime(self.rent_current["rent_from"], "%Y-%m-%d %H:%M:%S")).days
                        self.rent_price_tot_entry.delete(0, 'end')
                        self.rent_price_tot_entry.insert(0, self.rent_current["price_tot"])
                except ValueError:
                    showerror("Error", "Invalid price")
                    return -1
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
        else:
            try:
                self.rent_current["price_tot"] = int(self.rent_price_tot_entry.get())
            except ValueError:
                showerror("Error", "Invalid price")
                return -1

        if not post:
            try:
                response = rentals(put=True, json=self.rent_current)
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1

            if 'message' in response:
                self.error_message = Label(self.edit_rental_frame, fg='red')
                self.error_message["text"] = response["message"]
                self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
                return -1

            self.rent_label_edit["text"] = \
                f'ID: {self.rent_current["id"]}\nUser id: {self.rent_current["user_id"]}\nRegistration number: {self.rent_current["reg_number"]}\n' \
                f'Rented from: {self.rent_current["rent_from"].replace("T", " ")}\nRented to: {self.rent_current["rent_to"].replace("T", " ")}\n' \
                f'Total price for rent: {self.rent_current["price_tot"]}'

            showinfo(title='Success', message='Rental successfully modified')
        else:
            try:
                response = rentals(post=True, json=self.rent_current)
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1

            if 'message' in response:
                self.error_message = Label(self.edit_rental_frame, fg='red')
                self.error_message["text"] = response["message"]
                self.error_message.grid(column=2, row=6, columnspan=7, pady=20)
                return -1
            self.one_rental(response[0])
            showinfo(title='Success', message='Rental successfully created')

    def delete_one_rental(self):
        if askyesno('Delete rental', 'Are you sure you want to delete this rental?'):
            try:
                rentals(delete=True, rental_id=self.rent_current["id"])
            except ConnectionError:
                showerror('Connection error', 'Cant connect to server')
                return -1
            showinfo('Success', 'Rental successfully deleted')
            self.main_page()

    def return_all_users(self):
        try:
            self.users_handler(users(get=True))
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')
            return -1

    def return_all_cars(self):
        try:
            return self.cars_handler(cars(get=True))
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')
            return -1

    def return_all_rentals(self):
        try:
            return self.rental_handler(rentals(get=True))
        except ConnectionError:
            showerror('Connection Error', 'Cant connect to server')
            return -1


# The center function is not mine it was taken from:
# https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter/10018670#10018670
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

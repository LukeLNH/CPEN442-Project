# https://www.simplifiedpython.net/python-gui-login/

from tkinter import *
from dataclass import MasterAccount, MessagingAppProfile
import requests

def login():
    global login_screen

    login_screen = Tk()
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter your login credentials").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password__login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password__login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verification).pack()

    #https://stackoverflow.com/questions/111155/how-do-i-handle-the-window-close-event-in-tkinter
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.mainloop()
    
def on_closing():
    login_screen.destroy()

def login_verification():
    global success_screen

    success_screen = Toplevel(login_screen)
    success_screen.title("Login Success")
    success_screen.geometry("400x200")

    Label(success_screen, text="").pack()
    Label(success_screen, text=f"Welcome, User: {username_verify.get()}").pack()
    Label(success_screen, text="").pack()

    Button(success_screen, text="View Organizations associated with me", width=40, height=1, command=view_known_orgs_frame).pack()
    Button(success_screen, text="View my messaging accounts", width=40, height=1, command=view_messaging_accounts_frame).pack()
    Button(success_screen, text="Connect to CAIMAN through Org", width=40, height=1, command=connect_to_CAIMAN_frame).pack()
    Button(success_screen, text="Disconnect from CAIMAN", width=40, height=1, command=disconnect_from_CAIMAN_frame).pack()
    Button(success_screen, text="Remove an Org Key", width=40, height=1, command=revoke_key_frame).pack()
    
    success_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.withdraw()

def view_known_orgs_frame():
    known_profiles_screen = Toplevel(success_screen)
    known_profiles_screen.title("Known Organizations")
    known_profiles_screen.geometry("400x300")

    employee = MessagingAppProfile()
    employee.load_profile_from_id(username_verify.get())
    
    # https://stackoverflow.com/questions/20768405/print-dictionary-in-python-ttk
    header_text = 'Names of Organizations with assigned key'
    Label(known_profiles_screen, text=header_text).pack()

    text = '\n'.join(f"{k}" for k in employee.private_signatures.keys())
    Label(known_profiles_screen, text=text).pack()
    
    #known_profiles_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def view_messaging_accounts_frame():
    known_profiles_screen = Toplevel(success_screen)
    known_profiles_screen.title("Messaging Accounts")
    known_profiles_screen.geometry("400x300")
    
    # https://stackoverflow.com/questions/20768405/print-dictionary-in-python-ttk
    header_text = 'Messaging Accounts'
    Label(known_profiles_screen, text=header_text).pack()

    text = 'Happy People Messaging'
    Label(known_profiles_screen, text=text).pack()
    
    #known_profiles_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def connect_to_CAIMAN_frame():
    connect_frame = Toplevel(success_screen)
    connect_frame.title("Connect to CAIMAN")
    connect_frame.geometry("400x300")

    employee = MessagingAppProfile()
    employee.load_profile_from_id(username_verify.get())

    Label(connect_frame, text="").pack()
    Label(connect_frame, text="Select Organization *").pack()

    global organizations_dropdown
    organizations_dropdown = StringVar()
    organizations_dropdown_menu = OptionMenu(connect_frame, organizations_dropdown, *list(employee.private_signatures.keys()))
    organizations_dropdown_menu.pack()

    Label(connect_frame, text="").pack()
    Label(connect_frame, text="Select Messaging App *").pack()
    global messaging_dropdown
    messaging_dropdown = StringVar()
    messaging_app_dropdown_menu = OptionMenu(connect_frame, messaging_dropdown, 'Happy People Messaging')
    messaging_app_dropdown_menu.pack()

    Label(connect_frame, text="").pack()
    Label(connect_frame, text="").pack()
    Button(connect_frame, text="Connect to CAIMAN", width=20, height=1, command=connect_to_CAIMAN).pack()
    
    #assign_key_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def connect_to_CAIMAN():
    json_dict = {
        'Org_name': organizations_dropdown.get(),
        'Logged_in': True
    }

    url = 'http://127.0.0.1:5000/set_verification_org'
    requests.post(url=url, json=json_dict)

    connect_success_frame = Toplevel(success_screen)
    connect_success_frame.title("Connect Success")
    connect_success_frame.geometry("400x200")

    Label(connect_success_frame, text="").pack()
    Label(connect_success_frame, text=f"Successfully Logged into CAIMAN!").pack()
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def disconnect_from_CAIMAN_frame():
    json_dict = {
        'Org_name': '',
        'Logged_in': False
    }

    url = 'http://127.0.0.1:5000/set_verification_org'
    requests.post(url=url, json=json_dict)

    connect_success_frame = Toplevel(success_screen)
    connect_success_frame.title("Disconnect Success")
    connect_success_frame.geometry("400x200")

    Label(connect_success_frame, text="").pack()
    Label(connect_success_frame, text=f"Successfully disconnected from CAIMAN!").pack()
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def revoke_key_frame():
    revoke_key_frame = Toplevel(success_screen)
    revoke_key_frame.title("Revoke Key")
    revoke_key_frame.geometry("400x300")

    Label(revoke_key_frame, text="").pack()
    Label(revoke_key_frame, text="Select an Organization *").pack()

    employee = MessagingAppProfile()
    employee.load_profile_from_id(username_verify.get())

    global organizations_dropdown
    organizations_dropdown = StringVar()
    organizations_dropdown_menu = OptionMenu(revoke_key_frame, organizations_dropdown, *list(employee.private_signatures.keys()))
    organizations_dropdown_menu.pack()

    Button(revoke_key_frame, text="Revoke Key", width=20, height=1, command=revoke_key).pack()
    
    #revoke_key_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def revoke_key():
    employee = MessagingAppProfile()
    employee.load_profile_from_id(username_verify.get())

    employee.revoke_key(organizations_dropdown.get())

    employee.save_profile()

    assign_success_frame = Toplevel(success_screen)
    assign_success_frame.title("Revoke Key Success")
    assign_success_frame.geometry("400x200")

    Label(assign_success_frame, text="").pack()
    Label(assign_success_frame, text="Successfully revoked key from Organization: ").pack()
    Label(assign_success_frame, text=organizations_dropdown.get()).pack()
    
    #assign_success_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

login() # call the main_account_screen() function
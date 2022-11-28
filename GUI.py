# https://www.simplifiedpython.net/python-gui-login/

from tkinter import *
from dataclass import MasterAccount, MessagingAppProfile

def login():
    global login_screen

    login_screen = Tk()
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details of your Org below to login").pack()
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
    Label(success_screen, text=f"Welcome, org: MockOrg").pack()
    Label(success_screen, text="").pack()

    Button(success_screen, text="View Messaging Profiles with Assigned Keys", width=40, height=1, command=view_known_profiles_frame).pack()
    Button(success_screen, text="Assign a new key to a new Messaging Profile", width=40, height=1, command=assign_new_key_frame).pack()
    Button(success_screen, text="Revoke Key from Messaging Profile", width=40, height=1, command=revoke_key_frame).pack()
    
    success_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.withdraw()

def view_known_profiles_frame():
    known_profiles_screen = Toplevel(success_screen)
    known_profiles_screen.title("Known Messaging App Profiles")
    known_profiles_screen.geometry("400x300")

    master_account = MasterAccount()
    master_account.load_account_from_org_name("MockOrg")
    
    # https://stackoverflow.com/questions/20768405/print-dictionary-in-python-ttk
    header_text = 'IDs of profiles with a key assigned'
    Label(known_profiles_screen, text=header_text).pack()

    text = '\n'.join(f"{k}" for k in master_account.id_key_dict.keys())
    Label(known_profiles_screen, text=text).pack()
    
    #known_profiles_screen.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)


def assign_new_key_frame():
    assign_key_frame = Toplevel(success_screen)
    assign_key_frame.title("Assign Key")
    assign_key_frame.geometry("400x300")

    Label(assign_key_frame, text="").pack()
    Label(assign_key_frame, text="Enter Messaging ID *").pack()

    global assign_message_id
    assign_message_id = StringVar()
    message_id_entry = Entry(assign_key_frame, textvariable=assign_message_id)
    message_id_entry.pack()

    Button(assign_key_frame, text="Assign Key", width=20, height=1, command=assign_key).pack()
    
    #assign_key_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def assign_key():
    master_account = MasterAccount()
    master_account.load_account_from_org_name("MockOrg")

    messaging_profile = MessagingAppProfile()
    messaging_profile.load_profile_from_id(assign_message_id.get())

    master_account.issue_private_key(messaging_profile)

    messaging_profile.save_profile()
    master_account.save_account()

    assign_success_frame = Toplevel(success_screen)
    assign_success_frame.title("Assign Key Success")
    assign_success_frame.geometry("400x200")

    Label(assign_success_frame, text="").pack()
    Label(assign_success_frame, text="Successfully assigned new key to profile with ID: ").pack()
    Label(assign_success_frame, text=assign_message_id.get()).pack()
    
    #assign_success_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def revoke_key_frame():
    revoke_key_frame = Toplevel(success_screen)
    revoke_key_frame.title("Revoke Key")
    revoke_key_frame.geometry("400x300")

    Label(revoke_key_frame, text="").pack()
    Label(revoke_key_frame, text="Enter Messaging ID *").pack()

    global revoke_message_id
    revoke_message_id = StringVar()
    message_id_entry = Entry(revoke_key_frame, textvariable=revoke_message_id)
    message_id_entry.pack()

    Button(revoke_key_frame, text="Revoke Key", width=20, height=1, command=revoke_key).pack()
    
    #revoke_key_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

def revoke_key():
    master_account = MasterAccount()
    master_account.load_account_from_org_name("MockOrg")

    messaging_profile = MessagingAppProfile()
    messaging_profile.load_profile_from_id(revoke_message_id.get())

    master_account.revoke_key(messaging_profile)

    messaging_profile.save_profile()
    master_account.save_account()

    assign_success_frame = Toplevel(success_screen)
    assign_success_frame.title("Revoke Key Success")
    assign_success_frame.geometry("400x200")

    Label(assign_success_frame, text="").pack()
    Label(assign_success_frame, text="Successfully revoked key from profile with ID: ").pack()
    Label(assign_success_frame, text=revoke_message_id.get()).pack()
    
    #assign_success_frame.protocol("WM_DELETE_WINDOW", on_closing)
    login_screen.protocol("WM_DELETE_WINDOW", on_closing)

login() # call the main_account_screen() function
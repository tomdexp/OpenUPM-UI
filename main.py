import tkinter
import customtkinter
from tkinter import filedialog
import os
import subprocess
import installation_process

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("780x640")
app.title("Open Source Unity Package Registry Installer")

current_installation_process = installation_process.InstallationProcess("", "", False)


def button_callback():
    #current_installation_process.apply_defaults()
    #print(current_installation_process)
    current_installation_process.log_test()


def select_folder():
    selected_folder_path = filedialog.askdirectory(title='Select the Parent Directory')
    label_selected_folder.configure(text="Selected folder: " + selected_folder_path)
    print(selected_folder_path)
    current_installation_process.folder_path = selected_folder_path
    verify_if_can_install()


def install_into_folder():
    current_installation_process.CallBackEvents.on_installation_complete += installation_complete
    current_installation_process.CallBackEvents.on_installation_failed += installation_failed
    current_installation_process.CallBackEvents.on_log += add_log
    current_installation_process.install()


def installation_complete():
    print("Installation complete! event callback called.")


def installation_failed():
    print("Installation failed! event callback called.")


def add_log(value):
    textbox_installation_logs.configure(state="normal")
    textbox_installation_logs.insert(tkinter.END, value + "\n")
    textbox_installation_logs.configure(state="disabled")


def parse_package_url():
    value = input_url.get()
    print("Parsing package URL...")
    add_log("Parsing package URL...")
    if value == "":
        print("No package URL specified! Please enter a package URL.")
        add_log("No package URL specified! Please enter a package URL.")
        return
    print("Given URL is : " + value)
    add_log("Given URL is : " + value)
    # with an url like https://openupm.com/packages/com.cysharp.memorypack/#close, just get com.cysharp.memorypack
    try:
        package_name = value.split("/")[4]
    except IndexError:
        print("Invalid URL! Please enter a valid package URL.")
        add_log("Invalid URL! Please enter a valid package URL.")
        return
    print("Package name is : " + package_name)
    add_log("Package name is : " + package_name)
    current_installation_process.package_name = package_name
    verify_if_can_install()


def visit_openupm_website():
    print("Opening OpenUPM website...")
    add_log("Opening OpenUPM website...")
    os.startfile("https://openupm.com/packages/")


def verify_if_can_install():
    if current_installation_process.folder_path == "" or current_installation_process.package_name == "":
        return
    else:
        button_install.configure(state="normal")


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT, text="Enter the URL of the package you want to install:")
label_1.pack(pady=12, padx=50)

input_url = customtkinter.CTkEntry(master=frame_1, placeholder_text="OpenUPM URL Here...", width=500)
input_url.pack(pady=12, padx=50)

button_check_url = customtkinter.CTkButton(master=frame_1, text="Check URL", command=parse_package_url)
button_check_url.pack(pady=12, padx=50)

button_visit_url = customtkinter.CTkButton(master=frame_1, text="OpenUPM Website", command=visit_openupm_website)
button_visit_url.pack(pady=12, padx=50)

#button_debug_print = customtkinter.CTkButton(master=frame_1, text="Debug Print", command=button_callback)
#button_debug_print.pack(pady=12, padx=50)

button_2 = customtkinter.CTkButton(master=frame_1, command=select_folder, text="Select Project Folder")
button_2.pack(pady=12, padx=50)

label_selected_folder = customtkinter.CTkLabel(master=frame_1, justify=tkinter.LEFT, text="Selected Folder: None")
label_selected_folder.pack(pady=12, padx=50)

button_install = customtkinter.CTkButton(master=frame_1, command=install_into_folder, text="Install")
button_install.configure(state="disabled")
button_install.pack(pady=12, padx=50)

textbox_installation_logs = customtkinter.CTkTextbox(app, text_font=("Consolas", 10))
textbox_installation_logs.insert("0.0", "[Logs]\n")
textbox_installation_logs.configure(state="disabled")
textbox_installation_logs.pack(pady=12, padx=12, fill="both", expand=True)
app.mainloop()

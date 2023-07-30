import os
import glob
from tkinter import *
from tkinter import filedialog
import datetime
import numbers
import sys

running = False  # Loop toggle
num = 1  # Renaming index
amt_delayed = 500 # Rename Delay
standard_delay = amt_delayed # User Set Delay
file_path = os.path.join(os.environ['USERPROFILE'], "Downloads\FyshIndexer")
recursion_counter = 0

# Start Loop
def unlock(event):
    global running
    running = True
    directory_setter["state"] = DISABLED

# Stop Loop
def lock(event):
    global running
    running = False
    directory_setter["state"] = NORMAL

# Prevents RecursionError
def reset(self):
    global recursion_counter
    global running
    recursion_counter = 0
    running = False
    print('Pre Break')
    self.after(3000, running, True)
    print('Post Break')
    running = True

# Locate Working Directory
def setdir(event):
    global file_path
    temp = filedialog.askdirectory()
    if len(temp) != 0:
        file_path = temp
        selector["state"] = NORMAL

# Close Window
def exitapp(event):
    print('Exiting')
    root.destroy()

# Delay
def waithere():
    var = IntVar()
    global amt_delayed
    root.after(amt_delayed, var.set, 1)
    print("waiting...")
    root.wait_variable(var)


class DelayedUpdateUI(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master=master, **kw)
        # Call update to begin our recursive loop.
        self.update()


    def update(self):
        global num
        global amt_delayed
        global standard_delay
        global file_path
        global entry_lines
        global recursion_counter

        if entry_lines.get().isdigit() and int(entry_lines.get()) > 500:
            standard_delay = int(entry_lines.get())

        self.after(amt_delayed, self.update)

        if running:
            amt_delayed = standard_delay
            print("Alive " + str(datetime.datetime.now()) + '\n\n')
            os.chdir(file_path)
            files = glob.glob('*')
            recursion_counter +=1
            print(recursion_counter)
            if recursion_counter > 100:
                reset(self)

            for file in files:
                if file.find('_ID_') != -1 or file.find('FyshIndexer') != -1:
                    continue
                else:
                    num += 1
                    orig = file.split('.')
                    newname = orig[0] + '_ID_' + str(num) + '.' + orig[1]
                    os.rename(file, newname)
            waithere()
        else:
            amt_delayed = 1
            print('...')
            print(entry_lines.get())

if __name__ == '__main__':
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    sys.setrecursionlimit(5000)
    # Window Setup
    root = Tk()
    root.title("Title")
    root.title('Fysh Indexer')
    root.geometry('300x100')
    app = Frame(root)
    root.iconbitmap("fysh_logo_ico.ico")

    # Program "Run / Close / Stop" Button
    selector = Button(root, text='Mouse: Unlock | ESC | Lock')
    selector.bind('<Button-1>', unlock)
    selector.bind('<Button-3>', lock)
    selector.bind('<Button-2>', exitapp)
    selector.pack(side=TOP, ipadx=70, ipady=2, expand=TRUE)
    selector["state"] = DISABLED

    # Program Directory Setter
    directory_setter = Button(root, text='Set File Location')
    directory_setter.bind('<Button-1>', setdir)
    directory_setter.bind('<Button-3>', setdir)
    directory_setter.bind('<Button-2>', exitapp)
    directory_setter.pack(side=TOP, ipadx=98, ipady=2, expand=TRUE)

    entry_lines = StringVar()
    delay_val = Entry(root, textvariable=entry_lines)
    delay_val.pack(side=TOP, ipadx=0, ipady=2, expand=TRUE)

    DelayedUpdateUI(root)
    root.mainloop()
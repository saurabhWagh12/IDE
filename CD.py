from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os

compiler = Tk()
compiler.title('My Code Editor')

filepath = ''

def setFilePath(path):
    global filepath
    filepath = path

def run_python():
    command = f'python3 {filepath}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    codeOutput.delete('1.0', END)
    codeOutput.insert('1.0', output.decode("utf-8"))
    codeOutput.insert('1.0', error.decode("utf-8"))

def run_java():
    code = editor.get('1.0', END)
    if filepath == '':
        # Save the Java code to a file (e.g., code.java)
        with open('Main.java', 'w') as java_file:
            java_file.write(code)
        file_name = 'Main.java'
    else:
        # Save the Java code to the existing file
        with open(filepath, 'w') as java_file:
            java_file.write(code)
        file_name = os.path.basename(filepath)

    # Compile and run the Java code using subprocess
    compile_process = subprocess.run(['javac', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(filepath))
    if compile_process.returncode == 0:
        run_process = subprocess.Popen(['java', file_name[:-5]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(filepath))
        output, error = run_process.communicate()
        codeOutput.delete('1.0', END)
        codeOutput.insert('1.0', output.decode("utf-8"))
        codeOutput.insert('1.0', error.decode("utf-8"))
    else:
        codeOutput.delete('1.0', END)
        codeOutput.insert('1.0', compile_process.stderr.decode("utf-8"))



def saveAs():
    if filepath == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py'), ('Java Files', '*.java')])
    else:
        path = filepath
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        setFilePath(path)

def openFile():
    path = askopenfilename(filetypes=[('Python Files', '*.py'), ('Java Files', '*.java')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        setFilePath(path)

menuBar = Menu(compiler)

fileMenu = Menu(menuBar, tearoff=0)
fileMenu.add_command(label='Open', command=openFile)
fileMenu.add_command(label='Save', command=saveAs)
fileMenu.add_command(label='Save As', command=saveAs)
fileMenu.add_command(label='Exit', command=exit)
menuBar.add_cascade(label='File', menu=fileMenu)

runMenu = Menu(menuBar, tearoff=0)
runMenu.add_command(label='Run Python', command=run_python)
runMenu.add_command(label='Run Java', command=run_java)
menuBar.add_cascade(label='Run', menu=runMenu)

compiler.config(menu=menuBar)

editor = Text(compiler)
editor.grid(row=0, column=0, sticky="nsew")  # Use grid and set row/column weights
compiler.grid_rowconfigure(0, weight=1)       # Make row expandable
compiler.grid_columnconfigure(0, weight=1)    # Make column expandable

def on_tab_pressed(event):
    editor.insert(INSERT, "    ")  # Insert four spaces when the Tab key is pressed
    return 'break'  # Prevents the default behavior of the Tab key

# Tab button Updation
editor.bind("<Tab>", on_tab_pressed)

codeOutput = Text(compiler, height=10)
codeOutput.grid(row=1, column=0, sticky="nsew")  # Use grid for codeOutput as well
compiler.grid_rowconfigure(1, weight=1)          # Make row expandable

compiler.mainloop()

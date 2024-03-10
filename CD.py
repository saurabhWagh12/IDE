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

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True, universal_newlines=True)
    output, error = process.communicate()
    update_output(output, error)

def run_python():
    command = f'python3 {filepath}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    output, error = process.communicate()
    update_output(output, error)

def run_java():
    code = editor.get('1.0', END)
    if filepath == '':
        with open('Main.java', 'w') as java_file:
            java_file.write(code)
        file_name = 'Main.java'
    else:
        with open(filepath, 'w') as java_file:
            java_file.write(code)
        file_name = os.path.basename(filepath)

    # Compile and run the Java code using subprocess
    compile_process = subprocess.run(['javac', file_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(filepath))
    if compile_process.returncode == 0:
        run_process = subprocess.Popen(['java', file_name[:-5]], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(filepath), universal_newlines=True)
        output, error = run_process.communicate()
        update_output(output, error)
    else:
        update_output(compile_process.stderr.decode("utf-8"))

def update_output(output, error=""):
    codeOutput.delete('1.0', END)
    codeOutput.insert('1.0', output)
    codeOutput.insert('1.0', error)

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

def run_enter(event):
    command = codeOutput.get("1.0", "end-1c")  
    run_command(command)

def clear_terminal():
    codeOutput.delete('1.0', END)

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
runMenu.add_command(label='Clear Terminal', command=clear_terminal)
menuBar.add_cascade(label='Run', menu=runMenu)

compiler.config(menu=menuBar)

editor = Text(compiler)
editor.grid(row=0, column=0, sticky="nsew")
compiler.grid_rowconfigure(0, weight=1)
compiler.grid_columnconfigure(0, weight=1)

def on_tab_pressed(event):
    editor.insert(INSERT, "    ")
    return 'break'

editor.bind("<Tab>", on_tab_pressed)

codeOutput = Text(compiler, height=8)
codeOutput.grid(row=1, column=0, sticky="nsew")
compiler.grid_rowconfigure(1, weight=1)
codeOutput.bind("<Return>", run_enter)  

compiler.mainloop()

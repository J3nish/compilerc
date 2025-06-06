import tkinter as tk
import subprocess
import threading
import time
import os

def kill_tempcode_exe():
    try:
        # Try to kill tempcode.exe if running
        subprocess.run(['taskkill', '/f', '/im', 'tempcode.exe'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.1)  # Give time for process to terminate
    except Exception:
        pass
    try:
        if os.path.exists('tempcode.exe'):
            os.remove('tempcode.exe')
    except Exception:
        pass

# run section
def run():
    value = text_area.get('1.0', tk.END).strip() # get the text from the text area
    out_area.config(state='normal')  # make the output area editable
    out_area.delete('1.0', tk.END)  # clear the output area before running the code
    input_field.grid_remove()
    input_label.grid_remove()
    kill_tempcode_exe()  # Kill and remove previous exe before compiling
    with open('tempcode.c', 'w') as f:
        f.write(value)

    # compile code
    compile = subprocess.run(['gcc', '-Wall', '-Werror', 'tempcode.c', '-o', 'tempcode.exe'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if compile.returncode!= 0:  # check if the compilation was successful
        out_area.insert('1.0', "Compilation Error:\n" + compile.stderr)  # insert the compilation error into the output area
        out_area.config(state='disabled')  # make the output area non-editable
        return
    # Start interactive execution in a thread
    threading.Thread(target=run_interactive, daemon=True).start()

def run_interactive():
    proc = subprocess.Popen(['tempcode.exe'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True,
                           bufsize=1)
    def read_output():
        prompt = ''
        while True:
            char = proc.stdout.read(1)
            if not char:
                break
            prompt += char
            out_area.config(state='normal')
            out_area.insert('end', char)
            out_area.see('end')
            out_area.config(state='disabled')
            # If a prompt is likely finished (ends with ':' or '?'), enable input
            if char in [':', '?', '\\n'] and 'scanf' in text_area.get('1.0', tk.END):
                input_label.grid(row=2, column=1, sticky='w', padx=5,pady=5)
                input_label.config(width=5)  # Update label to indicate input is expected
                input_field.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
                input_field.config(width=50)  # Set width for input field
                input_field.focus_set()
                # Wait for user input
                user_input = wait_for_input()
                proc.stdin.write(user_input + '\n')
                proc.stdin.flush()
                prompt = ''
        # Read any remaining stderr
        err = proc.stderr.read()
        if err:
            out_area.config(state='normal')
            out_area.insert('end', "\nRuntime Error:\n" + err)
            out_area.config(state='disabled')
    read_output()

def wait_for_input():
    input_ready = threading.Event()
    user_input = {'value': ''}
    def on_enter(event=None):
        user_input['value'] = input_field.get()
        # Display the entered input in the output area to mimic terminal behavior
        out_area.config(state='normal')
        out_area.insert('end', user_input['value'] + '\n')
        out_area.see('end')
        out_area.config(state='disabled')
        input_field.delete(0, tk.END)
        input_field.grid_remove()
        input_label.grid_remove()
        input_ready.set()
    input_field.bind('<Return>', on_enter)
    input_ready.wait()
    return user_input['value']

# root section
root = tk.Tk()
root.title("ParaCode")
root.columnconfigure(0, weight=1) # make the first column expandable
root.columnconfigure(1, weight=1)  # make the second column expandable
root.rowconfigure(0, weight=1) # make the first row expandable
root.iconbitmap("LOGOPARACODE.ico") # set the icon of the window
root.state('zoomed') # set the window to full screen

'''---UI LOGIC---'''
# frame1 section(left frame)
frame1 = tk.Frame(root,bg='black') # create a frame
frame1.grid(row=0, column=0, sticky='nsew') # place the frame in the grid
frame1.columnconfigure(0, weight=1) # make the first column of the frame expandable
frame1.columnconfigure(1, weight=0) # make the second column of the frame non-expandable
frame1.rowconfigure(1, weight=1) # make the first row of the frame expandable
#frame.grid_propagate(False) # prevent the frame from resizing to fit the contents

# header label 1
label = tk.Label(frame1, text="CODE HERE",anchor='w',relief='solid',borderwidth=1) # create a label
label.grid(row=0, column=0,columnspan=2,sticky='nsew',ipadx=4,ipady=9,) # place the label in the grid

# text area section
text_area = tk.Text(frame1, wrap='char', borderwidth=1,relief='solid',highlightthickness=0,font=("Consolas", 12),undo=True) # here the wrap is used to wrap the text in the text area
text_area.grid(row=1, column=0, sticky='nsew') # place the text area in the grid

text_area.bind('<Control-z>', lambda event: text_area.edit_undo())  # bind Ctrl+Z to undo
text_area.bind('<Control-y>', lambda event: text_area.edit_redo()) # bind Ctrl+Y to redo


#adding scrollbar in frame
scrollbar = tk.Scrollbar(frame1, command=text_area.yview) # create a scrollbar
scrollbar.grid(row=1, column=1, sticky='nsew') # place the scrollbar in the grid
text_area.config(yscrollcommand=scrollbar.set) # link the scrollbar to the text area


# run button
run_btn = tk.Button(frame1, text="Run",command=run,relief='raised',padx=9,pady=1,font=('Consolas')) # create a button to run the code
run_btn.grid(row=0,column=0,sticky='e') # place the button in the grid
'''---------------------------------------------------------------------------------------------------------------------'''
'''---------------------------------------------------------------------------------------------------------------------'''

# frame2 section(right frame)
frame2 = tk.Frame(root,bg='black') # create a frame
frame2.grid(row=0, column=1, sticky='nsew') # place the frame in the grid
frame2.columnconfigure(0, weight=1) # make the first column of the frame expandable
frame2.rowconfigure(1, weight=1) # make the first row of the frame expandable
#frame1.grid_propagate(False) # prevent the frame from resizing to fit the contents

label1 = tk.Label(frame2, text="OUTPUT",anchor='w',relief='solid',borderwidth=1) # create a label
label1.grid(row=0, column=1,columnspan=2,sticky='nsew',ipadx=4,ipady=9,) # place the label in the grid

# text area section2
out_area = tk.Text(frame2,borderwidth=1,relief='solid',highlightthickness=0,bg ='light grey') # here the wrap is used to wrap the text in the text area
#out_area.pack(expand=True, fill='both') # place the text area in the grid
out_area.grid(row=1, column=1, sticky='nsew') # place the text area in the grid

# Add input field and label to frame2 (hidden by default)
input_label = tk.Label(frame2, text="Input:", anchor='w')
input_field = tk.Entry(frame2,width=50)
input_field.grid_remove()
input_label.grid_remove()

root.mainloop()
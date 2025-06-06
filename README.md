# Python Desktop Compiler (Tkinter-Based)

This is a lightweight desktop compiler and code editor built using Python and Tkinter. The app allows users to write, compile, and run code directly through a graphical user interface. Initially created for compiling C code, it can be extended to support other languages like Python.

---

## Features

- Code editor with input/output support
- Compile and run code from the GUI
- Accepts runtime input like `scanf` or `input()`
- File management: open and save source code
- Supports plotting match score graphs using `matplotlib` (if Python-based)

---

## Technologies Used

- Python 3.13
- Tkinter for GUI
- subprocess for executing compiled or interpreted code
- matplotlib (optional, for chart generation)
- os, threading (for system tasks and performance)

---

## How to Use

1.Download and install the gcc compiler given in folder and add the gcc compiler to the environment variables ensuring it is accessible in system wherever it is called and used.
2.Download requirements.txt or libraries mentioned in it.
3.In Pycharm after downloading libraries, select interpreter Python 3.13.
4.Use the code and ensure teh above setup is completed.

//run the below mentioned code of c for scanf input.

#include <stdio.h>

int main() {
    int x;
    printf("Enter a number: ");
    fflush(stdout);  // Ensures the prompt prints immediately
    scanf("%d", &x);
    printf("You entered: %d\n", x);
    return 0;
}

### Requirements

Make sure Python 3.13 is installed. Then install the required dependencies.
Make sure gcc is accessible in the environment path.
Use fflush(stdout); in C code to ensure scanf() prompts are shown correctly.

```bash
pip install -r requirements.txt


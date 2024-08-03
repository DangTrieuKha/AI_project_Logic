import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import Program

# Constants
CELL_SIZE = 64

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Wumpus World")
        self.root.geometry("600x600")
    
        self.default_text = "Enter relative path of file..."
        
        # Frame
        self.welcome_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.map_frame = tk.Frame(self.root)

        # Load images
        self.player_image = tk.PhotoImage(file=os.path.join("Image", "agent1.png"))
        self.gold_image = tk.PhotoImage(file=os.path.join("Image", "gold.png"))
        self.wumpus_image = tk.PhotoImage(file=os.path.join("Image", "wumpus.png"))
        self.pit_image = tk.PhotoImage(file=os.path.join("Image", "pit.png"))
        

        self.show_welcome_frame()

        
    
    def draw_grid(self):
        rows = len(self.program.map)
        cols = len(self.program.map[0])
        for i in range(rows):
            for j in range(cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def draw_elements(self):
        self.canvas.delete("element")
        for i, row in enumerate(self.program.map):
            for j, cell in enumerate(row):
                x, y = j * self.cell_size, i * self.cell_size
                if 'A' in cell:
                    self.canvas.create_image(x + self.cell_size // 2, y + self.cell_size // 2, image=self.player_image, anchor=CENTER)
                if 'G' in cell:
                    self.canvas.create_image(x + self.cell_size // 2, y + self.cell_size // 2, image=self.gold_image, anchor=CENTER)
                if 'W' in cell:
                    self.canvas.create_image(x + self.cell_size // 2, y + self.cell_size // 2, image=self.wumpus_image, anchor=CENTER)
                if 'P' in cell:
                    self.canvas.create_image(x + self.cell_size // 2, y + self.cell_size // 2, image=self.pit_image, anchor=CENTER)
                if 'B' in cell:
                    self.canvas.create_text(x + self.cell_size // 2 - self.cell_size // 4, y + self.cell_size // 2 - self.cell_size // 4, text="B", fill="red", font="Arial 14", tags="element")
                if 'S' in cell:
                    self.canvas.create_text(x + self.cell_size // 2 + self.cell_size // 4, y + self.cell_size // 2 - self.cell_size // 4, text="S", fill="green", font="Arial 14", tags="element")
                

    def on_entry_click(self, event):
        if self.entry.get() == self.default_text:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")

    def on_entry_focus_out(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.default_text)
            self.entry.config(fg="gray")
    def enter_input(self):
        self.filename = self.entry.get()
        if self.check_file_exists(self.filename):
            self.default_text = self.filename
            self.program = Program.Program(self.filename)
            self.program = Program.Program(self.default_text)    
            self.show_main_frame()
                
        #self.default_text = self.filename
        else:
            messagebox.showerror("Error", "File not found. Please enter a valid file path.")
        #self.show_main_frame()


    def hidden_all_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()
            
    def show_welcome_frame(self):
        self.hidden_all_frame()
        self.clear_frame(self.welcome_frame)
        self.welcome_frame.pack(expand=True, anchor='center')

        self.label = tk.Label(self.welcome_frame, text="Welcome to the search project", font=("Helvetica", 16), fg="black")
        self.label.pack(pady=(20, 20))

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=80, padx=30, fill='x')

        self.entry_frame = tk.Frame(self.main_frame, bg="white")
        self.entry_frame.pack(pady=(40, 40), fill='x')


        # Tạo entry và đặt nó trong frame con
        self.entry = tk.Entry(self.entry_frame, fg="gray", width=50, justify="left", bg="white", highlightbackground="#2F4F4F")
        self.entry.insert(0, self.default_text)
        self.entry.bind("<FocusIn>", self.on_entry_click)
        self.entry.bind("<FocusOut>", self.on_entry_focus_out)
        self.entry.pack(side='left', padx=(0, 5), fill='x', expand=True)



        # Tạo button Enter và đặt nó trong frame con
        self.button_enter_input = tk.Button(self.entry_frame, text="Enter", command=self.enter_input, bg="#323232", fg="#FAFAFA", width=10, height=1, cursor="hand2")
        self.button_enter_input.pack(side='right')

        # Tạo button Exit và đặt nó dưới frame con
        self.button_exit = tk.Button(self.main_frame, text="Exit", command=root.quit, bg="#323232", fg="#FAFAFA", width=10, height=1, cursor="hand2")
        self.button_exit.pack(pady=(10, 40))

        # Khởi tạo lại path và search_board
        self.paths = None
        self.search_board = None

    def show_main_frame(self):
        self.current_entity_index = 0
        self.hidden_all_frame()
        self.clear_frame(self.main_frame)
        self.main_frame.pack(expand=True, anchor='center')

        self.button_mainframe = tk.Frame(self.main_frame)
        self.button_mainframe.pack(pady=(40, 40))

        # Create 4 buttons and add them to the frame
        self.input_button = tk.Button(self.button_mainframe, text="Show map", command=self.show_map, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        self.input_button.pack(pady=(5, 5))

        # self.result = tk.Button(self.button_mainframe, text="Show path",command= self.show_path_frame, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        # self.result.pack(pady=(5, 5))

        # self.step = tk.Button(self.button_mainframe, text="Step by step", command=self.show_step_by_step, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        # self.step.pack(pady=(5, 5))

        
        self.default_text = "Enter relative path of file..."
        self.exit_main = tk.Button(self.button_mainframe, text="Back", bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2", command=self.show_welcome_frame)
        self.exit_main.pack(pady=(5, 5))
    
    def show_map(self):
        self.hidden_all_frame()
        self.clear_frame(self.map_frame)
        self.map_frame.pack(expand=True, anchor='center')

        rows = len(self.program.map)
        cols = len(self.program.map[0])
        self.cell_size = 20 + 150 / (rows if rows > cols else cols)

        self.canvas = Canvas(self.map_frame, width=cols * self.cell_size, height=rows * self.cell_size, background='white')
        self.canvas.pack(pady=(10, 10))

        self.draw_grid()
        self.draw_elements()

        self.button_frame_input = tk.Frame(self.map_frame)
        self.button_frame_input.pack(pady=(10, 10))
        #self.back = tk.Button(self.button_frame_input, text="Back", command=self.show_main_frame, bg="#323232", fg="#FAFAFA", width=30, height=1, cursor="hand2")
        #self.back.pack(pady=(5, 5))
    
    def check_file_exists(self, filename):
        return os.path.isfile(filename)
    
    def reset_game(self):
        self.player_position = self.program.start
        self.draw_elements()

    
if __name__ == "__main__":
    root = tk.Tk()
    game = App(root)
    root.mainloop()

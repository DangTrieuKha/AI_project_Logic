import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import copy
import pygame
import threading
from Program import Program
from State import State
from Agent_KB import AgentKB
from Agent import Agent

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Wumpus World")
        self.root.geometry("1280x780")
        self.cell_size = 50
    
        try:
            pygame.mixer.init()
            self.sound = pygame.mixer.Sound("Image/scream.mp3")
        except pygame.error as e:
            print(f"Không thể tải âm thanh: {e}")
            return

    
        self.default_input_text = "Enter relative path of file..."
        self.default_text = None
        
        # Frame
        self.welcome_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.map_frame = tk.Frame(self.root)
        self.map_agent_frame = tk.Frame(self.root)
        self.end_frame = tk.Frame(self.root)

        # Load images
        self.player_image_up = tk.PhotoImage(file=os.path.join("Image", "agent_up.png"))
        self.player_image_down = tk.PhotoImage(file=os.path.join("Image", "agent_down.png"))
        self.player_image_left = tk.PhotoImage(file=os.path.join("Image", "agent_left.png"))
        self.player_image_right = tk.PhotoImage(file=os.path.join("Image", "agent_right.png"))
        self.gold_image = tk.PhotoImage(file=os.path.join("Image", "gold.png"))
        self.wumpus_image = tk.PhotoImage(file=os.path.join("Image", "wumpus.png"))
        self.pit_image = tk.PhotoImage(file=os.path.join("Image", "pit.png"))
        self.poison_image = tk.PhotoImage(file=os.path.join("Image", "poison.png"))
        self.healing_poison_image = tk.PhotoImage(file=os.path.join("Image", "healing_poison.png"))
        
        self.agentKB_list = []
        self.path = []

        self.show_welcome_frame()
    
    
    def draw_grid(self, canvas):
        rows = len(self.program.map)
        cols = len(self.program.map[0])
        for i in range(rows):
            for j in range(cols):
                x0, y0 = j * self.cell_size, i * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def update_grid(self, i, j, color, canvas):
        x0, y0 = (i - 1) * self.cell_size, (10 - j) * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")

    
    def draw_element_i(self, i, j, cell, mode, canvas):

        x, y = j * self.cell_size, i * self.cell_size

        tu_list = cell.split()
        n = len(tu_list)
        for i in range(n):
            if n == 1:
                x_s, y_s = x + self.cell_size // 2, y + self.cell_size // 2
            else:
                x_s, y_s = x + self.cell_size // 2 - 10 + i * 20, y + self.cell_size // 2
            if mode == 1 and tu_list[i] == 'A':
                canvas.create_image(x_s, y_s, image=self.player_image_down, anchor=CENTER)
            if tu_list[i] == 'G':
                canvas.create_image(x_s, y_s, image=self.gold_image, anchor=CENTER)
            
            if tu_list[i] == 'W':
                canvas.create_image(x_s, y_s, image=self.wumpus_image, anchor=CENTER) 

            if tu_list[i] == 'S':
                canvas.create_text(x_s, y_s + self.cell_size // 4, text="S", fill="brown", font="Arial 12", tags="element")
            
            if tu_list[i] == 'P':
                canvas.create_image(x_s, y_s, image=self.pit_image, anchor=CENTER)
            if tu_list[i] == 'B':
                canvas.create_text(x_s, y_s, text="B", fill="green", font="Arial 12", tags="element")

            if tu_list[i] == 'H_P':
                canvas.create_image(x_s, y_s, image=self.healing_poison_image, anchor=CENTER)
            if tu_list[i] == 'G_L':
                canvas.create_text(x_s, y_s + self.cell_size // 4, text="G_L", fill="blue", font="Arial 12", tags="element")    
            
            if tu_list[i] == 'P_G':
                canvas.create_image(x_s, y_s, image=self.poison_image, anchor=CENTER)
            if tu_list[i] == 'W_H':
                canvas.create_text(x_s , y_s - self.cell_size // 4, text="W_H", fill="red", font="Arial 12", tags="element")

    def draw_elements(self, canvas):
        canvas.delete("element")
        for i, row in enumerate(self.program.map):
            for j, cell in enumerate(row):
                self.draw_element_i(i, j, cell, 1, canvas=canvas)
        
    
    def draw_agent(self, state, canvas):
        canvas.delete("agent")
        x, y = state.get_position()
        x_m, y_m = (x - 1) * self.cell_size, (10 - y) * self.cell_size
        direction = state.get_direction()

        if direction == 'UP':
            canvas.create_image(x_m + self.cell_size // 2, y_m + self.cell_size // 2, image=self.player_image_up, anchor=CENTER, tags="agent")
        elif direction == 'DOWN':
            canvas.create_image(x_m + self.cell_size // 2, y_m + self.cell_size // 2, image=self.player_image_down, anchor=CENTER, tags="agent")
        elif direction == 'LEFT':
            canvas.create_image(x_m + self.cell_size // 2, y_m + self.cell_size // 2, image=self.player_image_left, anchor=CENTER, tags="agent")
        elif direction == 'RIGHT':
            canvas.create_image(x_m + self.cell_size // 2, y_m + self.cell_size // 2, image=self.player_image_right, anchor=CENTER, tags="agent")
        #canvas.tag_raise("agent")

    def draw_agentKB(self, state, canvas):
        canvas.delete("agentKB")
        x, y = state.get_position()
        # DEBUG
        print(f'({x}, {y}): {self.agent.kb.is_there_stench(x, y)}')

        dx = [-1, 1, 0, 0]
        dy = [0,0,-1,1]
        list_agentKB = []
        list_agentKB.append((x, y))
        for i in range(4):
            x1 = x + dx[i]
            y1 = y + dy[i]
            if x1 >= 1 and x1 <= 10 and y1 >= 1 and y1 <= 10:
                list_agentKB.append((x1, y1))
                if (x1, y1) not in self.agentKB_list:
                    self.agentKB_list.append((x1, y1))

        #for x1, y1 in self.agentKB_list:
        #print((x,y),':' )
        for x1, y1 in list_agentKB:
            x_u, y_u = copy.deepcopy(x1), copy.deepcopy(y1)
            x1 = (x1 - 1) * self.cell_size
            y1 = (10 - y1) * self.cell_size
            check = False
            if self.agent.kb.is_there_pit(x1, y1):
                canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=self.pit_image, anchor=CENTER, tags="agentKB")
                check = True

            if self.agent.kb.is_there_wumpus(x1, y1):
                canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=self.wumpus_image, anchor=CENTER, tags="agentKB")
                check = True

            if self.agent.kb.is_there_poison(x1, y1):
                canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=self.poison_image, anchor=CENTER, tags="agentKB")
                check = True

            if self.agent.kb.is_there_healing(x1, y1):
                canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=self.healing_poison_image, anchor=CENTER, tags="agentKB")
                check = True

            if self.agent.kb.is_there_glow(x1, y1):
                canvas.create_text(x1 + self.cell_size // 2, y1 + self.cell_size // 2, text="G_L", fill="blue", font="Arial 12", tags="agentKB")
                check = True
            
            if self.agent.kb.is_there_stench(x1, y1):
                canvas.create_text(x1 + self.cell_size // 2, y1 + self.cell_size // 2, text="S", fill="red", font="Arial 12", tags="agentKB")
                check = True
            
            if self.agent.kb.is_there_not_pit(x1, y1) and self.agent.kb.is_there_not_wumpus(x1, y1) and self.agent.kb.is_there_not_poison(x1, y1) and self.agent.kb.is_there_not_healing(x1, y1) and self.agent.kb.is_there_not_glow(x1, y1) and self.agent.kb.is_there_not_stench and check == False:
                self.update_grid(x_u, y_u, "blue", canvas=canvas)
            else:
                self.update_grid(x_u, y_u, "white", canvas=canvas)
        x_m, y_m = 10 - y, x - 1
        self.draw_element_i(x_m, y_m, self.program.map[x_m][y_m], 0, self.agentKB_canvas)
            

    def on_entry_click(self, event):
        if self.entry.get() == self.default_input_text:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")

    def on_entry_focus_out(self, event):
        if self.entry.get() == "":
            self.entry.insert(0, self.default_input_text)
            self.entry.config(fg="gray")
    def enter_input(self):
        filename = self.entry.get()
        if self.check_file_exists(filename):
            self.default_text = filename
            self.program = Program(self.default_text)
            self.agent = Agent(self.program.get_env_info, self.program.is_scream)
            self.show_main_frame()
        else:
            messagebox.showerror("Error", "File not found. Please enter a valid file path.")

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

        self.label = tk.Label(self.welcome_frame, text="Welcome to Wumpus World", font=("Helvetica", 16), fg="black")
        self.label.pack(pady=(20, 20))

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=80, padx=30, fill='x')

        self.entry_frame = tk.Frame(self.main_frame, bg="white")
        self.entry_frame.pack(pady=(40, 40), fill='x')

        # Tạo entry và đặt nó trong frame con
        self.entry = tk.Entry(self.entry_frame, fg="gray", width=50, justify="left", bg="white", highlightbackground="#2F4F4F")
        self.entry.insert(0, self.default_input_text)
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
        self.hidden_all_frame()
        self.clear_frame(self.main_frame)
        self.main_frame.pack(expand=True, anchor='center')

        
        self.button_mainframe = tk.Frame(self.main_frame)
        self.button_mainframe.pack(pady=(40, 40))

        # Create 4 buttons and add them to the frame
        self.input_button = tk.Button(self.button_mainframe, text="Show map", command=self.show_map, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        self.input_button.pack(pady=(5, 5))

        self.run_button = tk.Button(self.button_mainframe, text="Run", command=self.show_map_agent, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        self.run_button.pack(pady=(5, 5))

        self.default_input_text = "Enter relative path of file..."
        self.exit_main = tk.Button(self.button_mainframe, text="Back", bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2", command=self.show_welcome_frame)
        self.exit_main.pack(pady=(5, 5))

        # [DEBUG ONLY, COMMENT OR DELETE WHEN DONE] show end game frame through button
        # self.endgame_button = tk.Button(self.button_mainframe, text="End Game", command=self.show_end_frame, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        # self.endgame_button.pack(pady=(5, 5))
    
    def show_map(self):
        self.hidden_all_frame()
        self.clear_frame(self.map_frame)
        self.map_frame.pack(expand=True, anchor='center')

        self.program = Program(self.default_text)
        self.agent = Agent(self.program.get_env_info, self.program.is_scream)


        rows = len(self.program.map)
        cols = len(self.program.map[0])
        
        self.canvas = Canvas(self.map_frame, width=cols * self.cell_size, height=rows * self.cell_size, background='white')
        self.canvas.pack(pady=(10, 10))

        self.draw_grid(canvas=self.canvas)
        self.draw_elements(canvas=self.canvas)

        self.button_frame = tk.Frame(self.map_frame)
        self.button_frame.pack(pady=(10, 10))

        self.back = tk.Button(self.button_frame, text="Back", command=self.show_main_frame, bg="#323232", fg="#FAFAFA", width=30, height=1, cursor="hand2")
        self.back.pack(pady=(5, 5))

    def show_map_agent(self):
        self.hidden_all_frame()
        self.clear_frame(self.map_agent_frame)
        self.map_agent_frame.pack(expand=True, anchor='center')

        self.program = Program(self.default_text)
        self.agent = Agent(self.program.get_env_info, self.program.is_scream)

        rows = len(self.program.map)
        cols = len(self.program.map[0])

        self.map_environment_frame = tk.Frame(self.map_agent_frame)
        self.map_environment_frame.pack(pady=(8, 5), fill='x')

        self.left_label = tk.Label(self.map_environment_frame, text="Environment", font=("Arial", 16))
        self.left_label.pack(side='left', padx=(0, 0), expand=True)

        self.right_label = tk.Label(self.map_environment_frame, text="Knowledge base", font=("Arial", 16))
        self.right_label.pack(side='right', padx=(0, 0), expand=True)
       

        self.score_label = tk.Label(self.map_agent_frame, text=f"Score: {self.program.get_score}", font=("Arial", 14), bg="white")
        self.score_label.pack()
        self.score_label.config(text=f"Score: {self.program.get_score()}")

        self.health_label = tk.Label(self.map_agent_frame, text=f"Health: {self.program.agent_state.get_health}", font=("Arial", 14), bg="white")
        self.health_label.pack()
        self.health_label.config(text=f"Health: {self.program.agent_state.get_health()}")

        self.run_frame = tk.Frame(self.map_agent_frame)
        self.run_frame.pack(pady=(5, 5))
        
        # vẽ map của program
        self.program_canvas = Canvas(self.run_frame, width=cols * self.cell_size, height=rows * self.cell_size, background='white')
        self.program_canvas.pack(side='left', padx=(10, 5), pady=(5, 5))
        self.draw_grid(self.program_canvas)
        self.draw_elements(self.program_canvas)
        # màu = "white" thay vì "green"
        self.update_grid(self.agent.state.get_position()[0], self.agent.state.get_position()[1], "white", self.program_canvas)
        self.draw_agent(self.agent.state, self.program_canvas)

        # vẽ map của KB
        self.agentKB_canvas = Canvas(self.run_frame, width=cols * self.cell_size, height=rows * self.cell_size, background='gray')
        self.agentKB_canvas.pack(side='left', padx=(10, 5), pady=(5, 5))
        self.draw_grid(self.agentKB_canvas)
        # màu = "white" thay vì "green"
        self.update_grid(self.agent.state.get_position()[0], self.agent.state.get_position()[1], "white", self.agentKB_canvas)
        self.draw_agent(self.agent.state, self.agentKB_canvas)
        x, y = self.agent.state.get_position()
        self.path.append((x, y))
        self.agentKB_list.append((x, y))
        self.agentKB_list.append((x, y + 1))
        self.agentKB_list.append((x + 1, y))

        action = self.action()
        self.action_label = tk.Label(self.map_agent_frame, text=f"Action: {action}", font=("Arial", 14), bg="white")
        self.action_label.pack()
        self.score_label.config(text=f"Action: {action}")

        self.button_frame_step_2 = tk.Frame(self.map_agent_frame)
        self.button_frame_step_2.pack(pady=(10, 10))
        self.next_step_button = tk.Button(self.button_frame_step_2, text="Next Step", command=self.next_step, bg="#323232", fg="#FAFAFA", width=30, height=1, cursor="hand2")
        self.next_step_button.pack(side = tk.LEFT ,padx=(0, 3))
        self.auto_run_button = tk.Button(self.button_frame_step_2, text="Auto Run", command=self.auto_run, bg="#323232", fg="#FAFAFA", width=30, height=1, cursor="hand2")
        self.auto_run_button.pack(side = tk.RIGHT, padx=(8, 10))

        self.button_agent_frame = tk.Frame(self.map_agent_frame)
        self.button_agent_frame.pack(pady=(10, 10))

        self.back_run = tk.Button(self.button_agent_frame, text="Back", command=self.back_button_behavior, bg="#323232", fg="#FAFAFA", width=30, height=1, cursor="hand2")
        self.back_run.pack(pady=(5, 5))

    def back_button_behavior(self):
        if self.program.run() == "Finished":
            # nếu chạy self.program.run để lấy trạng thái kết thúc game
            # thì sẽ bị tăng thêm 10đ do CLIMB
            # nên cần trừ đi 10đ
            self.program.update_score(-10) 
            return self.show_end_frame()
        else:
            return self.show_main_frame()

    def show_end_frame(self):
        self.hidden_all_frame()
        self.clear_frame(self.end_frame)
        self.end_frame.pack(expand=True, anchor='center')

        self.end_label = tk.Label(self.end_frame, text="Game Over", font=("Arial", 16), fg="black")
        self.end_label.pack(pady=(10, 10))

        self.score_label = tk.Label(self.end_frame, text=f"Score: {self.program.get_score()}", font=("Arial", 16), fg="black")
        self.score_label.pack(pady=(10, 10))
        self.score_label.config(text=f"Score: {self.program.get_score()}")

        self.back_welcome_frame = tk.Button(self.end_frame, text="Back to Welcome Screen", command=self.show_welcome_frame, bg="#323232", fg="#FAFAFA", width=40, height=2, cursor="hand2")
        self.back_welcome_frame.pack(pady=(10, 10))

    def next_step(self):
        self.agent.run() 
        self.sound_scream()
        x, y = self.agent.state.get_position()
        #self.path.append((x, y))
        rows = len(self.program.map)
        cols = len(self.program.map[0])
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                if (i, j) in self.agentKB_list:
                    self.update_grid(i, j, "gray", self.agentKB_canvas)
        # màu = "white" thay vì "green"
        
        self.update_grid(x, y, "white", self.agentKB_canvas)
        self.update_grid(x, y, "white", self.program_canvas)
        x_m, y_m = 10 - y, x - 1
        
        # update trạng thái của agent trong map của agentKB
        
        self.draw_agentKB(self.agent.state, self.agentKB_canvas)
        self.draw_agent(self.agent.state, self.agentKB_canvas)

        # update trạng thái của agent trong map của program
        self.draw_element_i(x_m, y_m, self.program.map[x_m][y_m], 0, self.program_canvas)
        self.draw_agent(self.agent.state, self.program_canvas)

        self.score_label.config(text=f"Score: {self.program.get_score()}")
        self.health_label.config(text=f"Health: {self.program.agent_state.get_health()}")
        self.action_label.config(text=f"Action: {self.action()}")
        if self.program.run() == "Finished":
            # self.next_step_button.config(state="disabled")
            # self.auto_run_button.config(state="disabled")
            self.show_end_frame()

    def auto_run(self):
        while True:
            # self.auto_run_button.config(state="disabled")
            self.next_step()
            self.root.update()
            self.root.after(500)
            if self.program.run() == "Finished":
                break

    def action(self):
        actions = self.program.agent_state.get_actions()
        for act in actions:
            if actions[act]:
                return act

    def play_sound(self):
        # Phát âm thanh bằng pygame
        self.sound.play()

    def sound_scream(self):
        if self.program.is_scream():
            thread = threading.Thread(target=self.play_sound)
            thread.start()
    
    def check_file_exists(self, filename):
        return os.path.isfile(filename)
    
    def reset_game(self):
        self.player_position = self.program.start
        self.draw_elements()
    
if __name__ == "__main__":
    root = tk.Tk()
    game = App(root)
    root.mainloop()


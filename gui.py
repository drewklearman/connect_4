import tkinter as tk
from tkinter import messagebox


class Connect4GUI:
    def __init__(self, root, ):
        self.root = root
        self.root.title("Connect 4")
        self.canvas = tk.Canvas(self.root, width=7*100, height=6*100, bg="blue")
        self.canvas.pack()
        self.draw_board()
        #self.canvas.bind("<Button-1>", self.handle_click)

    def draw_board(self):
        for row in range(6):
            for col in range(7):
                x1 = col * 100 + 10
                y1 = row * 100 + 10
                x2 = col * 100 + 90
                y2 = row * 100 + 90
                self.canvas.create_oval(x1, y1, x2, y2, fill="white", tags=f"slot_{row}_{col}")

    def handle_click(self, event):
        col = event.x // 100
        row = self.game.find_next_open_row(col)
        if row is not None:
            self.draw_disc(row, col, self.game.current_player)
            if self.game.drop_disc(row, col):
                if self.game.check_win(self.game.current_player):
                    messagebox.showinfo("Connect 4", f"Player {self.game.current_player} wins!")
                    self.game.reset_game()
                    self.canvas.delete("disc")
                    self.draw_board()
                else:
                    self.game.switch_player()

    def draw_disc(self, row, col, player):
        x1 = col * 100 + 10
        y1 = row * 100 + 10
        x2 = col * 100 + 90
        y2 = row * 100 + 90
        color = "red" if player == 1 else "yellow"
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, tags=f"disc_{row}_{col}")
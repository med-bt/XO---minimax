import numpy as np
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivymd.toast import toast

class TicTacToeGame(MDApp):
    def build(self):
        self.title = "Tic Tac Toe"
        self.players = ["X", "O"]  
        self.current_player = self.players[0]  
        self.board = np.full((3, 3), "") 
        self.game_over = False  

        self.main_layout = BoxLayout(orientation='vertical', spacing=10)
        
        self.grid = GridLayout(cols=3)
        self.main_layout.add_widget(self.grid)

        for row in range(3):
            for col in range(3):
                btn = Button(font_size=128, on_release=lambda btn, row=row, col=col: self.make_move(btn, row, col))
                btn.row, btn.col = row, col  
                self.grid.add_widget(btn)
        
        self.restart_btn = Button(text="Restart", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        self.restart_btn.bind(on_release=self.restart_game)
        self.restart_btn.opacity = 0  
        self.main_layout.add_widget(self.restart_btn)

        return self.main_layout

    def make_move(self, btn, row, col):
        if self.game_over or btn.text:  
            return
        
        btn.text = self.current_player
        self.board[row, col] = self.current_player
        if self.check_win(self.current_player):
            toast(f"Player {self.current_player} wins!")
            self.show_restart_button()
        elif self.is_board_full():
            toast("It's a tie!")
            self.show_restart_button()
        else:
            self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
            if self.current_player == "O":  
                self.bot_move()

    def check_win(self, player):
        for i in range(3):
            if all(self.board[i, :] == player):  
                return True
            if all(self.board[:, i] == player):  
                return True
        if all(np.diag(self.board) == player) or all(np.diag(np.fliplr(self.board)) == player):  # Check diagonals
            return True
        return False

    def is_board_full(self):
        return not (self.board == "").any()

    def show_restart_button(self):
        self.game_over = True  
        self.restart_btn.opacity = 1  

    def restart_game(self, instance):
        for btn in self.grid.children:
            btn.text = ""
        self.board.fill("")  
        self.current_player = self.players[0]  
        self.game_over = False  
        self.restart_btn.opacity = 0  

    def minimax(self, minimax_board, depth, is_maximizing):
        if self.check_win(self.players[1]):  
            return 1
        elif self.check_win(self.players[0]):  
            return -1
        elif self.is_board_full(): 
            return 0

        best_score = -float('inf') if is_maximizing else float('inf')
        for row in range(3):
            for col in range(3):
                if minimax_board[row, col] == "":  
                    minimax_board[row, col] = "O" if is_maximizing else "X"
                    score = self.minimax(minimax_board, depth + 1, not is_maximizing)
                    minimax_board[row, col] = ""  
                    best_score = max(score, best_score) if is_maximizing else min(score, best_score)
        return best_score

    def best_move(self):
        best_score = -float('inf')
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if self.board[row, col] == "":  
                    self.board[row, col] = "O"  
                    score = self.minimax(self.board, 0, False)
                    self.board[row, col] = ""  
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        return move

    def bot_move(self):
        row, col = self.best_move()
        if row != -1 and col != -1:
            self.board[row, col] = "O"
            for btn in self.grid.children:
                if btn.row == row and btn.col == col:
                    btn.text = "O"
                    break
            if self.check_win("O"):
                toast("Bot wins!")
                self.show_restart_button()
            elif self.is_board_full():
                toast("It's a tie!")
                self.show_restart_button()
            else:
                self.current_player = "X"  

if __name__ == "__main__":
    TicTacToeGame().run()

import customtkinter as ctk
import random

class OthelloGame:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("オセロゲーム")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        
        # ゲーム状態
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.current_player = 1  # 1: プレイヤー(黒), -1: コンピューター(白)
        self.game_started = False
        self.buttons = []
        self.difficulty = "easy"
        
        # 初期配置
        self.board[3][3] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = -1
        
        self.create_start_screen()
    
    def create_start_screen(self):
        self.clear_screen()
        
        # タイトル
        title = ctk.CTkLabel(self.root, text="オセロゲーム", font=ctk.CTkFont(size=40, weight="bold"))
        title.pack(pady=50)
        
        # 難易度選択
        diff_label = ctk.CTkLabel(self.root, text="難易度を選択:", font=ctk.CTkFont(size=18))
        diff_label.pack(pady=20)
        
        self.difficulty_var = ctk.StringVar(value="easy")
        diff_menu = ctk.CTkOptionMenu(self.root, values=["easy", "hard"], variable=self.difficulty_var)
        diff_menu.pack(pady=10)
        
        # テーマ選択
        theme_label = ctk.CTkLabel(self.root, text="テーマを選択:", font=ctk.CTkFont(size=18))
        theme_label.pack(pady=20)
        
        theme_menu = ctk.CTkOptionMenu(self.root, values=["dark", "light"], command=self.change_theme)
        theme_menu.pack(pady=10)
        
        # スタートボタン
        start_btn = ctk.CTkButton(self.root, text="ゲーム開始", font=ctk.CTkFont(size=20), 
                                 width=200, height=50, command=self.start_game)
        start_btn.pack(pady=40)
    
    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
    
    def start_game(self):
        self.clear_screen()
        self.game_started = True
        self.difficulty = self.difficulty_var.get()
        
        # スコア表示
        score_frame = ctk.CTkFrame(self.root)
        score_frame.pack(pady=20)
        
        self.black_score = ctk.CTkLabel(score_frame, text="● 黒: 2", font=ctk.CTkFont(size=18))
        self.black_score.pack(side="left", padx=30, pady=10)
        
        self.white_score = ctk.CTkLabel(score_frame, text="○ 白: 2", font=ctk.CTkFont(size=18))
        self.white_score.pack(side="right", padx=30, pady=10)
        
        # ターン表示
        self.turn_label = ctk.CTkLabel(self.root, text="あなたの番です", font=ctk.CTkFont(size=16))
        self.turn_label.pack(pady=10)
        
        # ボード
        board_frame = ctk.CTkFrame(self.root, fg_color="#8B4513", corner_radius=10)
        board_frame.pack(pady=20, padx=20)
        
        self.create_board(board_frame)
        
        # リセットボタン
        reset_btn = ctk.CTkButton(self.root, text="リセット", command=self.reset_game)
        reset_btn.pack(pady=20)
        
        self.update_display()
    
    def create_board(self, parent):
        self.buttons = []
        for i in range(8):
            row = []
            for j in range(8):
                btn = ctk.CTkButton(parent, text="", width=50, height=50, 
                                   fg_color="#228B22", hover_color="#32CD32",
                                   border_width=1, border_color="#000000",
                                   command=lambda r=i, c=j: self.make_move(r, c))
                btn.grid(row=i, column=j, padx=0, pady=0)
                row.append(btn)
            self.buttons.append(row)
    
    def update_display(self):
        if not self.game_started:
            return
        
        valid_moves = self.get_valid_moves(self.current_player)
        
        for i in range(8):
            for j in range(8):
                btn = self.buttons[i][j]
                if self.board[i][j] == 1:  # 黒石
                    btn.configure(fg_color="#228B22", text="●", text_color="#000000", 
                                 font=ctk.CTkFont(size=35, weight="bold"))
                elif self.board[i][j] == -1:  # 白石
                    btn.configure(fg_color="#228B22", text="●", text_color="#FFFFFF", 
                                 font=ctk.CTkFont(size=35, weight="bold"))
                elif (i, j) in valid_moves and self.current_player == 1:  # 選択可能
                    btn.configure(fg_color="#228B22", text="○", text_color="#FFD700", 
                                 font=ctk.CTkFont(size=25))
                else:  # 空
                    btn.configure(fg_color="#228B22", text="", text_color="white")
        
        # スコア更新
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)
        
        self.black_score.configure(text=f"● 黒: {black_count}")
        self.white_score.configure(text=f"○ 白: {white_count}")
        
        # ターン表示
        if self.current_player == 1:
            self.turn_label.configure(text="あなたの番です")
        else:
            self.turn_label.configure(text="コンピューターの番です")
    
    def get_valid_moves(self, player):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 0 and self.is_valid_move(i, j, player):
                    valid_moves.append((i, j))
        return valid_moves
    
    def is_valid_move(self, row, col, player):
        if self.board[row][col] != 0:
            return False
        
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in directions:
            if self.check_direction(row, col, dr, dc, player):
                return True
        return False
    
    def check_direction(self, row, col, dr, dc, player):
        r, c = row + dr, col + dc
        found_opponent = False
        
        while 0 <= r < 8 and 0 <= c < 8:
            if self.board[r][c] == 0:
                return False
            elif self.board[r][c] == -player:
                found_opponent = True
            elif self.board[r][c] == player:
                return found_opponent
            r, c = r + dr, c + dc
        
        return False
    
    def make_move(self, row, col):
        if not self.game_started or self.current_player != 1:
            return
        
        if not self.is_valid_move(row, col, self.current_player):
            return
        
        self.place_stone(row, col, self.current_player)
        self.current_player = -1
        self.update_display()
        
        self.root.after(300, self.computer_move)
    
    def place_stone(self, row, col, player):
        self.board[row][col] = player
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in directions:
            if self.check_direction(row, col, dr, dc, player):
                r, c = row + dr, col + dc
                while self.board[r][c] == -player:
                    self.board[r][c] = player
                    r, c = r + dr, c + dc
    
    def computer_move(self):
        if not self.game_started:
            return
        
        valid_moves = self.get_valid_moves(self.current_player)
        
        if valid_moves:
            if self.difficulty == "easy":
                row, col = random.choice(valid_moves)
            else:
                row, col = self.get_best_move(valid_moves)
            
            self.place_stone(row, col, self.current_player)
        
        self.current_player = 1
        self.update_display()
        self.check_game_end()
    
    def get_best_move(self, valid_moves):
        best_move = None
        max_flips = -1
        
        for row, col in valid_moves:
            flips = self.count_flips(row, col, self.current_player)
            if flips > max_flips:
                max_flips = flips
                best_move = (row, col)
        
        return best_move if best_move else random.choice(valid_moves)
    
    def count_flips(self, row, col, player):
        if self.board[row][col] != 0:
            return 0
        
        total_flips = 0
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        
        for dr, dc in directions:
            if self.check_direction(row, col, dr, dc, player):
                r, c = row + dr, col + dc
                while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == -player:
                    total_flips += 1
                    r, c = r + dr, c + dc
        
        return total_flips
    
    def check_game_end(self):
        player_moves = self.get_valid_moves(1)
        computer_moves = self.get_valid_moves(-1)
        
        if not player_moves and not computer_moves:
            self.end_game()
        elif not player_moves:
            self.current_player = -1
            self.root.after(300, self.computer_move)
    
    def end_game(self):
        self.game_started = False
        
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)
        
        if black_count > white_count:
            result = "あなたの勝利！"
        elif white_count > black_count:
            result = "コンピューターの勝利！"
        else:
            result = "引き分け！"
        
        self.show_game_over(result, black_count, white_count)
    
    def show_game_over(self, result, black_count, white_count):
        self.clear_screen()
        
        # 結果表示
        ctk.CTkLabel(self.root, text="ゲーム終了", font=ctk.CTkFont(size=36, weight="bold")).pack(pady=50)
        ctk.CTkLabel(self.root, text=result, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(self.root, text=f"最終スコア\n● 黒: {black_count}\n○ 白: {white_count}", 
                    font=ctk.CTkFont(size=18)).pack(pady=30)
        
        # ボタン
        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=30)
        
        ctk.CTkButton(button_frame, text="もう一度", font=ctk.CTkFont(size=18), 
                     width=150, height=50, command=self.reset_game).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="終了", font=ctk.CTkFont(size=18), 
                     width=150, height=50, command=self.root.quit).pack(side="left", padx=10)
    
    def reset_game(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = -1
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = -1
        self.current_player = 1
        self.game_started = False
        self.create_start_screen()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = OthelloGame()
    game.run()
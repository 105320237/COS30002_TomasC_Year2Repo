import random   

class TicTacToe:
    winning_sets = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]]
    
    def __init__(self):
        self.player_moves = []
        self.ai_moves = []
        self.available_moves = list(range(9))
        self.current_player = self.randomize_first_player()
        self.winner = None

    def randomize_first_player(self):
        return 'human' if random.randint(0, 1) == 0 else 'ai'
    
    def check_winner(self):
        for winning_set in self.winning_sets:
            if all(move in self.player_moves for move in winning_set):
                self.winner = 'human'
                return
            if all(move in self.ai_moves for move in winning_set):
                self.winner = 'ai'
                return
        #tie if no more moves available
        if len(self.available_moves) == 0:
            self.winner = 'tie'
            return 
    
    def display_board(self):
        board = [' ' for _ in range(9)]
        for move in self.player_moves:
            board[move] = 'X'
        for move in self.ai_moves:
            board[move] = 'O'
        print("\n")

        print(f"{board[0]} | {board[1]} | {board[2]}")
        print("---------")
        print(f"{board[3]} | {board[4]} | {board[5]}")
        print("---------")
        print(f"{board[6]} | {board[7]} | {board[8]}")

        print("\n")
    
    def human_move(self):
        while True:
            try:
                move = int(input("Choose your move (0-8): "))
                if move < 0 or move > 8:
                    print("Your move is invalid. Please choose a number between 0 and 8.")
                elif move not in self.available_moves:
                    print("Spot already taken. Please choose another move.")
                else:
                    return move
            except ValueError:
                print("Your move is invalid. Please enter a number between 0 and 8.")
    
    def ai_move(self):
        move = random.choice(self.available_moves)
        return move
    #storing the moves
    def process_input(self):
        if self.current_player =="human":
            return self.human_move()
        else:
            return self.ai_move()
        
    def update_game_state(self, move):
        if self.current_player == "human":
            self.player_moves.append(move)
        else:
            self.ai_moves.append(move)
        self.available_moves.remove(move)
        self.check_winner()

        #now switch player in case the game is not over
        if self.winner is None:
            if self.current_player == "human":
                self.current_player = "ai"
            else:
                self.current_player = "human"
    #displaying the board after each move
    def render (self):
        self.display_board()
        if self.winner is not None:
            print ("Current player :" + self.current_player)
    
    #game loop

if __name__ == "__main__":
    game = TicTacToe()
    while game.winner is None:
        move = game.process_input()
        game.update_game_state(move)
        game.render()

    print("Game over, the winner is: " + game.winner)
    

                


    


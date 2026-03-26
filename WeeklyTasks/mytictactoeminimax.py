import random   

class Gamestate:
    
    def __init__(self, player_moves=None, ai_moves=None, current_player='human'):
        self.player_moves = player_moves or []
        self.ai_moves = ai_moves or []
        self.current_player = current_player

    def get_available_moves(self):
        taken = set(self.player_moves + self.ai_moves)
        return [i for i in range(9) if i not in taken]

    def check_winner(self):
        winning_sets = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]]
            
        for winner_set in winning_sets:
            if all(move in self.player_moves for move in winner_set):
                return 'human'
            if all(move in self.ai_moves for move in winner_set):
                return 'ai'
        #tie if no more moves available
        if len(self.get_available_moves()) == 0:
            return 'tie'
        return None
    
    def apply_move(self, move):
        #creating new states applying moves
        new_state = Gamestate(self.player_moves.copy(), self.ai_moves.copy(), self.current_player)
        if new_state.current_player == 'human':
            new_state.player_moves.append(move)
            new_state.current_player = 'ai'
        else:
            new_state.ai_moves.append(move)
            new_state.current_player = 'human'
        return new_state
    
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

class RandomAi:
    def get_move(self, state):
        available = state.get_available_moves()
        while True:
            move = random.randint(0,8)
        
            if move in available:
                return move
            
class RandomEfficientAi:
    def get_move(self, state):
        available = state.get_available_moves()
        return random.choice(available)
    
class MinimaxAi:
    def minimax(self, state, maximizing):
        winner = state.check_winner()
        if winner == 'ai':
            return 1
        elif winner == 'human':
            return -1
        elif winner == 'tie':
            return 0
        
        if maximizing:
            best = -float('inf')
            for move in state.get_available_moves():
                new_state = state.apply_move(move)
                best = max(best, self.minimax(new_state, False))
            return best
        #ai wants the highest score
        else:
            best = float('inf')
            for move in state.get_available_moves():
                new_state = state.apply_move(move)
                best = min(best, self.minimax(new_state, True))
            return best
        #I want the lower score
        
    def get_move(self, state):
        best_score = -float('inf')
        best_move = None
        for move in state.get_available_moves():
            new_state = state.apply_move(move)
            score = self.minimax(new_state, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

class NodesTicTacToe:
    def __init__(self, ai_choice= 'random'):
        self.state = Gamestate()
        self.ai_choice = ai_choice
        if ai_choice == 'efficient':
            self.ai = RandomEfficientAi()
        elif ai_choice == 'minimax':
            self.ai = MinimaxAi()
        else:
            self.ai = RandomAi()
    
    def playgame(self):
        while self.state.check_winner() is None:
            self.state.display_board()

            if self.state.current_player == 'human':
                move = int(input("Choose your next move (0-8): "))
                while move not in self.state.get_available_moves():
                    print("Choose a valid move")
                    move = int(input("Choose your next move (0-8): "))
            
            else:
                move = self.ai.get_move(self.state)
                print(f"Ai chooses: {move}")

            self.state = self.state.apply_move(move)
        self.state.display_board()
        print (f"Winner is: {self.state.check_winner()}")


if __name__ == "__main__":
    print ("Choose Ai: random, efficient, minimax ")
    choice = input(": ")
    game = NodesTicTacToe(choice)
    game.playgame()

    


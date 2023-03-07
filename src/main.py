class Game:
    def __init__(self) -> None:
        self.size = 19 * 19 # Goban
        self.board = []
        self.capture = []
        self.to_play = "black" # Black always start
        self.status = "begin" # Begin, finished
        # rule player or ia

    def init_board(self):
        self.board = [[0 for col in range(19)] for row in range(19)]
        self.capture = [0, 0]

    def is_winner(self):
        print("Winner is", self.to_play)

    def is_valid_move(self, x, y):
        if x < 0 or x >= 19 or y < 0 or y >= 19 or self.board[y][x] != 0:
            print("Invalid Coord.")
            return 0

    def get_move(self):
        valid = 0
        print("Player", self.to_play)
        while valid == 0:
            move_x, move_y = map(int, input("Coord x & y\n").split()) # Check if valid move
            valid = self.is_valid_move(move_x, move_y)
        self.board[move_y][move_x] = 1 if self.to_play == "black" else 2
        self.to_play = "white" if self.to_play == "black" else "black"

    def print_board(self):
        for row in self.board:
            print(row)

    def play(self):
        while self.status != 'finished':
            self.get_move()
            self.print_board()

def main():
    test = Game()
    test.init_board()
    test.play()

if __name__ == "__main__":
    main()
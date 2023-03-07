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
        #self.board[1][1] = 1; self.board[2][2] = 1;self.board[4][6] = 1; self.board[4][5] = 1 # Test 2_3 violation
        self.print_board()

    def is_winner(self):
        print("Winner is", self.to_play)

    def double_three(self, x, y):
        # First check +2 to see if possible
        player = 1 if self.to_play == "black" else 2
        allied = []
        # Check 2rd circle
        for check_y in range(y - 2, y + 4, 2):
            if check_y < 0 or check_y >= 19:
                continue
            for check_x in range(x - 2, x + 4, 2):
                if check_x < 0 or check_x >= 19 or (check_x == x and check_y == y):
                    continue
                if self.board[check_y][check_x] == player:
                    allied.append([check_y,check_x])

        if len(allied) >= 2:
            count = 0
            # Check 1rd circle
            for e in allied:
                test_y, test_x = int((e[0] + y) / 2), int((e[1] + x) / 2)
                if self.board[test_y][test_x] == player:
                    count += 1
                    if count == 2:
                        return 1
            # Check 3rd circle
            if count == 1:
                for check_y in range(y - 3, y + 6, 3):
                    if check_y < 0 or check_y >= 19:
                        continue
                    for check_x in range(x - 3, x + 6, 3):
                        if check_x < 0 or check_x >= 19 or (check_x == x and check_y == y):
                            continue
                        if self.board[check_y][check_x] == player:
                            count += 1
                            if count == 2:
                                return 1
        return 0

    def is_valid_move(self, x, y):
        if x < 0 or x >= 19 or y < 0 or y >= 19 or self.board[y][x] != 0:
            print("Invalid Coord.")
            return 0
        if self.double_three(x, y):          # 2 Free 3
            print("Double-three violation.")
            return 0

    def get_move(self):
        valid = 0
        print("Player", self.to_play)
        while valid == 0:
            move_y, move_x = map(int, input("Coord y & x\n").split()) # Check if valid move
            valid = self.is_valid_move(move_x, move_y)
        print("Valid")
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
import numpy as np


class Game:
    def __init__(self) -> None:
        self.size = 19 * 19  # Goban
        self.board = []
        # Number of capture by player --> 5 == gg
        self.capture = {"black": 0, "white": 0}
        self.to_play = "black"  # Black always start
        self.status = "begin"  # Begin, finished
        # rule player or ia

    def init_board(self):
        self.board = np.zeros((19, 19), dtype=np.uint8)
        # self.board[0, 1] = 2; self.board[0, 2] = 2; self.board[0, 3] = 1
        # self.board[1, 0] = 2; self.board[2, 0] = 2; self.board[3, 0] = 1

        # self.board[18, 17] = 2; self.board[18, 16] = 2; self.board[18, 15] = 1
        # self.board[17, 18] = 2; self.board[16, 18] = 2; self.board[15, 18] = 1
        self.board[1, 1] = 2;self.board[2, 2] = 2;self.board[0, 0] = 1;self.board[4, 4] = 2;self.board[5, 5] = 2;self.board[6, 6] = 1

        self.board[1, 5] = 2;self.board[2, 4] = 2;self.board[0, 6] = 1;self.board[4, 2] = 2;self.board[5, 1] = 2;self.board[6, 0] = 1

        self.board[3, 0] = 1
        self.board[3, 1] = 2
        self.board[3, 2] = 2
        self.board[3, 4] = 2
        self.board[3, 5] = 2
        self.board[3, 6] = 1

        self.board[0, 3] = 1
        self.board[1, 3] = 2
        self.board[2, 3] = 2
        self.board[4, 3] = 2
        self.board[5, 3] = 2
        self.board[6, 3] = 1

        self.print_board()

    def is_winner(self):
        print("Winner is", self.to_play)

    def create_axes(self, x, y):
        axes = [
            self.board[max(0, y - 3):min(19, y + 4), x],
            self.board[y, max(0, x - 3):min(19, x + 4)]
        ]
        diag = self.board.diagonal(x - y)
        r_x = 18 - x
        reversed_diag = np.fliplr(self.board).diagonal(r_x - y)

        if x - y >= 0:
            axes.append(diag[max(y - 3, 0):min(y + 4, 19)])
            axes.append(reversed_diag[max(y - 3, 0):min(y + 4, 19)])
        else:
            axes.append(diag[max(x - 3, 0):min(x + 4, 19)])
            axes.append(reversed_diag[max(r_x - 3, 0):min(r_x + 4, 19)])
        return axes

    def is_capturing(self, x, y, p, e, axes):
        captured = []
        val_neg = [(-2, 0, -1, 0), (0, -2, 0, -1), (-2, -2, -1, -1), (-2, 2, -1, 1)] # A sortir d'ici pour ne pas repeter la creation d'un truc qui ne va jamais bouger et moi j'aime biene ecrire truc avec un k comme truck
        val_pos =[(1, 0, 2, 0), (0, 1, 0, 2), (1, 1, 2, 2), (1, -1, 2, -2)]

        for c, axe in enumerate(axes):
            axe = "".join(map(str, axe))
            len_axe = len(axe)
            if len_axe < 4:
                continue
            index_capture = [axe.find(f"{p}{e}{e}{p}", 0, 4), axe.find(f"{p}{e}{e}{p}", len_axe - 4, len_axe)]
            if index_capture[0] != -1:
                opponent_coords = [(y + val_neg[c][0], x + val_neg[c][1]), (y + val_neg[c][2], x + val_neg[c][3])]
                captured.extend([tuple(coord) for coord in opponent_coords if coord[0] >= 0 and coord[1] >= 0 and coord[0] < 19 and coord[1] < 19])

            if index_capture[1] != -1:
                opponent_coords = [(y + val_pos[c][0], x + val_pos[c][1]), (y + val_pos[c][2], x + val_pos[c][3])]
                captured.extend([tuple(coord) for coord in opponent_coords if coord[0] >= 0 and coord[1] >= 0 and coord[0] < 19 and coord[1] < 19])
        return captured

    def free_three(self, axe, p):
        if axe.find(f"0{p}{p}{p}0") != -1 or axe.find(f"0{p}0{p}{p}0") != -1 or axe.find(f"0{p}{p}0{p}0") != -1:
            return 1
        if axe.find(f"{p}{p}{p}{p}{p}") != -1:
            return -2
        if axe.find(f"{p}{p}{p}{p}") != -1:
            return -1
        return 0

    def double_three(self, p, axes):
        count = 0

        for axe in axes:
            axe = "".join(map(str, axe))
            c = self.free_three(axe, p)
            if c == -1:
                return False
            if c == -2:
                return False
            count += c
            if count == 2:
                return True
        return False

    def check_move(self, x, y):
        if x < 0 or x >= 19 or y < 0 or y >= 19 or self.board[y, x] != 0:
            print("Invalid Coord.")
            return 0

        p, e = (1, 2) if self.to_play == "black" else (2, 1)
        self.board[y, x] = p
        # for i in range(10000):
        axes = self.create_axes(x, y)
        captured = self.is_capturing(x, y, p, e, axes)
        if captured:
            print("Captured at :", captured)
            for coord in captured:
                self.board[coord] = 0
        else:
            if self.double_three(p, axes):
                print("Double-three violation.")
                self.board[y, x] = 0
                return 0
        return 1

    def get_move(self):
        valid = 0
        print("Player", self.to_play)
        while valid == 0:
            # Check if valid move
            move_y, move_x = map(int, input("Coord y & x\n").split())
            valid = self.check_move(move_x, move_y)
        print("Valid")
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

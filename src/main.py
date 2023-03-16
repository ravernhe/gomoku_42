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
        self.board[1, 1] = 2
        self.board[2, 2] = 2
        self.board[0, 0] = 1
        self.board[4, 4] = 2
        self.board[5, 5] = 2
        self.board[6, 6] = 1

        self.board[1, 5] = 2
        self.board[2, 4] = 2
        self.board[0, 6] = 1
        self.board[4, 2] = 2
        self.board[5, 1] = 2
        self.board[6, 0] = 1

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

    def get_axes(self, x, y):
        pass

    def is_capturing(self, x, y, p, e):
        
        captured = []
        axes = [
            (max(0, x-3), x+1, y, y),
            (x, min(19, x+4), y, y),
            (x, x, max(0, y-3), y+1),
            (x, x, y, min(19, y+4)),
            ]

        for c, axis in enumerate(axes):
            if axis[0] == axis[1]:
                section = self.board[axis[0], axis[2]:axis[3]]
            else:
                section = self.board[axis[0]:axis[1], axis[2]]

            if len(section) == 4 and  np.all(section == [p, e, e, p]):
                if c == 0:
                    opponent_coords = [(y, x-2), (y, x-1)]
                elif c == 1:
                    opponent_coords = [(y, x+1), (y, x+2)]
                elif c == 2:
                    opponent_coords = [(y-2, x), (y-1, x)]
                else:
                    opponent_coords = [(y+1, x), (y+2, x)]
                
                captured.extend([tuple(coord) for coord in opponent_coords])

        sections = []
        diag = self.board.diagonal(x-y)
        r_x = 18 - x
        reversed_diag = np.fliplr(self.board).diagonal(r_x-y)

        if x-y >= 0:
            sections.append(diag[max(y-3, 0):y+1])
            sections.append(diag[y:min(y+4, 19)])
            sections.append(reversed_diag[max(y-3, 0):y+1])
            sections.append(reversed_diag[y:min(y+4, 19)])
        else:
            sections.append(diag[max(x-3, 0):x+1])
            sections.append(diag[x:min(x+4, 19)])
            sections.append(reversed_diag[max(r_x-3, 0):r_x+1])
            sections.append(reversed_diag[r_x:min(r_x+4, 19)])
        
        for c, section in enumerate(sections):
            if len(section) == 4 and np.all(section == [p, e, e, p]):
                if c == 0:
                    opponent_coords = [(y-2, x-2), (y-1, x-1)]
                elif c == 1:
                    opponent_coords = [(y+1, x+1), (y+2, x+2)]
                elif c == 2:
                    opponent_coords = [(y-2, x+2), (y-1, x+1)]
                else:
                    opponent_coords = [(y+1, x-1), (y+2, x-2)]
                
                captured.extend([tuple(coord) for coord in opponent_coords])
        return captured

    def double_three(self, x, y):

        return 0

    def check_move(self, x, y):
        if x < 0 or x >= 19 or y < 0 or y >= 19 or self.board[y, x] != 0:
            print("Invalid Coord.")
            return 0

        p, e = (1, 2) if self.to_play == "black" else (2, 1)
        self.board[y, x] = p
        captured = self.is_capturing(x, y, p, e)
        if captured:
            for coord in captured:
                self.board[coord] = 0
        else:
            if self.double_three(p, e):
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

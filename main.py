import os
import random


class Board:
    def __init__(self) -> None:
        self.cells = [' ']*9
        self.available_cells = list()
        self.set_available_cells()

    def set_cell_value(self, position, value) -> None:
        """Sets a value in board and updates available cells"""
        self.cells[position] = value
        self.set_available_cells()

    def set_available_cells(self) -> None:
        """Updates available cells in board"""
        self.available_cells = list()
        for count, value in enumerate(self.cells):
            self.available_cells.append(count) if value == ' ' else None

    def clear_board(self) -> None:
        """Clear the board"""
        self.cells = [' '] * 9
    
    def __str__(self) -> str:
        """Print board"""
        return f"""   {self.cells[0]} | {self.cells[1]} | {self.cells[2]} 
  -----------
   {self.cells[3]} | {self.cells[4]} | {self.cells[5]} 
  -----------
   {self.cells[6]} | {self.cells[7]} | {self.cells[8]} """


class Player:
    def __init__(self, symbol: str='x') -> None:
        self.player_cells = list()
        self.opponent_cells = list()
        self.symbol = symbol

    def place_mark(self, position, board: Board) -> None:
        board.set_cell_value(position, self.symbol)
        self.player_cells.append(position)
        


class PC_Player(Player):
    def __init__(self, symbol: str='o') -> None:
        super().__init__(symbol=symbol)

    def can_win(self, player: Player, board: Board) -> int:
        winning_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                             [0, 3, 6], [1, 4, 7], [2, 5, 8],
                             [0, 4, 8], [2, 4, 6]]
        player_cells_set = set(player.player_cells)
        for position in winning_positions:
            position_set = set(position)
            positions_intersection = len(player_cells_set.intersection(position_set))
            # Si hay posibilidad de ganar entonces retornamos la posicion
            if positions_intersection == 2:
                winning_cell = (position_set - player_cells_set).pop()
                if (winning_cell in board.available_cells):
                    return winning_cell

        return 10

    def place_mark(self, board: Board, opponent: Player) -> None:
        pc_win = self.can_win(self, board)     # Celda para ganar
        opponent_win = self.can_win(opponent, board)  # Celda del oponente para ganar
        if pc_win != 10:
            mark = pc_win
        elif opponent_win != 10:
            mark = opponent_win
        else:
            mark = random.choice(board.available_cells)

        self.player_cells.append(mark)
        board.set_cell_value(mark, self.symbol)
    

def user_mark(player: Player, board: Board) -> None:
    """User (person) turn"""
    while 1:
        print('Introduzca una casilla de las siguientes: ')
        print(board.available_cells)
        usr_input = int(input())
        if usr_input in board.available_cells:
            player.place_mark(usr_input, board)
            break


def check_game_over(board: Board, turn_counter: int) -> bool:
    winning_positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8],
                       [0, 3, 6], [1, 4, 7], [2, 5, 8],
                       [0, 4, 8], [2, 4, 6]]
    
    for positions in winning_positions:
        symbols = [board.cells[i] for i in positions]
        symbols = set(symbols)
        if len(symbols) == 1 and (' ' not in symbols):
            return True, symbols.pop()
    
    if turn_counter == 9:
        return True, 'Draw'
    else:
        return False, None


if __name__ == '__main__':
    game_over = False
    turn = bool(random.getrandbits(1))  # Turno == 1 significa turno del jugador
    turn_counter = 0
    board = Board()
    player1 = Player()
    player2 = PC_Player()

    while not game_over:
        os.system('clear')  # Limpiar la consola
        print(board)        # Dibujar tablero
        turn_counter += 1
        # Marcar una casilla dependiendo del turno
        if turn:
            user_mark(player1, board)
            turn = not turn
        else:
            player2.place_mark(board=board, opponent=player1)
            turn = not turn
        # Verificar si hay un ganador
        if turn_counter >= 5:
            game_over, winner = check_game_over(board, turn_counter)
    
    os.system('clear')
    print(board)
    if winner != 'Draw':
        print(f'GANADOR {winner}')
    else:
        print('EMPATE')

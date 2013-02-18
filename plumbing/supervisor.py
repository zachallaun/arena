
from server import start, stop, get_move, send_state
from gameplay.tictactoe import TicTacToe
from gameplay.checkers import Checkers

HOST = '127.0.0.1'
PORT = 1060


def build_state(player, board, winner):

    return {
        'player': player,
        'board': board,
        'winner': winner,
        }

def play(sockets, game_class):

    player = 1
    game = game_class()

    while True:
        player_sock = sockets[player]
        state = build_state(player, game.board, 0)
        send_state(player_sock, state)

        move = get_move(player_sock)

        if game.move_legal(move):

            player = 3 - player # Toggle between 1 and 2...
            game.draw_board()
            #game = game.transition(move, player)
            game.transition(move, player)

            result = game.result()
            if result:
                game.draw_board()
                print("Game over!")
                send_state(sockets[1], build_state(1, game.board, result))
                send_state(sockets[2], build_state(2, game.board, result))
                return


def play_wrapper(game_class):
    sockets = start(HOST, PORT)    
    play(sockets, game_class)
    stop(sockets)

if __name__ == "__main__":
    play_wrapper(Checkers)
    #play_wrapper(ConnectFour)


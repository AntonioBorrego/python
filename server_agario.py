# -*- coding: utf-8 -*-

#Definimos el tablero, recurso en competencia
#Pensar en la estructura de datos... es quizás los más interesante
# del problema, la parte de conc/dist parece fácil.

#procesos que atienden a los clientes:
#recibe dato (id, movimiento, tecla)
#accede en EM al tablero y comprueba si come o es comido, actualiza posición
# y devuelve la ventana de tablero.
#envía de vuelta al cliente la ventana de tablero

from multiprocessing.connection import Listener
from multiprocessing import Process
from multiprocessing.connection import AuthenticationError
from multiprocessing import Lock
from multiprocessing import Manager

import time


def clear_client(board, id):
    board.pop(id[1])

def update_board(board, id, m):
    board[id[1]] = (m, board[id[1]][1]+.05,'#1200FF')
    return board.items()

def serve_client(conn, id, board, semaphore):
    delay = .05
    init_position = 250,125
    init_size = 10
    board[id[1]] = (init_position, init_size)
    while True:
        try:
            m = conn.recv()
        except EOFError:
            print('No receive, connection abruptly closed by client')
            break
        print ('received message:', m, 'from', id[1])
        
        semaphore.acquire()
        answer = update_board(board, id, m)
        semaphore.release()

        try:
            conn.send(answer)
        except IOError:
            print ('No send, connection abruptly closed by client')
            break
        time.sleep(delay)

    semaphore.acquire()
    clear_client(board,id)
    semaphore.release()
    conn.close()
    print ('connection', id, 'closed')

if __name__ == '__main__':

    listener = Listener(address=('127.0.0.1', 6000), authkey=b'secret')
    print ('listener starting')
    
    manager = Manager()
    board = manager.dict()
    semaphore = Lock()

    while True:
        print ('accepting conexions')
        try:
            conn = listener.accept()                
            print ('connection accepted from', listener.last_accepted)
            p = Process(target=serve_client, args=(conn, listener.last_accepted, board, semaphore))
            p.start()
        except AuthenticationError:
            print ('Connection refused, incorrect password')

    listener.close()
    print ('end')

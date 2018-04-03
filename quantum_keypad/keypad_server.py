import socket
import sys
import time
from qiskit import QuantumProgram
import numpy as np

mapping = {
    98: '/',
    55: '*',
    74: '-',
    78: '+',
    14: 'Back',
    96: 'Enter',

    83: '.',
    82: '0',
    79: '1',
    80: '2',
    81: '3',
    75: '4',
    76: '5',
    77: '6',
    71: '7',
    72: '8',
    73: '9'
}


def build_qc(qc, grid, qr, cr):
    theta = np.pi / 4

    for i in range(grid.shape[1]):
        tmp = grid[:2, i]

        if 'C ' in tmp:
            if 'X ' not in tmp:
                raise RuntimeError
            else:
                if 'X ' == tmp[0]:
                    qc.cx(qr[1], qr[0])
                else:
                    qc.cx(qr[0], qr[1])
        else:
            for operator in ['X ', 'H ', 'Y ', 'Z ', 'S ', 'S^', 'U1', 'U2', 'U3', 'I ']:
                pos = np.where(tmp == operator)
                if operator not in tmp:
                    continue

                pos = [int(x) for x in pos[0]]

                if operator is 'X ':
                    for j in pos:
                        qc.x(qr[j])
                elif operator is 'H ':
                    for j in pos:
                        qc.h(qr[j])
                elif operator is 'Y ':
                    for j in pos:
                        qc.y(qr[j])
                elif operator is 'Z ':
                    for j in pos:
                        qc.z(qr[j])
                elif operator is 'S ':
                    for j in pos:
                        qc.s(qr[j])
                elif operator is 'S^':
                    for j in pos:
                        qc.sdg(qr[j])
                elif operator is 'U1':
                    for j in pos:
                        qc.u1(theta, qr[j])
                elif operator is 'U2':
                    for j in pos:
                        qc.u2(theta, theta, qr[j])
                elif operator is 'U3':
                    for j in pos:
                        qc.u3(theta, theta, theta, qr[j])

    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])

    return qc


def simulate(grid):
    qp = QuantumProgram()

    qr = qp.create_quantum_register('qr', 2)
    cr = qp.create_classical_register('cr', 2)

    qc = qp.create_circuit('pi', [qr], [cr])
    qc = build_qc(qc, grid, qr, cr)

    result = qp.execute('pi')
    return result.get_counts('pi')


class State:
    def __init__(self):
        self.POS = "__"
        self.EMPTY = "  "
        self.LINE = "--"

        self.position = np.array([0, 0])
        self.width = 10
        self.height = 2
        self.grid = []

        for i in range(self.height * 2):
            if i % 2 == 0:
                self.grid.append([self.LINE] * self.width)
            else:
                self.grid.append([self.EMPTY] * self.width)
        self.grid = np.array(self.grid)

    def up(self):
        self.position[0] -= 2
        if self.position[0] < 0:
            self.position[0] = 0

    def down(self):
        self.position[0] += 2
        if self.position[0] >= self.height:
            self.position[0] = self.height - 1

    def right(self):
        self.position[1] += 1
        if self.position[1] >= self.width:
            self.position[1] = self.width - 1

    def left(self):
        self.position[1] -= 1
        if self.position[1] < 0:
            self.position[1] = 0

    def back(self):
        self.left()
        self.grid[2 * self.position[0] + 1, self.position[1]] = self.EMPTY
        self.grid[2 * self.position[0], self.position[1]] = self.LINE

    def delete(self):
        self.grid[2 * self.position[0] + 1, self.position[1]] = self.EMPTY
        self.grid[2 * self.position[0], self.position[1]] = self.LINE

    def add(self, operation):
        self.grid[2 * self.position[0], self.position[1]] = operation

    def vis(self):
        self.grid[2 * self.position[0] + 1, self.position[1]] = self.POS

        res = ''
        for i, row in enumerate(self.grid):
            if i % 2 == 0:
                res += '|0> '
            else:
                res += '   .'
            res += '.'.join(row)
            res += '.'
            res += '\n'

        self.grid[2 * self.position[0] + 1, self.position[1]] = self.EMPTY
        return res

    def enter(self):
        self.__init__()


s = State()


def do_smt(key, num=False):
    global s

    BLANK = '\n' * 40

    if mapping[key] is '8':
        if num:
            s.up()
        else:
            s.add('Y ')
    elif mapping[key] is '2':
        if num:
            s.down()
        else:
            s.add('U2')
    elif mapping[key] is '6':
        if num:
            s.right()
        else:
            s.add('S^')
    elif mapping[key] is '4':
        if num:
            s.left()
        else:
            s.add('H ')
    elif mapping[key] is '.':
        s.add('I ')
    elif mapping[key] is '0':
        s.add('C ')
    elif mapping[key] is '5':
        s.add('S ')
    elif mapping[key] is '7':
        s.add('X ')
    elif mapping[key] is '9':
        s.add('Z ')
    elif mapping[key] is '*':
        s.add('T ')
    elif mapping[key] is '-':
        s.add('T^')
    elif mapping[key] is '/':
        s.back()
    # elif mapping[key] is 'Back':
    #     s.delete()
    # elif mapping[key] is 'Back':
    #     s.back()
    elif mapping[key] is '+':
        s.delete()
    elif mapping[key] is 'Enter':
        print(BLANK)
        prev_vis = s.vis()
        print(prev_vis)
        print('Simulating...')

        res = simulate(s.grid[::2])
        s.enter()

        print(BLANK)
        print(prev_vis)
        print('Result: ', res)

        return

    print(BLANK)
    print(s.vis())

    return


def find_pattern(actions):
    if len(actions) == 0 or (len(actions) == 1 and actions == [69]):
        return actions
    elif actions[0] == 69:
        if actions[-1] == 69:
            for key in actions[1:-1]:
                do_smt(key, num=True)

            actions = []
        else:
            return actions
    else:
        do_smt(actions[-1])
        actions.pop()

    return actions


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.0.3', 6665)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

connection, client_address = sock.accept()

presses = []
find_pattern(presses)

while True:
    data = connection.recv(16)
    data = data.decode().split()
    for x in data:
        presses.append(int(x))
        presses = find_pattern(presses)

    time.sleep(0.01)
    # print('received {} w {}'.format(int(x), len(data)))


# for event in dev.read_loop():
#     if event.type == ecodes.EV_KEY:
#         if event.value == 1:
#             presses.append(event.code)
#             presses = find_pattern(presses)

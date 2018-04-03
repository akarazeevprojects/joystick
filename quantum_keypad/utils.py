"""
File name: utils.py
Author: Anton Karazeev <anton.karazeev@gmail.com>

This file is part of joystick project (https://github.com/akarazeevprojects/joystick)
"""

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


class State:
    def __init__(self):
        self.POS = "^^"
        self.EMPTY = "  "
        self.LINE = "--"
        self.SEP = " "
        assert len(self.SEP) == 1

        self.position = np.array([0, 0])
        self.width = 7
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
        """

        q[0] |0> --.--.C-.--.--.--.--.--.Mz┐
                .  .  .  .  .  .  .  .  .  |
        q[1] |0> --.--.X-.--.--.--.--.--.--|Mz┐
                .  .  .  .^^.  .  .  .  .  |  |
                                           |  |
        c   0-/----------------------------v--v--
                                           0  1
        """

        self.grid[2 * self.position[0] + 1, self.position[1]] = self.POS

        res = ''
        for i, row in enumerate(self.grid):
            if i % 2 == 0:
                res += 'q[{}]  |0> '.format(i // 2)
            else:
                res += '         ' + self.SEP
            res += self.SEP.join(row)
            res += self.SEP

            if i % 2 == 0:
                res += (self.LINE + '|') * (i // 2)
                res += 'Mz┐'
            else:
                res += (self.EMPTY + '|') * (1 + (i // 2))
            res += '\n'

        # res += (self.EMPTY + self.EMPTY[0]) * self.width
        # res += '            |  |'
        # res += '\n'

        res += 'c.reg. '
        res += '0-/'
        res += (self.LINE + self.LINE[0]) * self.width + self.LINE
        res += 'v--v-'

        res += '\n'
        res += (self.EMPTY + self.EMPTY[0]) * self.width
        res += '            0  1'

        self.grid[2 * self.position[0] + 1, self.position[1]] = self.EMPTY
        return res

    def enter(self):
        self.__init__()


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
            for operator in ['X ', 'Y ', 'Z ',
                             'H ', 'S ', 'S^',
                             'U1', 'U2', 'U3',
                             'I ', 'T ', 'T^']:
                pos = np.where(tmp == operator)
                if operator not in tmp:
                    continue

                pos = [int(x) for x in pos[0]]

                if operator is 'X ':
                    for j in pos:
                        qc.x(qr[j])
                elif operator is 'Y ':
                    for j in pos:
                        qc.y(qr[j])
                elif operator is 'Z ':
                    for j in pos:
                        qc.z(qr[j])

                elif operator is 'H ':
                    for j in pos:
                        qc.h(qr[j])
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

                elif operator is 'I ':
                    for j in pos:
                        qc.iden(qr[j])
                elif operator is 'T ':
                    for j in pos:
                        qc.t(qr[j])
                elif operator is 'T^':
                    for j in pos:
                        qc.tdg(qr[j])

    qc.measure(qr[0], cr[0])
    qc.measure(qr[1], cr[1])

    return qc


def find_pattern(state, actions, blank=True):
    def do_smt(key, num=False):

        BLANK = '\n' * 40

        if key == -1:
            if blank:
                print(BLANK)
            print(state.vis())

            return
        else:
            if key in mapping:
                if mapping[key] is '8':
                    if num:
                        state.up()
                    else:
                        state.add('Y ')
                elif mapping[key] is '2':
                    if num:
                        state.down()
                    else:
                        state.add('U2')
                elif mapping[key] is '6':
                    if num:
                        state.right()
                    else:
                        state.add('S^')
                elif mapping[key] is '4':
                    if num:
                        state.left()
                    else:
                        state.add('H ')
                elif mapping[key] is '1':
                    state.add('U1')
                elif mapping[key] is '3':
                    state.add('U3')
                elif mapping[key] is '.':
                    state.add('I ')
                elif mapping[key] is '0':
                    state.add('C ')
                elif mapping[key] is '5':
                    state.add('S ')
                elif mapping[key] is '7':
                    state.add('X ')
                elif mapping[key] is '9':
                    state.add('Z ')
                elif mapping[key] is '*':
                    state.add('T ')
                elif mapping[key] is '-':
                    state.add('T^')
                elif mapping[key] is '/':
                    state.back()
                # elif mapping[key] is 'Back':
                #     state.measure()
                elif mapping[key] is '+':
                    state.delete()
                elif mapping[key] is 'Enter':
                    if blank:
                        print(BLANK)
                    prev_vis = state.vis()
                    print(prev_vis)
                    print('Simulating...')

                    res = simulate(state.grid[::2])
                    state.enter()

                    if blank:
                        print(BLANK)
                    print(prev_vis)
                    print('Result: ', res)

                    return

                if blank:
                    print(BLANK)
                print(state.vis())
            else:
                print("Key {} is not recognized".format(key))

        return

    # 69 is a code responsible for Num Lock.
    if len(actions) == 0 or (len(actions) == 1 and actions == [69]):
        # Do something.
        do_smt(-1, blank)

        return actions
    elif actions[0] == 69:
        if actions[-1] == 69:
            for key in actions[1:-1]:
                # Do something.
                do_smt(key, num=True)

            actions = []
        else:
            return actions
    else:
        # Do something.
        do_smt(actions[-1], num=False)
        actions.pop()

    return actions


def simulate(grid):
    qp = QuantumProgram()

    qr = qp.create_quantum_register('qr', 2)
    cr = qp.create_classical_register('cr', 2)

    qc = qp.create_circuit('pi', [qr], [cr])

    qc = build_qc(qc, grid, qr, cr)
    result = qp.execute('pi')

    tmp = result.get_counts('pi')
    tmp = dict([(x[0], round(x[1] / 1024, 2)) for x in list(tmp.items())])

    return tmp

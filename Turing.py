#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Tape(object):
    def __init__(self, _list=None, position=0):
        if _list is None:
            self.right_list = []
        else:
            self.right_list = list(_list)
        self.position = int(position)
        self.left_list = []

    def move_right(self):
        self.position += 1

    def move_left(self):
        self.position -= 1

    def _list_pos(self):
        if self.position >= 0:
            return self.right_list, self.position
        return self.left_list, -self.position - 1

    def read(self):
        list_, pos = self._list_pos()
        try:
            return list_[pos]
        except IndexError:
            list_.append(None)
            return None

    def write(self, value):
        list_, pos = self._list_pos()
        try:
            list_[pos] = value
        except IndexError:
            list_.append(value)

    def __str__(self):
        return  ', '.join(str(el) if i != self.position else "[%s]" % str(el)
                for i, el in enumerate(self.left_list + self.right_list))

class Turing(object):
    """A pretty simple and stupid Touring machine implementation"""
    def __init__(self, Q, Gamma, b, Sigma, delta, q0, F):
        assert(b in Gamma)
        assert(q0 in Q)
        assert(Sigma.issubset(Gamma - set((b, ))))
        self.Q = Q
        self.Gamma = Gamma
        self.b = b
        self.Sigma = Sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def evaluate(self, tape, print_before_each_move=False):
        state = self.q0 # q = current state -> initially q0
        while True:
            if print_before_each_move:
                print "%s) %s" % (state, tape)   # DBG
            if state in self.F:     # q in final state?
                break
            symbol = tape.read()
            couple = (state, symbol)
            try:
                state, symbol, movement = self.delta[(state, symbol)]
            except KeyError:        # delta(state, symbol) undefined?
                break
            tape.write(symbol)
            if movement == 'R':
                tape.move_right()
            elif movement == 'L':
                tape.move_left()

    def __str__(self):
        return 'Turing(' + ', '.join(map(str, (self.Q, self.Gamma, self.b,
                self.Sigma, self.delta, self.q0, self.F))) + ')'

if __name__ == '__main__':
    T = Turing(Q=set(['q0', 'q1', 'q2']), Gamma=set(['a', 'b', 'c', 'd', None]),
            b=None, q0='q0', F=set(['q2']), Sigma=set(['a', 'b', 'c']), delta={
                    ('q0', 'a') : ('q0', 'a', 'R'),
                    ('q0', 'b') : ('q0', 'b', 'R'),
                    ('q0', None): ('q1', 'b', 'L'),
                    ('q1', 'b') : ('q0', 'b', 'R'),
                    ('q0', 'c') : ('q2', 'c', 'N')})
    print T
    T.evaluate(Tape(['a', 'b', None, 'c', 'd']), print_before_each_move=True)

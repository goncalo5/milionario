from Tkinter import *
from constantes import *
from logic import *

class Game(object):
    def __init__(self):
        self.i = Tk()
        self.n = 0  # number of the question
        self.A = ''  # Answer

        # money
        self.money = Label(text='Dinheiro: ' + str(MONEY[self.n]))
        self.money.grid(row=0, column=0, columnspan=2)

        # create questions
        self.q = Label(text='')
        self.q.grid(row=1, column=0, columnspan=2)

        self.a = Button(self.i, text='', width=12, command=self.a)
        self.a.grid(row=2, column=0)
        self.b = Button(self.i, text='', width=12, command=self.b)
        self.b.grid(row=2, column=1)
        self.c = Button(self.i, text='', width=12, command=self.c)
        self.c.grid(row=3, column=0)
        self.d = Button(self.i, text='', width=12, command=self.d)
        self.d.grid(row=3, column=1)

        self.update()
        self.i.mainloop()

    def update(self):
        self.money['text'] = 'Dinheiro: ' + str(MONEY[self.n])

        self.q['text'] = Q[self.n]

        self.a['text'] = H[self.n]['A']
        self.b['text'] = H[self.n]['B']
        self.c['text'] = H[self.n]['C']
        self.d['text'] = H[self.n]['D']

    def a(self):
        self.A = 'A'
        self.check()

    def b(self):
        self.A = 'B'
        self.check()

    def c(self):
        self.A = 'C'
        self.check()

    def d(self):
        self.A = 'D'
        self.check()

    def check(self):
        if S[self.n] == self.A:
            self.n += 1
            if self.n == N_QUEST:
                self.clean()
                self.money['text'] = 'Dinheiro: ' + str(MONEY[self.n])
                self.q['text'] = 'ganhaste'
            else:
                self.update()
        else:
            self.q['text'] = 'perdeste'
            self.clean()

    def clean(self):
        self.a.destroy(), self.c.destroy()
        self.b.destroy(), self.d.destroy()

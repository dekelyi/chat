import term

X = term.TERMSIZE[0]


class Positioner(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __call__(self, *args):
        text = ' '.join(args)[:-1]
        print text
        # length = len(text)
        # changed = [length % X, length / X]
        # self.x += changed[0]
        # self.y += changed[1] + 1
        self.y += 1

    def __enter__(self):
        term.save()
        term.position(self.x, self.y)
        return self

    def __exit__(self, *_):
        term.restore()

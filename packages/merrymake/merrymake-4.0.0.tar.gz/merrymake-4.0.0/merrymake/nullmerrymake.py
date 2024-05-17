from merrymake.imerrymake import IMerrymake

class NullMerrymake(IMerrymake):

    def handle(self, action, handler):
        return self

    def initialize(self, f):
        return

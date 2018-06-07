from numpy.random import rand as los

class Tripwire():
    def __init__(self, error):
        self.error = error
    def stumble(self, current_decision):
        height = los()
        if height > self.error:
            return current_decision
        else:
            changed_decision = (current_decision-1)*(-1)
            return changed_decision
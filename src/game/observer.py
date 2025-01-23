class Observer:
    def __init__(self):
        pass
    def onNotify(self, game, event):
        pass



class Publisher():
    def __init__(self):
        self.observers : Observer = []

    def addObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def notify(self, game, event):
        for observer in self.observers:
            observer.onNotify(game, event)
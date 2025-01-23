import pygame

class Timer:
    def __init__(self):
        self.startTime = None
        self.waitTime = None
   
    
    def start(self, timeMiliseconds):
        self.startTime = pygame.time.get_ticks()
        self.waitTime = timeMiliseconds

    
    def isDone(self):
        now = pygame.time.get_ticks()
        if now - self.startTime >= self.waitTime:
            return True
        return False

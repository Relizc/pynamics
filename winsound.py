import pygame
pygame.mixer.init()

SND_ASYNC = 0
SND_LOOP = 1
SND_PURGE = 2

def PlaySound(snd, flags):
    if flags == 2:
        pygame.mixer.stop()
        return
    l = 0
    if flags & 1:
        l = -1
    s = pygame.mixer.Sound(snd)
    s.play(loops=l)
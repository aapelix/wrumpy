import pygame

events: list[pygame.event.Event] = []


def get_events():
    return events


def update_events():
    global events
    events = pygame.event.get()

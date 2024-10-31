# Imports

import pgzero
import pgzrun
import random
from pgzero.actor import Actor
from pgzero.keyboard import keyboard

# Constants

WIDTH = 720
HEIGHT = 480
BG_COLOR = (0, 51, 102)
MAX_ENEMIES = 20

# Garlic (enemy) class
class Enemy(Actor):
    def __init__(self, image, pos, hero):
        super().__init__(image, pos)
        self.hero = hero

    def update(self):
        if self.x < self.hero.x:
            self.x += 1
        elif self.x > self.hero.x:
            self.x -= 1
        if self.y < self.hero.y:
            self.y += 1
        elif self.y > self.hero.y:
            self.y -= 1

# Fighter (hero) class
class Fighter(Actor):
    def update(self):
        if keyboard.left:
            self.x -= 5
            if self.x < 0:
                self.x = 0
        if keyboard.right:
            self.x += 5
            if self.x > WIDTH:
                self.x = WIDTH
        if keyboard.up:
            self.y -= 5
            if self.y < 0:
                self.y = 0
        if keyboard.down:
            self.y += 5
            if self.y > HEIGHT:
                self.y = HEIGHT

# Fighter instance
fighter = Fighter('fighter')
fighter.x = WIDTH / 2
fighter.y = HEIGHT / 2


# Double the enemies each 5 sec
enemies = [Enemy('garlic', (random.randint(0, WIDTH), random.randint(0, HEIGHT)), fighter)]

def double_enemies():
    if len(enemies) < MAX_ENEMIES:
        new_enemies = []
        for _ in range(len(enemies)):
            if len(enemies) + len(new_enemies) >= MAX_ENEMIES:
                break
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                pos = (random.randint(0, WIDTH), 0)
            elif side == 'bottom':
                pos = (random.randint(0, WIDTH), HEIGHT)
            elif side == 'left':
                pos = (0, random.randint(0, HEIGHT))
            elif side == 'right':
                pos = (WIDTH, random.randint(0, HEIGHT))
            new_enemies.append(Enemy('garlic', pos, fighter))
        enemies.extend(new_enemies)

pgzero.clock.schedule_interval(double_enemies, 5.0)

# Update screen frame
def update():
    fighter.update()
    for enemy in enemies:
        enemy.update()

def draw():
    screen.fill(BG_COLOR)
    fighter.draw()
    for enemy in enemies:
        enemy.draw()

pgzrun.go()
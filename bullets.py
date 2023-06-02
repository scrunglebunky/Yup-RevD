#Program by Andrew Church 5/26/23
import pygame

# 5/26/23 - This is the default bullet.
# It is rather similar to the previous version's bullet, but that's because of how simple it is
class Bullet(pygame.sprite.Sprite):
    
    #DEFAULT IMAGE - rendered by pygame draw function
    image = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(image, "black", (5, 5), 5)
    pygame.draw.circle(image, "white", (5, 5), 4)
    screen_rect = pygame.Rect(0, 0, 450, 600)

    count = 0
    max = 2

    def __init__(self,pos:tuple=(0,0),sound:bool=True,speed:int=15):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.center=pos
        self.health = 1
        self.speed=speed
        self.kill_on_spawn = False

        #5/27/2023 - Kill Counter
        # If there are too many of a single bullet on screen, the bullet stops spawning. That's all. 
        Bullet.count += 1
        if Bullet.count > Bullet.max:
            self.kill_on_spawn = True
            return

        

        

    def update(self):
        if self.kill_on_spawn:
            self.kill()

        self.rect.y -= self.speed
        if not self.on_screen() or self.health <= 0: 
            self.kill()

    def on_screen(self) -> bool:
        return Bullet.screen_rect.colliderect(self.rect)

    def on_collide(self,collide_type):
        #5/26/23 - This is usually explained elsewhere
        #collision with enemy types
        if collide_type == 2:
            self.health -= 1

    def kill(self):
        pygame.sprite.Sprite.kill(self)
        Bullet.count -= 1







LOADED = [
    Bullet,
]
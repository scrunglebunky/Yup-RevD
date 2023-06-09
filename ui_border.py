#CODE BY ANDREW CHURCH
import pygame,anim,text,random


#06/22/2023 - UI BAR CLASS
# The UI bar is something used by playstate to display things such as the score, background image, and logo.

class Border():
    
    #06/24/2023 - Adding EMBLEMS, which are just different UI symbols to add
    emblems = [ ]

    #06/25/2023 - items to go with emblems
    # So, there are all of the emblems that show where the score values should go, right?
    # Well this is going to be the same thing but a little more specific.
    # This will be a tuple filled with coordinates
    # Main will then feed in another tuple filled with specific number assets to feed into these positions
    num_coords = ()

    def __init__(self,
        anim_bg:bool = False,
        anim_logo:bool = False,
        UI_art:str = "uibox.png",
        ):

        #06/03/2023 - UI - Making a separate brick to the right with highest graphical priority used as a backgorund for the UI
        self.UI_art = UI_art
        self.UI_rect = pygame.Rect(0,0,pygame.display.dimensions[0],pygame.display.dimensions[1])
        self.UI_img = pygame.Surface(pygame.display.dimensions)
        self.UI_img.blit(pygame.transform.scale(anim.all_loaded_images[self.UI_art],(self.UI_rect[2],self.UI_rect[3])),(0,0))

        #06/22/2023 - Animation booleans / setting spritesheet info
        self.anim_bg:bool = anim_bg
        self.anim_logo:bool = anim_logo
        self.animated = self.anim_bg and self.anim_logo


        #06/30/2023 - filling dynamic image sizes for the emblems
        #06/24/2023 - Adding EMBLEMS, which are just different UI symbols to add
        Border.emblems = [ 
            ( #LOGO EMBLEM
                'logo.png',
                (
                    pygame.display.dimensions[0] - ( pygame.display.dimensions[0] - (pygame.display.play_dimensions_resize[0] + pygame.display.play_pos[0])),
                    pygame.display.dimensions[1]*0.15 - (anim.all_loaded_images['logo.png'].get_height()/2)
                )
                
            ),
            ( #SCORE EMBLEM
                "score.png", 
                (
                    pygame.display.play_dimensions_resize[0] + pygame.display.play_pos[0] + 25,
                    pygame.display.dimensions[1]*0.4
                )
            ),
            ( #DEBUG EMBLEM
                "debug.png", 
                (
                    pygame.display.play_dimensions_resize[0] + pygame.display.play_pos[0] + 25,
                    pygame.display.dimensions[1]*0.53
                )
            ),
            ( #LIVES EMBLEM
                "lives.png", 
                (
                    pygame.display.dimensions[0]*0.016,
                    pygame.display.dimensions[1] - anim.all_loaded_images['lives.png'].get_height() - 10
                )
            ),
            ( #WEAPON EMBLEM
                "weapon.png",
                (
                    pygame.display.dimensions[0] - anim.all_loaded_images['weapon.png'].get_width() - 10,
                    pygame.display.dimensions[1] - anim.all_loaded_images['weapon.png'].get_height() - 10,

                )
            )
        ]

        #06/25/2023 - giving corresponding images for num_coords
        Border.num_coords = (
            (pygame.display.dimensions[0],pygame.display.dimensions[1]*0.4,True), #Score
            (pygame.display.dimensions[0],pygame.display.dimensions[1]*0.53,True), #FPS
            (pygame.display.dimensions[0],pygame.display.dimensions[1]*0.58,True), #clock offset to be 60fps
            (pygame.display.dimensions[0],pygame.display.dimensions[1]*0.63,True), #offset fps 
        )
        

    

    def draw(self,window:pygame.Surface):
        # main graphics
        window.blit(self.UI_img,self.UI_rect)
        for emblem in Border.emblems:
            window.blit(anim.all_loaded_images[emblem[0]],emblem[1])

        
    def draw_specific(self,window:pygame.Surface,lives:int,nums:tuple):
        for i in range(len(nums)):
            text.display_numbers(
                nums[i],
                (
                    Border.num_coords[i][0],
                    Border.num_coords[i][1]
                    ),
                window=window,
                reverse=Border.num_coords[i][2])

        # displaying lives
        self.display_lives(window=window, location = ( 95, Border.emblems[3][1][1], ) , lives = lives)
    

    def display_lives(self,window:pygame.Surface,location:tuple = (0,0),lives:int = 3):
        for i in range(lives):
            window.blit(anim.all_loaded_images["life.png"],(location[0] + i*38,location[1]))

    def update(self):
        if not self.animated: return 

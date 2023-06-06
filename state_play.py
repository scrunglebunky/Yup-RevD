import pygame,os,player,text,random,characters,levels,json,formation,anim,backgrounds
#05/28/2023 - STATE IMPLEMENTATION
# instead of everything being handled in main, states handle every specific thing
# playstate is what handles gameplay, specifically
# therefore, this state holds quite a lot of information!

class State():
    data:dict = None
    sprites:dict = None

    def __init__(self,
                 data:dict,
                 sprites:dict,
                 window:pygame.display,
                 campaign:str = "main_story.order",
                 world:int = 1,
                 level:int = 1,
                 level_in_world:"int" = 1,
                 ):
        self.sprites = sprites
        self.data = data
        self.window = window

        #Player spawn
        self.bar = ( #the field the player is able to move along
            "h", #if the bar is horizontal or vertical.
            450, #x position if vertical, y position if horizontal.
            (20,430), #the limits on both sides for the player to move on, y positions if vertical, x positions if horizontal
            1, #gravity. 
            )
        self.player = player.Player(bar=self.bar,sprite_groups=self.sprites)
        sprites[0].add(self.player); sprites[1].add(self.player)

        #06/01/2023 - Loading in level data
        self.campaign = campaign
        self.world = world
        self.level = level #the total amount of levels passed, usually used for intensities or score
        self.level_in_world = level_in_world #the amount of levels completed in the world currently 
        self.world_data = levels.fetch_level_info(campaign_world = (self.campaign,self.world))
        if self.world_data["dynamic_intensity"]:
            levels.update_intensities(self.level,self.world_data)

        #06/01/2023 - loading the formation
        #the formation handles spawning and management of most characters, but the state manages drawing them to the window and updating them
        self.formation = formation.Formation(
            player = self.player,
            world_data = self.world_data,
            level=self.level,
            data=self.data,
            level_in_world=self.level_in_world, 
            sprites=self.sprites)

        #06/03/2023 - UI - Making a separate brick to the right with highest graphical priority used as a backgorund for the UI
        self.UI_art = "placeholder.bmp"
        self.UI_rect = pygame.Rect(
            pygame.display.play_dimensions[0],
            0,
            (pygame.display.get_window_size()[0]-pygame.display.play_dimensions[0]),
            pygame.display.get_window_size()[1]
            )
        self.UI_img = pygame.Surface(((pygame.display.get_window_size()[0]-pygame.display.play_dimensions[0]),pygame.display.get_window_size()[1] ))
        self.UI_img.blit(
            pygame.transform.scale(anim.all_loaded_images[self.UI_art],(self.UI_rect[2],self.UI_rect[3])),
            (0,0))


        #06/03/2023 - Loading in the background
        self.background = backgrounds.Background(self.world_data['bg'], resize = self.world_data['bg_size'], speed = self.world_data['bg_speed'])


        # TEST - text spawn
        for i in range(0):
            spd=random.randint(-5,5)
            if spd == 0: spd = 1
            txt=text.Text(text=random.choice(["owo","uwu","hewwo","cwinge","howy fuck"]),vertex=(random.randint(0,450),random.randint(0,600)),pos=(random.randint(0,450),random.randint(0,600)),pattern="sine",duration=3600,modifier=random.randint(1,100),modifier2=(random.randint(1,25)/random.randint(1,100)),speed=spd)
            sprites[0].add(txt)

    def update(self):
        #Updating sprites
        self.background.update()
        self.background.draw(self.window)
        self.sprites[0].update()
        self.sprites[0].draw(self.window)
        self.formation.update()
        #UI draw
        self.window.blit(self.UI_img,self.UI_rect)

        #Detecting collision between players and enemies 
        collidelist=pygame.sprite.groupcollide(self.sprites[1],self.sprites[2],False,False)
        for key,value in collidelist.items():
            key.on_collide(2)
            value[0].on_collide(1)

        #06/01/2023 - TEST - drawing positioning for the formation for test purposes
        # self.window.blit(anim.all_loaded_images["placeholder.bmp"],self.formation.pos)
       
    def event_handler(self,event):
        self.player.controls(event)
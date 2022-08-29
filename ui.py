import pygame

class Transition:
    def __init__(self):
        self.objects = self.__dict__
        # get all of the methods and fields of class
    
    def lerp(self, new_position, duration):
        for obj in self.objects.values():
            # loop through all objects
            if type(obj) is pygame.Rect:
                obj.center = pygame.math.Vector2.lerp(pygame.math.Vector2(obj.center), new_position, duration)
                # if the type is rect, then lerp it to designated position

    def place(self, new_position):
        for obj in self.objects.values():
            # loop through all objects
            if type(obj) is pygame.Rect:
                obj.center = new_position
                # if the type is rect, then place it to the position
    
    def opacity_change(self, new_opacity, duration):

        for obj in self.objects.values():
            # loop through all objects
            if type(obj) is pygame.Surface:
                changed_opacity = pygame.math.Vector2.lerp(pygame.math.Vector2(obj.get_alpha(), 0), pygame.math.Vector2(new_opacity, 0), duration)
                obj = obj.set_alpha(changed_opacity.x)
                try:
                    obj.opacity = changed_opacity.x
                except:
                    pass
                # if the type is surface, then lerp the opacity and  change it to the lerped number

class Text(Transition):
    def __init__(self, text, position, color, font_name, font_size, opacity=255, shadow=False, shadow_color= (255, 0, 0), shadow_padding= pygame.math.Vector2(2, 2), shadow_opacity = 255):
        Transition.__init__(self)
        
        self.font_size = font_size
        self.font = pygame.font.Font(font_name, self.font_size)
        # define font and font size

        self.font_color = color
        self.text = self.font.render(text, True, self.font_color)
        self.opacity = opacity
        self.text.set_alpha(self.opacity)
        # define text to render and text opacity and color

        self.shadow_text = None
        self.shadow_padding = None
        self.shadow_color = None
        self.shadow_opacity = None

        if shadow is True:
            self.shadow_color = shadow_color
            self.shadow_text = self.font.render(text, True, self.shadow_color)
            self.shadow_padding = shadow_padding
            self.shadow_opacity = shadow_opacity
            self.shadow_text.set_alpha(self.shadow_opacity)
        
        # if shadow is not True, then add shadow components, otherwise, don't

        self.save_position = position
        # save the start position of the UI

        self.rect = self.text.get_rect()
        self.rect.center = self.save_position
        # set the rect's center to the save position
    
    def draw(self, display):
        if self.shadow_text != None:
            display.blit(self.shadow_text, self.rect.topleft + self.shadow_padding)
        # draw the shadow

        display.blit(self.text, self.rect.topleft)
        # draw the text at the rect position
    
    def update_text(self, new_text):
        self.text = self.font.render(new_text, True, self.font_color)
        self.text.set_alpha(self.opacity)
        # change text and change text opacity

        if self.shadow_text is not None:
            self.shadow_text = self.font.render(new_text, True, self.shadow_color)
        # change shadow text if it exists

        self.rect = self.text.get_rect()
        self.rect.center = self.save_position
        # create a new rect

import pygame

class SpriteSheet():
    def __init__(self, image, frame_size, transparent_color):
        self.sheet = image
        self.size = frame_size
        self.colorkey = transparent_color
    
    def get_image(self, frame, scale, state=0, right=True):
        image = pygame.Surface((self.size, self.size)).convert_alpha()
        image.blit(self.sheet, (0, 0), area=(frame*self.size, state*self.size, self.size, self.size))
        image = pygame.transform.scale_by(image, scale)
        if not right:
            image = pygame.transform.flip(image, True, False)
        image.set_colorkey(self.colorkey)
        return image
    
class SpriteState():
    def __init__(self, frame_count, start_idx):
        self.count = frame_count
        self.idx = start_idx
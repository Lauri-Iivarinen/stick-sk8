import pygame

# WHOLE CLASS IS OBSOLETE

class Dude:
    screen, x, y = None, None, None
    WIDTH = 5
    jump_speed = 3
    def __init__(self, _screen, _x, _y, _jump_speed) -> None:
        self.screen = _screen
        self.x = _x
        self.y = _y
        self.jump_speed = _jump_speed
    
    def draw(self):
        # head
        pygame.draw.circle(self.screen, "black", (self.x, self.y), 30, width=self.WIDTH)
        waist = self.y + 120
        pygame.draw.line(self.screen, "black", (self.x, self.y+25), (self.x, waist), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, waist), (self.x+40, self.y + 207), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, waist), (self.x-40, self.y + 207), width=self.WIDTH)
    
    START_JUMP = 14
    current_pop_frame = 0
    pop_asc = False
    pop_desc = False
    pop_height = 0
    right_leg = 0
    def pop(self):
        self.current_pop_frame += 1
        # w8 14 frames before rising
        if self.current_pop_frame > self.START_JUMP and not self.pop_asc and not self.pop_desc:
            self.pop_asc = True
            self.current_pop_frame = 0
        elif self.pop_asc:
            self.right_leg -= 0.75
            self.y -= self.jump_speed
            self.pop_height -= self.jump_speed
            if self.current_pop_frame > self.START_JUMP * 2:
                self.pop_asc = False
                self.pop_desc = True
        elif self.pop_desc:
            self.right_leg += 0.75
            self.y += self.jump_speed * 1.5
            self.pop_height += self.jump_speed * 1.5
        
        if self.pop_desc and self.pop_height >= 0:
            self.current_pop_frame = 0
            self.pop_asc = False
            self.pop_desc = False
            self.pop_height = 0
            self.right_leg = 0
            return True

        pygame.draw.circle(self.screen, "black", (self.x, self.y), 30, width=self.WIDTH)
        waist = self.y + 120
        pygame.draw.line(self.screen, "black", (self.x, self.y+25), (self.x, waist), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, waist), (self.x+40 - self.right_leg*1.5, self.y + 207 + self.right_leg * 1.1), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, waist), (self.x-40, self.y + 207), width=self.WIDTH)
        return False

    def roll_to_view(self):
        # 335 stopping monent
        self.draw()
        self.x += 10
        if self.x >= 335:
            return True
        return False

    def infinite_dude(self):
        self.draw()
        return False
    
    idle_cap = 0
    idle_curr = 0
    def idle(self):
        self.draw()
        self.idle_curr += 1
        if self.idle_curr >= self.idle_cap:
            self.idle_curr = 0
            return True
        return False
    
    def idle_2(self):
        self.idle_cap = 2
        return self.idle()

    def idle_5(self):
        self.idle_cap = 5
        return self.idle()

    def idle_10(self):
        self.idle_cap = 10
        return self.idle()
    
    def idle_15(self):
        self.idle_cap = 15
        return self.idle()
    
    def idle_20(self):
        self.idle_cap = 20
        return self.idle()
    
    def idle_30(self):
        self.idle_cap = 30
        return self.idle()
    
    def idle_40(self):
        self.idle_cap = 40
        return self.idle()
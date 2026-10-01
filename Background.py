import pygame

class Background:
    screen, x, y = None, None, None
    
    def __init__(self, _screen, _x, _y) -> None:
        self.screen = _screen
        self.x = _x
        self.y = _y
    
    def draw_floor(self):
        pygame.draw.line(self.screen, "black", (self.x, self.y), (self.x + 1002, self.y), width=5)
    
    def start_floor(self):
        self.x -= 10
        self.draw_floor()
        return self.x <= 0
    
    phase1_x, phase1_speed, phase1_size, phase_1_duration = 1000, 7, 50, 1410
    def phase1(self):
        self.phase1_x -= self.phase1_speed
        self.draw_floor()
        pygame.draw.rect(self.screen, "black", (self.phase1_x, self.y - self.phase1_size, self.phase1_size, self.phase1_size), 3)
        pygame.draw.rect(self.screen, "black", (self.phase1_x + 550, self.y - self.phase1_size, self.phase1_size, self.phase1_size), 3)
        if self.phase1_x <= self.phase_1_duration * -1:
            self.phase1_x = 1000
            return True
        return False
    
    idle_cap = 0
    idle_curr = 0
    def idle(self):
        self.draw_floor()
        self.idle_curr += 1
        if self.idle_curr >= self.idle_cap:
            self.idle_curr = 0
            return True
        return False
    
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
    
    def infinite_floor(self):
        self.draw_floor()
        return False
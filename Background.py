import pygame

CLOUD_SPEED = 2
SCREEN_WIDTH = 1200
class Background:
    screen, x, y, overlay = None, None, None, None
    
    def __init__(self, _screen, _x, _y, _bg) -> None:
        self.screen = _screen
        self.x = _x
        self.y = _y
        self.overlay = _bg

    def fade(self):
        WDTH = 1
        PAD = 150
        #pygame.draw.rect(self.overlay, pygame.Color(255,255,255,150), (0,0,100,900), 0)
        for i in range(PAD,-1,-1):
            pygame.draw.line(self.overlay, pygame.Color(255,255,255, (255/PAD) * (PAD - i)), (i,-10), (i,1000) , 1)
            pygame.draw.line(self.overlay, pygame.Color(255,255,255, (255/PAD) * (PAD - i)), (SCREEN_WIDTH - i,-10), (SCREEN_WIDTH - i,1000) , 1)


    def cloud_1(self, x, y, col = "black", w = 30):
        # BORDER
        pygame.draw.circle(self.screen, col, (x,y), w, 30)
        pygame.draw.circle(self.screen, col, (x+35,y+20), w, 30)
        pygame.draw.circle(self.screen, col, (x-20,y+15), w, 30)
        pygame.draw.circle(self.screen, col, (x + 10,y + 35), w, 30)
        pygame.draw.circle(self.screen, col, (x + 45, y + 45), w, 30)
        if col == "black":
            self.cloud_1(x,y,"white",28) # FILL

    clouds = [[1200,1400,0,cloud_1],[1200,1200,100,cloud_1], [1200,500,150,cloud_1], [1200,800,0,cloud_1]]
    def draw_cloud(self):
        for i in range(len(self.clouds)):
            cloud = self.clouds[i]
            cloud[1] -= CLOUD_SPEED
            cloud[3](self, cloud[1], cloud[2])
            if cloud[1] <= -100:
                cloud[1] = cloud[0]
            self.clouds[i] = cloud
    
    def draw_floor(self):
        pygame.draw.line(self.screen, "black", (self.x, self.y), (self.x + 1402, self.y), width=5)
    
    def start_floor(self):
        self.x -= 20
        self.draw_floor()
        return self.x <= 0
    
    phase1_x, phase1_speed, phase1_size, phase_1_duration = 1000, 20, 50, 2410
    def phase1(self):
        self.phase1_x -= self.phase1_speed
        self.draw_floor()
        pygame.draw.rect(self.screen, "black", (self.phase1_x, self.y - self.phase1_size, self.phase1_size, self.phase1_size), 3)
        pygame.draw.rect(self.screen, "black", (self.phase1_x + 1950, self.y - self.phase1_size, self.phase1_size, self.phase1_size), 3)
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
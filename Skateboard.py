import pygame
import math

# width 170
LENGTH = 170
DUDE_POINT = 75
TORSO_HEIGHT = 150
NECK_HEIGHT = 30
LEG_HEIGHT = 125
TAIL_WIDTH = 30
TAIL_ANGLE = 25
TIRE_ANGLE = 23
TIRE_GAP = 33

class Skateboard:
    screen, x, y, flat_y = None, None, None, None
    WIDTH = 5
    jump_speed = 3
    
    def __init__(self, _screen, _x, _y, _js) -> None:
        self.screen = _screen
        self.x = _x
        self.y = _y
        self.jump_speed = _js
        self.flat_y = _y
    
    def calc_x_y_raw(self, angle, length):
        # sin(alpha) = a / c
        # a = sin(alpha) * c
        x = math.sin(math.radians(90-angle)) * length
        y = math.sqrt(length ** 2 - x ** 2)
        return x, y
    
    def calc_x_y(self, angle, length):
        x,y = self.calc_x_y_raw(angle, length)
        if x < 0:
            x *= -1
        if y < 0:
            y *= -1
        return x, y

    
    def draw(self):
        # tail/nose x and y diff
        tnx,tny = self.calc_x_y(TAIL_ANGLE, TAIL_WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, self.y), (self.x + LENGTH, self.y), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x + LENGTH, self.y), (self.x + LENGTH + tnx, self.y - tny), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, self.y), (self.x - tnx, self.y - tny), width=self.WIDTH)
        # TIRES
        ltx, lty = self.calc_x_y(TIRE_ANGLE, TIRE_GAP)
        pygame.draw.circle(self.screen, "black", (self.x + ltx, self.y + lty),10,3)
        pygame.draw.circle(self.screen, "black", (self.x + LENGTH - ltx, self.y + lty),10,3)

        # DUDE
        # TORSO
        tox,toy = self.x + DUDE_POINT, self.y - LEG_HEIGHT
        pygame.draw.line(self.screen, "black", (tox, toy), (tox, toy - TORSO_HEIGHT), 2)
        pygame.draw.circle(self.screen, "black", (tox, toy - TORSO_HEIGHT - 30), 30, 2)
        # LLEG, anchor to x,y
        pygame.draw.line(self.screen, "black", (tox, toy), ((self.x, self.y)), 2)
        # RLEG
        rlx, rly = self.calc_x_y(50 ,LEG_HEIGHT/2)
        pygame.draw.line(self.screen, "black", (tox, toy), ((tox + rlx, toy + rly)), 2)
        stance_w = 130
        pygame.draw.line(self.screen, "black", (self.x + stance_w, self.y), ((tox + rlx, toy + rly)), 2)
        

    
    def draw_ollie_nose(self, angle, length):
        x, y = self.calc_x_y(angle, length)
        nx,ny = self.calc_x_y(TAIL_ANGLE + angle, TAIL_WIDTH)
        tx,ty = self.calc_x_y(angle - TAIL_ANGLE, TAIL_WIDTH)
        ltx, lty = self.calc_x_y(angle - TIRE_ANGLE, TIRE_GAP)

        if angle >= TAIL_ANGLE:
            ty *= -1

        # deck
        pygame.draw.line(self.screen, "black", (self.x, self.y), (self.x + x, self.y - y), width=self.WIDTH)
        # nose/tail
        pygame.draw.line(self.screen, "black", (self.x + x, self.y - y), (self.x + x + nx, self.y - y - ny), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x, self.y), (self.x - tx, self.y - ty), width=self.WIDTH)
        # tires, calc left tire and then just apply the standard angle to another tire
        if angle >= TIRE_ANGLE:
            lty *= -1
        pygame.draw.circle(self.screen, "black", (self.x + ltx, self.y + lty),10,3)
        tire_gap,_ = self.calc_x_y(TIRE_ANGLE, TIRE_GAP)
        rtx, rty = self.calc_x_y(angle, LENGTH - tire_gap * 2)
        pygame.draw.circle(self.screen, "black", (self.x + ltx + rtx, self.y + lty - rty),10,3)

        # TORSO
        tox, toy = self.calc_x_y(angle, DUDE_POINT)
        pygame.draw.line(self.screen, "black", (self.x+tox, self.y - toy - LEG_HEIGHT), (self.x+tox, self.y - toy - TORSO_HEIGHT - LEG_HEIGHT), 2)
        pygame.draw.circle(self.screen, "black", (self.x + tox, self.y - toy - TORSO_HEIGHT - LEG_HEIGHT - 30), 30, 2)
        tox = self.x + tox
        toy = self.y - toy - LEG_HEIGHT
        #LLEG
        pygame.draw.line(self.screen, "black", (tox, toy), ((self.x, self.y)), 2)
        #RLEG
        rlx, rly = self.calc_x_y(50 - angle, LEG_HEIGHT/2)
        pygame.draw.line(self.screen, "black", (tox, toy), (tox + rlx, toy + rly), 2)
        stance_w = 130
        rsx,rsy = self.calc_x_y(angle,stance_w)
        pygame.draw.line(self.screen, "black", (self.x + rsx, self.y - rsy), (tox + rlx, toy + rly), 2)


    # As we are lifting tail we need to draw the deck inverted
    def draw_ollie_tail(self, angle, length, lift_angle):
        a_x, a_y = self.calc_x_y(angle, length)
        b_x, b_y = self.calc_x_y(lift_angle, length)
        nx,ny = self.calc_x_y(angle - TAIL_ANGLE, TAIL_WIDTH)
        tx,ty = self.calc_x_y(TAIL_ANGLE + angle, TAIL_WIDTH)
        rtx, rty = self.calc_x_y(angle - TIRE_ANGLE, TIRE_GAP)
        
        if angle >= TAIL_ANGLE * -1:
            ty *= -1

        #print(a_y - b_y)
        ogx, ogy = self.x + b_x - a_x, self.y - (b_y - a_y)
        pygame.draw.line(self.screen, "black", (self.x + b_x, self.y - b_y), (ogx, ogy), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x + b_x, self.y - b_y), (self.x + b_x + nx, self.y - b_y - ny), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x + b_x - a_x, self.y - (b_y - a_y)), (self.x + b_x - a_x - tx, self.y - (b_y - a_y) + ty), width=self.WIDTH)
        
        # tires, calc right tire and then just apply the standard angle to another tire
        pygame.draw.circle(self.screen, "black", (self.x + b_x - rtx, self.y - b_y + rty),10,3)
        tire_gap,_ = self.calc_x_y(TIRE_ANGLE, TIRE_GAP)
        ltx, lty = self.calc_x_y(angle, LENGTH - tire_gap * 2)
        pygame.draw.circle(self.screen, "black", (self.x + b_x - rtx - ltx, self.y - b_y + rty + lty),10,3)

        # TORSO
        tox, toy = self.calc_x_y(angle, LENGTH - DUDE_POINT)
        tox = self.x + b_x - tox
        toy = self.y - b_y + toy - LEG_HEIGHT
        pygame.draw.line(self.screen, "black", (tox, toy), (tox, toy - TORSO_HEIGHT), 2)
        pygame.draw.circle(self.screen, "black", (tox, toy - TORSO_HEIGHT - 30), 30, 2)
        pygame.draw.line(self.screen, "black", (tox, toy), (ogx, ogy), 2)
        rlx, rly = self.calc_x_y(50 + angle, LEG_HEIGHT/2)
        pygame.draw.line(self.screen, "black", (tox, toy), (tox + rlx, toy + rly), 2)
        stance_w = 130
        rsx,rsy = self.calc_x_y(angle, stance_w)
        pygame.draw.line(self.screen, "black", (ogx + rsx, ogy - rsy), (tox + rlx, toy + rly), 2)

    
    rising_angle = 0
    r_asc = True
    r_desc = False
    falling_distance = 0
    travel_distance = 0
    rotate_compensation = 0
    def ollie_2(self):
        LIFT_SPEED = 5
        LIFT_ANGLE = 45
        FALL_SPEED = 7
        NOSE_SPEED = 7 # 6
        TAIL_SPEED = 5 # 5
        X_SPEED = 1.5
        COMPENSATION = 4 # 4
        
        if self.r_asc:
            self.rising_angle += NOSE_SPEED
            self.draw_ollie_nose(self.rising_angle, LENGTH)
            self.travel_distance += X_SPEED / 2
            self.x += X_SPEED / 2
            if self.rising_angle >= TAIL_ANGLE:
                self.y -= COMPENSATION
                self.falling_distance += COMPENSATION
            else:
                self.y += COMPENSATION
                self.falling_distance -= COMPENSATION
                
        elif not self.r_desc:
            self.rising_angle -= TAIL_SPEED
            self.travel_distance += X_SPEED
            self.y -= LIFT_SPEED
            self.falling_distance += LIFT_SPEED
            self.x += X_SPEED
            self.draw_ollie_tail(self.rising_angle * -1, LENGTH, LIFT_ANGLE)
        else:
            #print(self.falling_distance)
            self.falling_distance -= FALL_SPEED if self.falling_distance != 0 else 0
            self.y += FALL_SPEED
            if self.y > self.flat_y:
                self.y = self.flat_y

            self.travel_distance -= X_SPEED / 5
            self.x -= X_SPEED / 5

            self.draw()
            if self.falling_distance <= 0 and self.travel_distance <= 0:
                self.x += self.travel_distance # Reset x axis location to start
                self.rising_angle = 0
                self.r_asc = True
                self.r_desc = False
                self.falling_distance = 0
                self.travel_distance = 0
                return True

        if self.rising_angle >= LIFT_ANGLE:
            self.r_asc = False
        elif self.rising_angle <= 0 and not self.r_desc:
            self.r_desc = True
            _,y = self.calc_x_y(LIFT_ANGLE, LENGTH)
            self.falling_distance += y
            self.y -= y
            self.x -= X_SPEED
            #print("fall dist: ", y, " y now: ", self.y)

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
    
    def infinite_board(self):
        self.draw()
        return False

    ROLL_LENGTH = 60
    roll_current = 0
    def roll_to_view(self) -> bool:
        if self.x < 370:
            self.x += 20
        else:
            self.roll_current += 1
        self.draw()
        return self.x >= 370 and self.roll_current >= self.ROLL_LENGTH # idle for 1 sec after coming to screen

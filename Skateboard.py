import pygame
import math

# width 170
LENGTH = 170
TAIL_WIDTH = 30
TAIL_ANGLE = 25
TIRE_ANGLE = 23
TIRE_GAP = 33

class Skateboard:
    screen, x, y = None, None, None
    WIDTH = 5
    jump_speed = 3
    
    def __init__(self, _screen, _x, _y, _js) -> None:
        self.screen = _screen
        self.x = _x
        self.y = _y
        self.jump_speed = _js
    
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

        ltx, lty = self.calc_x_y(TIRE_ANGLE, TIRE_GAP)
        pygame.draw.circle(self.screen, "black", (self.x + ltx, self.y + lty),10,3)
        pygame.draw.circle(self.screen, "black", (self.x + LENGTH - ltx, self.y + lty),10,3)
    
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
        pygame.draw.line(self.screen, "black", (self.x + b_x, self.y - b_y), (self.x + b_x - a_x, self.y - (b_y - a_y)), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x + b_x, self.y - b_y), (self.x + b_x + nx, self.y - b_y - ny), width=self.WIDTH)
        pygame.draw.line(self.screen, "black", (self.x + b_x - a_x, self.y - (b_y - a_y)), (self.x + b_x - a_x - tx, self.y - (b_y - a_y) + ty), width=self.WIDTH)
        
        # tires, calc right tire and then just apply the standard angle to another tire
        pygame.draw.circle(self.screen, "black", (self.x + b_x - rtx, self.y - b_y + rty),10,3)
        tire_gap,_ = self.calc_x_y(TIRE_ANGLE, TIRE_GAP)
        ltx, lty = self.calc_x_y(angle, LENGTH - tire_gap * 2)
        pygame.draw.circle(self.screen, "black", (self.x + b_x - rtx - ltx, self.y - b_y + rty + lty),10,3)

    
    rising_angle = 0
    r_asc = True
    r_desc = False
    falling_distance = 0
    travel_distance = 0
    def ollie_2(self):
        
        LIFT_ANGLE = 45
        FALL_SPEED = 5
        NOSE_SPEED = 5
        TAIL_SPEED = 4
        X_SPEED = 1.5
        
        if self.r_asc:
            self.rising_angle += NOSE_SPEED
            self.draw_ollie_nose(self.rising_angle, LENGTH)
            self.travel_distance += X_SPEED / 2
            self.x += X_SPEED / 2
        elif not self.r_desc:
            self.rising_angle -= TAIL_SPEED
            self.travel_distance += X_SPEED
            self.x += X_SPEED
            self.draw_ollie_tail(self.rising_angle * -1, LENGTH, LIFT_ANGLE)
        else:
            #print(self.falling_distance)
            self.falling_distance -= FALL_SPEED
            self.y += FALL_SPEED if self.falling_distance > 0 else 0

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
                print(self.travel_distance)
                return True

        if self.rising_angle >= LIFT_ANGLE:
            self.r_asc = False
        elif self.rising_angle <= 0 and not self.r_desc:
            self.r_desc = True
            _,y = self.calc_x_y(LIFT_ANGLE, LENGTH)
            self.falling_distance = y
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
    
    def draw_start_ollie(self, m):
        # tail
        sx, sy = self.x, self.y - m
        ex, ey = self.x + 20 - m, self.y + 10 + m / 2
        pygame.draw.line(self.screen, "black", (sx, sy), (ex, ey), width=self.WIDTH)

        # deck
        sx, sy = ex, ey
        ex += 130 + m
        ey += 0 + m * 4
        pygame.draw.line(self.screen, "black", (sx, sy), (ex, ey), width=self.WIDTH)

        # tires
        pygame.draw.circle(self.screen, "black", (sx + 20 + m, ey + 15 - m * 3.5), 10, width=self.WIDTH)
        pygame.draw.circle(self.screen, "black", (sx + 110, ey + 15 + m * 0.1), 10, width=self.WIDTH)

        # nose
        sx, sy = ex, ey
        ex += 20 + m
        ey -= 10 - (m * 2)
        pygame.draw.line(self.screen, "black", (sx, sy), (ex, ey), width=self.WIDTH)
        
    
    ROLL_LENGTH = 60
    roll_current = 0
    def roll_to_view(self) -> bool:
        if self.x < 270:
            self.x += 10
        else:
            self.roll_current += 1
        self.draw()
        return self.x >= 270 and self.roll_current >= self.ROLL_LENGTH # idle for 1 sec after coming to screen
    
    JUMP_CAP = -7
    jump_current = 0
    rising = True
    leveling = False
    falling = False
    height_gained = 0
    def ollie(self):
        pop_speed = 0.5
        rise_speed = self.jump_speed
        if self.rising:
            self.y -= rise_speed
            self.height_gained -= rise_speed
            self.jump_current -= pop_speed
            self.draw_start_ollie(self.jump_current)
            if self.jump_current <= self.JUMP_CAP:
                self.rising = False
                self.leveling = True
        elif self.leveling:
            self.y -= rise_speed
            self.height_gained -= rise_speed
            self.jump_current += pop_speed
            self.draw_start_ollie(self.jump_current)
            if self.jump_current >= 0:
                self.leveling = False
                self.falling = True
        elif self.falling:
            self.y += rise_speed * 1.5
            self.height_gained += rise_speed * 1.5
            self.draw()
        if self.height_gained >= 0: # Reset for re-usability
            self.jump_current = 0
            self.rising = True
            self.leveling = False
            self.falling = False
            self.height_gained = 0
        return self.height_gained >= 0
            
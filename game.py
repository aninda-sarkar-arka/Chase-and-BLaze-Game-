from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import time

# Game States
game_started = False
game_over = False
game_won = False
paused = False
current_level = 1


pop_up_messages = []
high_score = 0


camera_pos = (0, -500, 200)
camera_target = (0, 0, 0)
camera_up = (0, 0, 1)
fovY = 60
camera_mode = "third_person"


LANES = [-250, -150, -50, 50, 150, 250]
current_lane = 2
lane_width = 80

# Player Variables
player_x = LANES[current_lane]
player_y = -200
player_z = 15
player_health = 100
player_max_health = 100
player_score = 0
player_speed = 300
cars_dodged = 0

# Nitro System
nitro_active = False
nitro_timer = 0
nitro_count = 2
max_nitro = 4

# Road and Environment
ROAD_LENGTH = 2000
ROAD_WIDTH = 600
road_offset = 0

# Time tracking
last_time = time.time()
level_start_time = 0
level_duration = 75

total_paused_time = 0
pause_start_time = 0



animation_time = 0
spawn_counter = 0

# Missiles/Bullets
missiles = []
missile_speed = 800
last_shot_time = 0
missile_count = 25

# Enemy Cars
enemy_cars = []
enemy_spawn_timer = 0
enemy_spawn_interval = 2.0
enemy_base_speed = 200
boss_car = None

# Power-ups
powerups = []
powerup_spawn_timer = 0


red_obstacles = []


explosions = []

# Level Configurations
level_configs = {
    1: {
        "enemy_speed": 240,
        "spawn_rate": 1.5,
        "cars_to_dodge": 18,
        "max_enemies_on_screen": 6,
        "min_enemies_on_screen": 3,
        "player_speed_boost": 0,
        "enemy_damage": 24,
        "boss_damage": 36,
        "boss": False
    },
    2: {
        "enemy_speed": 420,
        "spawn_rate": 1.2,
        "cars_to_dodge": 24,
        "max_enemies_on_screen": 8,
        "min_enemies_on_screen": 4,
        "player_speed_boost": 50,
        "enemy_damage": 24,
        "boss_damage": 36,
        "boss": False
    },
    3: {
        "enemy_speed": 540,
        "spawn_rate": 1.0,
        "cars_to_dodge": 18,
        "max_enemies_on_screen": 10,
        "min_enemies_on_screen": 5,
        "player_speed_boost": 100,
        "enemy_damage": 24,
        "boss_damage": 36,
        "boss": True
    }
}

# High Score Functions
def load_high_score():
    global high_score
    try:
        with open("highscore.txt", "r") as f:
            high_score = int(f.read())
    except (IOError, ValueError):
        high_score = 0

def save_high_score(new_score):
    global high_score
    if new_score > high_score:
        high_score = new_score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))

def add_pop_up(text, duration=2.0):
    pop_up_messages.append({"text": text, "timer": duration})

class EnemyCar:
    def __init__(self, lane_index, is_boss=False):
        global spawn_counter
        self.lane = lane_index
        self.x = LANES[lane_index]
        self.y = 800
        self.z = 15
        base_speed = level_configs[current_level]["enemy_speed"]

        speed_variation = (spawn_counter * 13) % 100 - 50
        self.speed = base_speed + speed_variation
        self.is_boss = is_boss
        self.health = 240 if is_boss else 24
        self.width = 60 if not is_boss else 80
        self.height = 100 if not is_boss else 140
        self.can_shoot = is_boss
        self.last_shot_time = 0
        self.color = (0.3, 0.0, 0.3) if is_boss else (0.1, 0.1, 0.1)

    def update(self, dt):
        effective_player_speed = player_speed + level_configs[current_level]["player_speed_boost"]
        self.y -= (self.speed + effective_player_speed) * dt

        if self.is_boss and self.can_shoot:
            current_time = time.time()
            if current_time - self.last_shot_time > 1.2:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        missiles.append({
            'x': self.x,
            'y': self.y - 50,
            'z': self.z,
            'vy': -missile_speed,
            'owner': 'enemy',
            'damage': 18
        })

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)

        if self.is_boss:

            glColor3f(0.1, 0.1, 0.1)
            glPushMatrix()
            glScalef(1.0, 1.8, 0.4)
            glutSolidCube(60)
            glPopMatrix()

            # Boss Cabin
            glColor3f(0.05, 0.05, 0.05)
            glPushMatrix()
            glTranslatef(0, -15, 22)
            glScalef(0.8, 0.8, 0.6)
            glutSolidCube(50)
            glPopMatrix()

            # Boss Armor Plating
            glColor3f(0.3, 0.3, 0.3)
            glPushMatrix()
            glTranslatef(0, 50, 5)
            glScalef(1.2, 0.3, 0.2)
            glutSolidCube(50)
            glPopMatrix()

            # Boss Rear Armor
            glPushMatrix()
            glTranslatef(0, -70, 10)
            glScalef(1.1, 0.4, 0.3)
            glutSolidCube(45)
            glPopMatrix()

            # Boss Twin Cannons
            glColor3f(0.2, 0.2, 0.2)
            glPushMatrix()
            glTranslatef(20, 40, 25)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 4, 3, 20, 8, 1)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(-20, 40, 25)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 4, 3, 20, 8, 1)
            glPopMatrix()

        else:

            enemy_colors = [
                (0.1, 0.3, 0.1),  # Dark green
                (0.3, 0.1, 0.1),  # Dark red
                (0.1, 0.1, 0.3),  # Dark blue
                (0.3, 0.3, 0.1),  # Dark yellow
                (0.3, 0.1, 0.3),  # Dark purple
                (0.2, 0.2, 0.2)   # Dark gray
            ]
            car_color = enemy_colors[self.lane]

            # Main Chassis
            glColor3f(*car_color)
            glPushMatrix()
            glScalef(0.7, 1.5, 0.3)
            glutSolidCube(45)
            glPopMatrix()

            # Cabin
            glColor3f(0.1, 0.1, 0.15)  # Dark tinted windows
            glPushMatrix()
            glTranslatef(0, -8, 16)
            glScalef(0.5, 0.6, 0.45)
            glutSolidCube(35)
            glPopMatrix()

            # Front section
            darker_color = (car_color[0]*0.7, car_color[1]*0.7, car_color[2]*0.7)
            glColor3f(*darker_color)
            glPushMatrix()
            glTranslatef(0, 40, 0)
            glScalef(0.6, 0.4, 0.25)
            glutSolidCube(40)
            glPopMatrix()

            # Rear section
            glPushMatrix()
            glTranslatef(0, -40, 0)
            glScalef(0.6, 0.4, 0.25)
            glutSolidCube(40)
            glPopMatrix()

            # Headlights
            glColor3f(0.9, 0.9, 0.7)
            glPushMatrix()
            glTranslatef(12, 50, 2)
            glutSolidCube(4)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(-12, 50, 2)
            glutSolidCube(4)
            glPopMatrix()

            # Taillights
            glColor3f(0.8, 0.1, 0.1)
            glPushMatrix()
            glTranslatef(12, -50, 5)
            glutSolidCube(3)
            glPopMatrix()
            glPushMatrix()
            glTranslatef(-12, -50, 5)
            glutSolidCube(3)
            glPopMatrix()

        # wheels for all enemy cars
        glColor3f(0.05, 0.05, 0.05)
        wheel_radius = 7 if not self.is_boss else 9
        wheel_positions = [
            (18, 35, -8),   # Front-right
            (-18, 35, -8),  # Front-left
            (18, -35, -8),  # Rear-right
            (-18, -35, -8)  # Rear-left
        ]

        if self.is_boss:
            wheel_positions = [
                (25, 40, -10),
                (-25, 40, -10),
                (25, -40, -10),
                (-25, -40, -10)
            ]

        for x, y, z in wheel_positions:
            glPushMatrix()
            glTranslatef(x, y, z)
            gluSphere(gluNewQuadric(), wheel_radius, 10, 10)
            glPopMatrix()

            # Wheel rims
            glColor3f(0.3, 0.3, 0.3)
            glPushMatrix()
            glTranslatef(x, y, z + 2)
            gluSphere(gluNewQuadric(), wheel_radius - 2, 8, 8)
            glPopMatrix()
            glColor3f(0.05, 0.05, 0.05)  # Reset for next wheel

        glPopMatrix()

class PowerUp:
    def __init__(self, lane_index, type):
        self.lane = lane_index
        self.x = LANES[lane_index]
        self.y = 800
        self.z = 20
        self.type = type
        self.collected = False
        self.rotation = 0

    def update(self, dt):
        effective_player_speed = player_speed + level_configs[current_level]["player_speed_boost"]
        self.y -= effective_player_speed * dt
        self.rotation += 180 * dt

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rotation, 0, 0, 1)

        if self.type == "health":
            glColor3f(0, 1, 0)

            glPushMatrix()
            glutSolidCube(30)
            glPopMatrix()
        else:
            glColor3f(1, 0.5, 0)

            glPushMatrix()
            glRotatef(90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 10, 10, 25, 16, 1)
            glPopMatrix()

        glPopMatrix()

#Red Obstacle Class
class RedObstacle:
    def __init__(self, lane_index):
        self.lane = lane_index
        self.x = LANES[lane_index]
        self.y = 1000
        self.z = 25
        self.size = 50

    def update(self, dt):
        effective_player_speed = player_speed + level_configs[current_level]["player_speed_boost"]
        self.y -= effective_player_speed * dt

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glColor3f(1, 0, 0)
        glutSolidCube(self.size)
        glPopMatrix()

class Explosion:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.lifetime = 1.0
        self.particles = []
        for i in range(15):

            angle = i * 24
            speed = 100 + (i * 10)
            self.particles.append({
                'vx': speed * (angle / 180.0 - 1),
                'vy': speed * (angle / 90.0 - 2),
                'vz': speed * (angle / 45.0),
                'x': 0,
                'y': 0,
                'z': 0
            })

    def update(self, dt):
        self.lifetime -= dt
        for p in self.particles:
            p['x'] += p['vx'] * dt
            p['y'] += p['vy'] * dt
            p['z'] += p['vz'] * dt
            p['vz'] -= 200 * dt
        return self.lifetime > 0

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        for p in self.particles:
            glPushMatrix()
            glTranslatef(p['x'], p['y'], p['z'])
            glColor3f(1, self.lifetime, 0)
            gluSphere(gluNewQuadric(), 3, 6, 6)
            glPopMatrix()
        glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):

    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()


    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top


    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
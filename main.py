import pygame

pygame.init()

win = pygame.display.set_mode((500, 480))
pygame.display.set_caption("First Game")

walkRight = [pygame.image.load(r'requirements/R1.png'), pygame.image.load(r'requirements/R2.png'), pygame.image.load(r'requirements/R3.png'),
             pygame.image.load(r'requirements/R4.png'), pygame.image.load(r'requirements/R5.png'), pygame.image.load(r'requirements/R6.png'),
             pygame.image.load(r'requirements/R7.png'), pygame.image.load(r'requirements/R8.png'), pygame.image.load(r'requirements/R9.png')]
walkLeft = [pygame.image.load(r'requirements/L1.png'), pygame.image.load(r'requirements/L2.png'), pygame.image.load(r'requirements/L3.png'),
            pygame.image.load(r'requirements/L4.png'), pygame.image.load(r'requirements/L5.png'), pygame.image.load(r'requirements/L6.png'),
            pygame.image.load(r'requirements/L7.png'), pygame.image.load(r'requirements/L8.png'), pygame.image.load(r'requirements/L9.png')]
bg = pygame.image.load(r'requirements/bg.jpg')
char = pygame.image.load(r'requirements/standing.png')

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound(r'requirements/bullet.wav')
hitSound = pygame.mixer.Sound(r'requirements/hit.wav')
music = pygame.mixer.music.load(r'requirements/music.mp3')
pygame.mixer.music.play(-1)


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 6
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.score = 0

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if not self.standing:
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)



    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.score -= 10
        self.x = 60
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render(str(man.score), 1, (255, 0, 0))
        win.blit(text, (250 - (text.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class enemy(object):
    walkRight = [pygame.image.load(r'requirements/R1E.png'), pygame.image.load(r'requirements/R2E.png'), pygame.image.load(r'requirements/R3E.png'),
                 pygame.image.load(r'requirements/R4E.png'), pygame.image.load(r'requirements/R5E.png'), pygame.image.load(r'requirements/R6E.png'),
                 pygame.image.load(r'requirements/R7E.png'), pygame.image.load(r'requirements/R8E.png'), pygame.image.load(r'requirements/R9E.png'),
                 pygame.image.load(r'requirements/R10E.png'), pygame.image.load(r'requirements/R11E.png')]
    walkLeft = [pygame.image.load(r'requirements/L1E.png'), pygame.image.load(r'requirements/L2E.png'), pygame.image.load(r'requirements/L3E.png'),
                pygame.image.load(r'requirements/L4E.png'), pygame.image.load(r'requirements/L5E.png'), pygame.image.load(r'requirements/L6E.png'),
                pygame.image.load(r'requirements/L7E.png'), pygame.image.load(r'requirements/L8E.png'), pygame.image.load(r'requirements/L9E.png'),
                pygame.image.load(r'requirements/L10E.png'), pygame.image.load(r'requirements/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.width = width
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.health = 100
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0),
                             [self.hitbox[0], self.hitbox[1] - 20, 50 - 0.5 * (100 - self.health), 10])
            self.hitbox = (self.x + 20, self.y, 28, 60)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            goblin.health -= 10
        else:
            goblin.visible = False


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


font = pygame.font.SysFont('comicsans', 30, True)


def redrawGameWindow():
    global walkCount
    win.blit(bg, (0, 0))
    text = font.render('Score : ' + str(man.score), 1, (0, 0, 0))
    win.blit(text, (370, 10))
    text1 = font.render('Health : ' + str(goblin.health), 1, (0, 0, 0))
    win.blit(text1, (30, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


man = player(200, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = []
shootLoop = 0
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if goblin.visible and bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + \
                    goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                man.score += 5
                bullets.pop(bullets.index(bullet))
        if 500 > bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(
                projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x + man.width + man.vel < 500:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if goblin.visible and man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
        if goblin.hitbox[0] < man.hitbox[0] + man.hitbox[2] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()

    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1

            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()
pygame.quit()

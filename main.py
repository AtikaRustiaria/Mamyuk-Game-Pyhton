import pygame, sys, time, random, colorsys, math
from pygame.math import Vector2
from pygame.locals import *
from player import Player
from background import Background
from button import Button
from food import makanan
from utils import clamp
from utils import checkCollisions


def main():
    pygame.init()
    # set tampilan
    DISPLAY=pygame.display.set_mode((640,480),0,32)
    pygame.display.set_caption('MamYuk')
    pygame.display.set_icon(makanan().sprite)
    # fonts
    font = pygame.font.Font('data/fonts/font.otf', 100)
    font_small = pygame.font.Font('data/fonts/font.otf', 32)
    font_20 = pygame.font.Font('data/fonts/font.otf', 20)
    # gambar
    shop = pygame.image.load('data/gambar/shop.png')
    shop_bg = pygame.image.load('data/gambar/shop_bg.png')
    retry_button = pygame.image.load('data/gambar/retry_button.png')
    logo = pygame.image.load('data/gambar/logo.png')
    bgawal= pygame.image.load('data/gambar/bg.jpg')
    bgawal.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
    # sounds
    flapfx = pygame.mixer.Sound("data/lagu/flap.wav")
    upgradefx = pygame.mixer.Sound("data/lagu/upgrade.wav")
    beanfx = pygame.mixer.Sound("data/lagu/bean.wav")
    deadfx = pygame.mixer.Sound("data/lagu/dead.wav")
    # warna
    WHITE=(255,255,255) # constant
    # variables
    rotOffset = -5
    # membuat object player baru
    player = Player()
    foods = []
    buttons = []
    # menambahkan tiga buttons
    for i in range(3): buttons.append(Button())
    # memuat gambar button berdasarkan indeks dalam daftar
    buttons[0].typeIndicatorSprite = pygame.image.load('data/gambar/flap_indicator.png')
    buttons[0].price = 5
    buttons[1].typeIndicatorSprite = pygame.image.load('data/gambar/speed_indicator.png')
    buttons[1].price = 5
    buttons[2].typeIndicatorSprite = pygame.image.load('data/gambar/beanup_indicator.png')
    buttons[2].price = 30
    # mengumpulkan 5 makanan
    for i in range(5): foods.append(makanan())
    # looping berdasarkan list jumlah makanan
    for food in foods:
        food.position.xy = random.randrange(0, DISPLAY.get_width() - food.sprite.get_width()), foods.index(food)*-200 - player.position.y
    # membuat list backgrounds, tiap index sbg object
    bg = [Background(), Background(), Background()]
    # variables lainnya
    beanCount = 0
    startingHeight = player.position.y
    height = 0
    health = 100
    flapForce = 3
    beanMultiplier = 5
    dead = False
    #  framerate dan time
    framerate = 60
    last_time = time.time()
    splashScreenTimer = 0
    #splash screen
    # play sound
    pygame.mixer.Sound.play(flapfx)
    while splashScreenTimer < 100:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()

        splashScreenTimer += dt

        for event in pygame.event.get():
            # user klik button
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        DISPLAY.fill((255,222,89))
        # tampilan awal game
        startMessage = font_small.render("BY \n Kelompok 2-Kelas J", True,(197,10,6))
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, DISPLAY.get_height()/2 - startMessage.get_height()/2))

        # update display
        pygame.display.update()
        # tunggu 10 detik sebelum masuk menu utama
        pygame.time.delay(10)

    titleScreen = True
    # menu utama
    pygame.mixer.Sound.play(flapfx)
    while titleScreen:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # get the position of the mouse
        mouseX,mouseY = pygame.mouse.get_pos()
        # getting the keys pressed
        clicked = False
        keys = pygame.key.get_pressed()
        # checking events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            # keluar
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
        # user clicked, dan jika cursor dibuttons
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, DISPLAY.get_width()/2 - retry_button.get_width()/2, 288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            pygame.mixer.Sound.play(upgradefx)
            titleScreen = False

        DISPLAY.fill(WHITE)
        #DISPLAY.blit(title_bg, (0,0))
        DISPLAY.blit(bgawal,(0,0))
        DISPLAY.blit(logo, (DISPLAY.get_width()/2 - logo.get_width()/2, DISPLAY.get_height()/2 - logo.get_height()/2 + math.sin(time.time()*5)*5 - 25))
        DISPLAY.blit(retry_button, (DISPLAY.get_width()/2 - retry_button.get_width()/2, 288))
        startMessage = font_small.render("START", True, (171, 145, 123))
        
        DISPLAY.blit(startMessage, (DISPLAY.get_width()/2 - startMessage.get_width()/2, 292))

        pygame.display.update()
        pygame.time.delay(10)

    # tampilan utama game(saatnya bermain)
    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        # get the position
        mouseX,mouseY = pygame.mouse.get_pos()

        jump = False
        clicked = False
        keys = pygame.key.get_pressed()
        # get events
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN and event.key==K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        camOffset = -player.position.y + DISPLAY.get_height()/2 - player.currentSprite.get_size()[1]/2

        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y/50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((player.position.y/50) % 100) / 100,0.5,0.5)
        currentHeightMarker = font.render(str(height), True, (color[0]*255, color[1]*255, color[2]*255, 50 ))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width()/2 - currentHeightMarker.get_width()/2, camOffset + round((player.position.y - startingHeight)/DISPLAY.get_height())*DISPLAY.get_height() + player.currentSprite.get_height() - 40))

        for food in foods:
            DISPLAY.blit(food.sprite, (food.position.x, food.position.y + camOffset))

        DISPLAY.blit(pygame.transform.rotate(player.currentSprite, clamp(player.velocity.y, -10, 5)*rotOffset), (player.position.x,player.position.y + camOffset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY,(81,48,20),(21,437,150*(health/100),25))
        DISPLAY.blit(shop, (0, 0))

        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (buttons.index(button)*125), 393))
            priceDisplay = font_small.render(str(button.price), True, (0,0,0))
            DISPLAY.blit(priceDisplay, (280 + (buttons.index(button)*125), 408))
            levelDisplay = font_20.render('Lvl. ' + str(button.level), True, (200,200,200))
            DISPLAY.blit(levelDisplay, (234 + (buttons.index(button)*125), 441))
            DISPLAY.blit(button.typeIndicatorSprite, (202 + (buttons.index(button)*125), 377))
        beanCountDisplay = font_small.render(str(beanCount).zfill(7), True, (0,0,0))
        DISPLAY.blit(beanCountDisplay, (72, 394))
        if dead:
            DISPLAY.blit(retry_button, (4, 4))
            deathMessage = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))

        height = round(-(player.position.y - startingHeight)/DISPLAY.get_height())

        player.position.x += player.velocity.x*dt
        if player.position.x + player.currentSprite.get_size()[0] > 640:
            player.velocity.x = -abs(player.velocity.x)
            player.currentSprite = player.leftSprite
            rotOffset = 5
        if player.position.x < 0:
            player.velocity.x = abs(player.velocity.x)
            player.currentSprite = player.rightSprite
            rotOffset = -5
        if jump and not dead:
            player.velocity.y = -flapForce
            pygame.mixer.Sound.play(flapfx)
        player.position.y += player.velocity.y*dt
        player.velocity.y = clamp(player.velocity.y + player.acceleration*dt, -99999999999, 50)

        health -= 0.2*dt
        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(deadfx)


        for food in foods:
            if food.position.y + camOffset + 90 > DISPLAY.get_height():
                food.position.y -= DISPLAY.get_height()*2
                food.position.x = random.randrange(0, DISPLAY.get_width() - food.sprite.get_width())
            if (checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(), player.currentSprite.get_height(), food.position.x, food.position.y, food.sprite.get_width(), food.sprite.get_height())):
                dead = False
                pygame.mixer.Sound.play(beanfx)
                beanCount += 1
                health = 100
                food.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                food.position.x = random.randrange(0, DISPLAY.get_width() - food.sprite.get_width())

        for button in buttons:
            buttonX,buttonY = 220 + (buttons.index(button)*125), 393
            if clicked and not dead and checkCollisions(mouseX, mouseY, 3, 3, buttonX, buttonY, button.sprite.get_width(), button.sprite.get_height()):
                if (beanCount >= button.price):
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    beanCount -= button.price
                    button.price = round(button.price*2.5)
                    if (buttons.index(button) == 0):
                        flapForce *= 1.5
                    if (buttons.index(button) == 1):
                        player.velocity.x *= 1.5
                    if (buttons.index(button) == 2):
                        oldBeanMultipler = beanMultiplier
                        beanMultiplier += 10
                        for i in range(beanMultiplier):
                            foods.append(makanan())
                            foods[-1].position.xy = random.randrange(0, DISPLAY.get_width() - food.sprite.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(0, 200)

        if dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, retry_button.get_width(), retry_button.get_height()):
            health = 100
            player.velocity.xy = 3, 0
            player.position.xy = 295, 100
            player.currentSprite = player.rightSprite
            beanCount = 0
            height = 0
            flapForce = 3
            beanMultiplier = 5
            buttons = []
            for i in range(3): buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load('data/gambar/flap_indicator.png')
            buttons[0].price = 5
            buttons[1].typeIndicatorSprite = pygame.image.load('data/gambar/speed_indicator.png')
            buttons[1].price = 5
            buttons[2].typeIndicatorSprite = pygame.image.load('data/gambar/beanup_indicator.png')
            buttons[2].price = 30
            foods = []
            for i in range(5): foods.append(makanan())
            for food in foods:
                food.position.xy = random.randrange(0, DISPLAY.get_width() - food.sprite.get_width()), foods.index(food)*-200 - player.position.y
            pygame.mixer.Sound.play(upgradefx)
            dead = False


        bg[0].position = camOffset + round(player.position.y/DISPLAY.get_height())*DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height()
        bg[2].position = bg[0].position - DISPLAY.get_height()

        pygame.display.update()
        pygame.time.delay(10)

if __name__ == "__main__":
    main()

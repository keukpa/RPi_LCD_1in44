import time
import random
import LCD_1in44
import LCD_Config

import RPi.GPIO as GPIO

from PIL import Image,ImageDraw,ImageFont,ImageColor

### DEFINES ###
SCREEN_SIZE = 128
SCREEN_MAX = 127
SCREEN_MIN = 0
GAME_TICK = 0.1


### KEY PAD CONTROL ###
KEY_UP_PIN	= 6
KEY_DOWN_PIN	= 19
KEY_LEFT_PIN	= 5
KEY_RIGHT_PIN	= 26
KEY_PRESS_PIN	= 13
KEY1_PIN	= 21
KEY2_PIN	= 20
KEY3_PIN	= 16

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(KEY_UP_PIN,      GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_LEFT_PIN,    GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(KEY_RIGHT_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY_PRESS_PIN,   GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(KEY1_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY2_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(KEY3_PIN,        GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

### Display setup SPI ###
disp = LCD_1in44.LCD()
Lcd_ScanDIR = LCD_1in44.SCAN_DIR_DFT
disp.LCD_Init(Lcd_ScanDIR)
disp.LCD_Clear()

### Init Screen set to blank ###
image = Image.new("RGB", (disp.width, disp.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, disp.width, disp.height), outline = 0, fill = "BLACK")
disp.LCD_ShowImage(image, 0, 0)

### SNAKE PARAMETERS ###
# init start pos
SnakeHeadX = [24]
SnakeHeadY = [48]

def main():
    print "hi\n"

    ### SNAKE INITS ###
    SNAKE_DIR_X = 0
    SNAKE_DIR_Y = 0
    FoodPosX = 96
    FoodPosY = 16
    SNAKE_EATS = False
    GENERATE_FOOD = False
    GAME_OVER = 0

    while True:

        ### SNAKE EATS ###
        if FoodPosX == SnakeHeadX[0] and FoodPosY == SnakeHeadY[0]:
            SNAKE_EATS = True
            GENERATE_FOOD = True
            while GENERATE_FOOD:
                FoodPosX = random.randint(0,15)*8
                FoodPosY = random.randint(0,15)*8
                GENERATE_FOOD = False
                for x, y in zip(SnakeHeadX, SnakeHeadY):
                    if x == FoodPosX and y == FoodPosY:
                        GENERATE_FOOD = True
                        break

        ### GROW SNAKE ###
        if SNAKE_EATS:
            SNAKE_EATS = False
            SnakeHeadX.append(0)
            SnakeHeadY.append(0)

        ### CHECK FOR INPUT ###
        if GPIO.input(KEY_RIGHT_PIN) == 0 and SNAKE_DIR_X != -1: # Joy R pressed
            SNAKE_DIR_X = 1
            SNAKE_DIR_Y = 0
            print "RIGHT PRESSED\n"
        if GPIO.input(KEY_LEFT_PIN) == 0 and SNAKE_DIR_X != 1: # Joy L pressed
            SNAKE_DIR_X = -1
            SNAKE_DIR_Y = 0
            print "LEFT PRESSED\n"
        if GPIO.input(KEY_UP_PIN) == 0 and SNAKE_DIR_Y != 1: # Joy U pressed
            SNAKE_DIR_X = 0
            SNAKE_DIR_Y = -1
            print "RIGHT PRESSED\n"
        if GPIO.input(KEY_DOWN_PIN) == 0 and SNAKE_DIR_Y != -1: # Joy D pressed
            SNAKE_DIR_X = 0
            SNAKE_DIR_Y = 1
            print "RIGHT PRESSED\n"


        print "SNAKE: %s", SNAKE_DIR_X

        ### MOVEMENT ###
        for i in range((len(SnakeHeadX) -1), 0, -1):
            SnakeHeadX[i] = SnakeHeadX[i-1]
            SnakeHeadY[i] = SnakeHeadY[i-1]

        SnakeHeadX[0] += SNAKE_DIR_X*8
        SnakeHeadY[0] += SNAKE_DIR_Y*8

        if SnakeHeadX[0] < SCREEN_MIN:
            SnakeHeadX[0] = SCREEN_MAX-7
        elif SnakeHeadX[0]+7 > SCREEN_MAX:
            SnakeHeadX[0] = SCREEN_MIN
        if SnakeHeadY[0] < SCREEN_MIN:
            SnakeHeadY[0] = SCREEN_MAX-7
        elif SnakeHeadY[0]+7 > SCREEN_MAX:
            SnakeHeadY[0] = SCREEN_MIN

        ### CHECK COLLISIONS ###
        for i in range(1, len(SnakeHeadX)):
            if SnakeHeadX[i] == SnakeHeadX[0] and SnakeHeadY[i] == SnakeHeadY[0]:
                GAME_OVER = True
                exit()


        ### DRAW SCREEN ###
        #disp.LCD_Clear()
        draw.rectangle((0, 0, disp.width, disp.height), outline = 0, fill = "BLACK")
        for x, y in zip(SnakeHeadX, SnakeHeadY):
            draw.rectangle((x, y, x+7, y+7), outline="GREEN", fill="GREEN")
            draw.point((x, y), fill="GREEN")

        draw.rectangle((FoodPosX, FoodPosY, FoodPosX+7, FoodPosY+7), outline="RED", fill="RED")

        ### UPDATE THE SCREEN ###
        disp.LCD_ShowImage(image, 0, 0)


        time.sleep(GAME_TICK)


if __name__ == '__main__':
    main()





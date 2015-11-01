"""Author: Benson Pan
   Date: April 20, 2014
   Description: Scrambled Eggs - A Flappy Bird Remake
"""
#Import
import pygame, SEsprites
pygame.init()
pygame.mixer.init()

def main():
    #Display
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Scrambled Eggs")

    #Entities
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))

    #Load music and sound effect
    pygame.mixer.music.load("./Resources/song.mp3")
    pygame.mixer.music.set_volume(0.250)
    pygame.mixer.music.play(-1)
    score_sound = pygame.mixer.Sound("./Resources/coin.wav")
    score_sound.set_volume(0.5)
    press_sound = pygame.mixer.Sound("./Resources/press.wav")
    press_sound.set_volume(0.125)
    crack_sound = pygame.mixer.Sound("./Resources/crack.wav")

    #creates the title screen objects and puts them in a group
    overlay = SEsprites.Title_overlay(screen.get_width(), screen.get_height())
    play_button = SEsprites.Button(screen.get_width(), screen.get_height(), -70, 100, "Play")
    quit_button = SEsprites.Button(screen.get_width(), screen.get_height(), 70, 100, "Quit")
    titleGroup = pygame.sprite.Group(overlay, play_button, quit_button)

    #creates the game over objects and puts them in a group
    game_over = SEsprites.Game_over_overlay(screen.get_width(), screen.get_height())
    score = SEsprites.Score_label(screen.get_width(), screen.get_height(), "score")
    highscore = SEsprites.Score_label(screen.get_width(), screen.get_height(), "highscore")
    retry_button = SEsprites.Button(screen.get_width(), screen.get_height(), -70, 100, "Retry")
    exit_button = SEsprites.Button(screen.get_width(), screen.get_height(), 70, 100, "Exit")
    gameOverGroup = pygame.sprite.Group(game_over, score, highscore, retry_button, exit_button)

    #creates the scrolling background and puts it into its own group
    background1 = SEsprites.Background(screen.get_width())
    background2 = SEsprites.Background(screen.get_width())
    background2.set_x_zero() #runs this method to position the second background
    backgroundGroup = pygame.sprite.Group(background1, background2)

    #Creates the score_label and egg and puts it into a group
    egg = SEsprites.Egg()
    score_keeper = SEsprites.Score_keeper(screen.get_width())
    allGroup = pygame.sprite.Group(egg, score_keeper)

    #Creates the instructions label and puts it into its own group
    instructionsGroup = pygame.sprite.Group(SEsprites.Instructions(150, 150))

    #Creates 2 pairs of pipes, and joins them in a nested group
    top_pipe1 = SEsprites.Top_pipe(screen.get_width(), screen.get_height())
    bot_pipe1 = SEsprites.Bottom_pipe(screen.get_width(), screen.get_height(),\
                                  top_pipe1.get_bottom())
    pipeGroup1 = pygame.sprite.Group(top_pipe1, bot_pipe1)

    top_pipe2 = SEsprites.Top_pipe(screen.get_width(), screen.get_height())
    bot_pipe2 = SEsprites.Bottom_pipe(screen.get_width(), screen.get_height(),\
                                  top_pipe2.get_bottom())
    pipeGroup2 = pygame.sprite.Group(top_pipe2, bot_pipe2)

    pipeGroup = pygame.sprite.Group(pipeGroup1, pipeGroup2)

    #Action
    #Assign
    clock = pygame.time.Clock()
    keepGoing = True #Main game loop variable
    game_start = False #Space bar triggered variable to activate pipes
    obtain_score1 = True #Pipe score limiter
    obtain_score2 = False #Pipe score limiter
    play = False #variable before game_start; must be triggered before it can be triggered
    end_screen =  False #game over screen
    instructions_visible = False
    pressed = pygame.key.get_pressed()
    zero_pressed = pressed #stores the no key press data for use in reseting

    #Loop
    while keepGoing:
        #Time
        clock.tick(60)

        #Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False


        #Mouse handler
        if not play and not end_screen:
            #Title Screen
            if play_button.get_rect().collidepoint(pygame.mouse.get_pos()):
                play_button.hover(True)
                if pygame.mouse.get_pressed()[0]:
                    press_sound.play()
                    play = True
            else:
                play_button.hover(False)

            if quit_button.get_rect().collidepoint(pygame.mouse.get_pos()):
                quit_button.hover(True)
                if pygame.mouse.get_pressed()[0]:
                    press_sound.play()
                    keepGoing = False
            else:
                quit_button.hover(False)
        elif end_screen:
            #Game Over Screen
            if retry_button.get_rect().collidepoint(pygame.mouse.get_pos()):
                retry_button.hover(True)
                if pygame.mouse.get_pressed()[0]:
                    #Starts game directly by changing play to true
                    press_sound.play()
                    end_screen = False
                    play = True
            else:
                retry_button.hover(False)

            if exit_button.get_rect().collidepoint(pygame.mouse.get_pos()):
                exit_button.hover(True)
                if pygame.mouse.get_pressed()[0]:
                    press_sound.play()
                    end_screen = False
                    #Delay slightly, as to not trigger the quit button when changing screens
                    pygame.time.delay(200)
            else:
                exit_button.hover(False)
        else:
            #Only allows press updates when they click the play button
            pressed = pygame.key.get_pressed()

        #Key handler
        if not game_start:
            instructions_visible = True
            if pressed[pygame.K_SPACE]:
                #Starts moving pipes when space is pressed once
                instructions_visible = False
                game_start = True
                egg.start()
                top_pipe1.move_pipe()
                bot_pipe1.move_pipe()

        if game_start:
            if pressed[pygame.K_SPACE]:
                #moves egg if space is pressed
                egg.jump()

            #Start moving the other set of pipes when one pair reached the middle and adds score
            if top_pipe1.get_x() <= (screen.get_width() / 2):
                top_pipe2.move_pipe()
                bot_pipe2.move_pipe()
                if obtain_score1:
                    score_keeper.add_score()
                    score_sound.play()
                    obtain_score1 = False
                    obtain_score2 = True
            elif top_pipe2.get_x() <= (screen.get_width() / 2):
                top_pipe1.move_pipe()
                bot_pipe1.move_pipe()
                if obtain_score2:
                    score_keeper.add_score()
                    score_sound.play()
                    obtain_score2 = False
                    obtain_score1 = True

            #Resets and stops pipes when they reach the end
            if top_pipe1.check_boundaires():
                bot_pipe1.reset(top_pipe1.get_bottom())
            elif top_pipe2.check_boundaires():
                bot_pipe2.reset(top_pipe2.get_bottom())

            if pygame.sprite.spritecollide(egg, pipeGroup, False) or \
               (egg.get_top() <= 0) or (egg.get_bot() >= screen.get_height()):
                #FULL GAME SPRITE ATTRIBUTE RESET
                if egg.get_pic_num() == 1:
                    #Animate the egg after pausing the pipes from moving
                    crack_sound.play()
                    top_pipe1.pause()
                    bot_pipe1.pause()
                    top_pipe2.pause()
                    bot_pipe2.pause()
                    egg.set_animate()
                if egg.get_pic_num() > 9:
                    #After egg animation is complete, reset all attributes
                    pygame.time.delay(500)
                    highscore.update_highscore(score_keeper.get_score())
                    score.update_highscore(score_keeper.get_score())
                    top_pipe1.reset()
                    top_pipe2.reset()
                    bot_pipe1.reset(top_pipe1.get_bottom())
                    bot_pipe2.reset(top_pipe2.get_bottom())
                    egg.reset()
                    score_keeper.reset()
                    pressed = zero_pressed #resets the press, to prevent "ghost jumps"
                    obtain_score1 = True #Ensures first pipe is first
                    obtain_score2 = False
                    game_start = False
                    play = False
                    end_screen = True

        #Refresh
        screen.blit(background, (0, 0))

        #Clear, update and draw is conditional, depending on what part of the game it is
        backgroundGroup.clear(screen,background)
        if play:
            #Main game items (in-game)
            pipeGroup.clear(screen,background)
            allGroup.clear(screen,background)
            if instructions_visible:
                #If player hasnt pressed space yet, instructions are visible
                instructionsGroup.clear(screen, background)
        elif not play and end_screen:
            #Game over screen items
            gameOverGroup.clear(screen, background)
        else:
            #Title screen items
            titleGroup.clear(screen,background)

        backgroundGroup.update()
        if play:
            pipeGroup.update()
            allGroup.update()
            if instructions_visible:
                instructionsGroup.update()
        elif not play and end_screen:
            gameOverGroup.update()
        else:
            titleGroup.update()

        backgroundGroup.draw(screen)
        if play:
            pipeGroup.draw(screen)
            allGroup.draw(screen)
            if instructions_visible:
                instructionsGroup.draw(screen)
        elif not play and end_screen:
            gameOverGroup.draw(screen)
        else:
            titleGroup.draw(screen)

        pygame.display.flip()

    #Fade out music and delays the program quit
    pygame.mixer.music.fadeout(1750)
    pygame.time.delay(2000)
    pygame.quit()

main()
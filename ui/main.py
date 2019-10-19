import pygame as pg

screen = pg.display.set_mode((640, 480))

def get_player_hash():
    
    font = pg.font.Font(None, 20)
    clock = pg.time.Clock()
    input_box = pg.Rect(220, 200, 140, 20)
    color_inactive = pg.Color('lightgreen')
    color_active = pg.Color('green')
    color = color_inactive
    active = False
    text = ''
    done = False
    myfont = pg.font.SysFont('Comic Sans MS', 15)
    enter_hash = myfont.render('Enter player 1 hash', False, (255, 255, 255))
    hash_button = pg.Rect(260, 230, 120, 20)
    button_text = myfont.render('Enter', False, (255, 255, 255))
    button_color = (0,200,0)
    bright_green = (0,255,0)
    player_hash = ''
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
                mouse_pos = event.pos
                if hash_button.collidepoint(mouse_pos):
                    print('button was pressed at {0}'.format(mouse_pos))
                    button_color = bright_green
                    player_hash = text
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        player_hash = text
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        if player_hash == '':
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            screen.blit(enter_hash,(input_box.x+25, input_box.y-25))
            # Blit the input_box rect.
            pg.draw.rect(screen, color, input_box, 2)
            pg.draw.rect(screen, button_color, hash_button, 0)
            screen.blit(button_text, (hash_button.x + 40, hash_button.y))
        else:
               
        pg.display.flip()
        clock.tick(30)

def main():
    player_hash = get_player_hash()




if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
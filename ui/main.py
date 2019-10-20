import pygame as pg

def display_text(msg, textx, texty, screen, text_color=(0, 0, 0), background_color=None):
    msgFont = pg.font.SysFont('Comic Sans MS', 15)
    textSurface = msgFont.render(msg, True, text_color, background_color)
    textRect = textSurface.get_rect()
    textRect.center = (textx, texty)
    screen.blit(textSurface, textRect)

class  Card:
    def __init__(self, name, image, attack, defence):
        self.name = name
        self.image = image
        self.attack = attack
        self.defence = defence
class CardSprite(pg.sprite.Sprite):
    def __init__(self, card, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(str(card.image))
        self.image = pg.transform.scale(self.image, (100, 150))
        # print(self.image)
        self.attack = card.attack
        self.defence = card.defence
        self.name = card.name
        self.x = int(x)
        self.y = int(y)

    def draw(self, gamedisplay):
        gamedisplay.blit(self.image, (self.x, self.y))
        display_text(self.name, self.x + 20, self.y +10, gamedisplay)
        display_text("Attack: " + str(self.attack), self.x + 20, self.y +100, gamedisplay)
        display_text("Defence: " + str(self.defence), self.x + 20, self.y +110, gamedisplay)

def main():

    screen = pg.display.set_mode((640, 480))
    pg.display.set_caption('Chained')
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
    button_color = (0,200,0)
    bright_green = (0,255,0)
    player_hash = ''

    enter_hash = myfont.render('Enter player hash', False, (255, 255, 255))
    hash_button = pg.Rect(260, 230, 120, 20)
    button_text = myfont.render('Enter', False, (255, 255, 255))

    game_state = "get_hash"

    card=Card("new", "blank.png", 10,10)
    card1=Card("new1", "blank.png", 11,11)
    testSprite = CardSprite(card, 300, 300)
    testSprite1 = CardSprite(card1, 350, 300)

    while not done:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT :
                done = True
        if game_state == "get_hash":
            for event in events:
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
                        game_state = "display_cards"
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
        if game_state == "display_cards":
            screen.fill((30, 30, 30))
            testSprite.draw(screen)
            testSprite1.draw(screen)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
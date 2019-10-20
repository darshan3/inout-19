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
        
        # print(self.image)
        self.attack = card.attack
        self.defence = card.defence
        self.name = card.name
        self.x = int(x)
        self.y = int(y)
        self.card_active = True
        self.front_image = card.image
        self.back_image = 'card_back.png'
        self.selected_image = 'selected.png'
        self.played = False
        self.highlight = False

    def draw(self, gamedisplay):
        if not self.played:
            if self.card_active:
                if self.highlight:
                    self.image = pg.image.load(str(self.selected_image))
                    self.image = pg.transform.scale(self.image, (100, 150))
                else:
                    self.image = pg.image.load(str(self.front_image))
                    self.image = pg.transform.scale(self.image, (100, 150))
                gamedisplay.blit(self.image, (self.x, self.y))
                display_text(self.name, self.x + 20, self.y +10, gamedisplay)
                display_text("Attack: " + str(self.attack), self.x + 40, self.y +100, gamedisplay)
                display_text("Defence: " + str(self.defence), self.x + 45, self.y +120, gamedisplay)
            else:
                self.image = pg.image.load(str(self.back_image))
                self.image = pg.transform.scale(self.image, (100, 150))
                gamedisplay.blit(self.image, (self.x, self.y))
        

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

    red_color = (255, 0, 0)

    enter_hash = myfont.render('Enter player hash', False, (255, 255, 255))
    hash_button = pg.Rect(260, 230, 120, 20)
    button_text = myfont.render('Enter', False, (255, 255, 255))

    game_state = "get_hash"

    card1=Card("new", "blank.png", 10,10)
    card2=Card("new1", "blank.png", 20,20)
    card3 = Card("new2", "blank.png", 30, 30)
    
    # card1_sprite = CardSprite(card1, 300, 300)
    # card2_sprite = CardSprite(card2, 190, 300)
    # card3_sprite = CardSprite(card3, 410, 300)

    attack_button = pg.Rect(190, 460, 100, 20)
    attack_text = myfont.render('ATTACK', False, (255, 255, 255))
    attack_color = bright_green

    defense_button = pg.Rect(410, 460, 100, 20)
    defense_text = myfont.render('DEFENSE', False, (255, 255, 255))
    defense_color = red_color

    join_button = pg.Rect(300, 460, 100, 20)
    join_text = myfont.render('JOIN', False, (255, 255, 255))
    join_color = red_color

    all_cards = []
    for i in range(0,6):
        all_cards.append(card1)
    all_card_sprites = []
    selected_cards = []
    start_x = 190
    start_y = 50
    i = 0
    for card in all_cards:
        if i < 3:
            all_card_sprites.append(CardSprite(card, start_x + i*110, start_y))
        else:
            all_card_sprites.append(CardSprite(card, start_x + (i-3)*110, start_y + 200))
        i = i + 1
        
    while not done:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT :
                done = True
        if game_state == "lobby":
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for card_sprite in all_card_sprites:
                        if card_sprite.x < mouse_pos[0] < card_sprite.x + 100 and card_sprite.y < mouse_pos[1] < card_sprite.y + 150:
                            card_sprite.highlight = not card_sprite.highlight

                    if join_button.collidepoint(mouse_pos):
                        for card_sprite in all_card_sprites:
                                if card_sprite.highlight:
                                    selected_cards.append(card_sprite)
                        if(len(selected_cards)==3):
                            card1_sprite = selected_cards[0]
                            card1_sprite.x = 190
                            card1_sprite.y = 300
                            card1_sprite.highlight = False
                            card2_sprite = selected_cards[1]
                            card2_sprite.x = 300
                            card2_sprite.y = 300
                            card2_sprite.highlight = False
                            card3_sprite = selected_cards[2]
                            card3_sprite.x = 410
                            card3_sprite.y = 300
                            card3_sprite.highlight = False
                            game_state = "display_cards"
                        else:
                            selected_cards = []
                        print(selected_cards)
            screen.fill((30, 30, 30))
            for card_sprite in all_card_sprites:
                card_sprite.draw(screen)
            pg.draw.rect(screen, defense_color, join_button, 0)
            screen.blit(join_text, (join_button.x + 20, join_button.y))

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
                    pos = pg.mouse.get_pos()
                    print(pos)
                    if hash_button.collidepoint(mouse_pos):
                        print('button was pressed at {0}'.format(mouse_pos))
                        button_color = bright_green
                        player_hash = text
                        game_state = "lobby"
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            player_hash = text
                            game_state = "lobby"
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
            # card1_sprite.draw(screen)
            for events in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    print(pos)
                    if card1_sprite.x < pos[0] < card1_sprite.x + 100 and card1_sprite.y < pos[1] < card1_sprite.y + 150:
                        card1_sprite.card_active = True
                    if card2_sprite.x < pos[0] < card2_sprite.x + 100 and card2_sprite.y < pos[1] < card2_sprite.y + 150:
                        card2_sprite.card_active = True
                    if card3_sprite.x < pos[0] < card3_sprite.x + 100 and card3_sprite.y < pos[1] < card3_sprite.y + 150:
                        card3_sprite.card_active = True
                    
                    # if card1_sprite.card_active:
                    #     if card1_sprite.x + 5 < pos[0] < card1_sprite.x + 80 and card1_sprite.y + 90 <= pos[1] < card1_sprite.y + 110:
                    #         print('Attack' + str(card1_sprite.attack))
                    #         card1_sprite.card_active = False
                    #         card1_sprite.played = True
                    #     if card1_sprite.x + 5 < pos[0] < card1_sprite.x + 80 and card1_sprite.y + 110 <= pos[1] <= card1_sprite.y + 130:
                    #         print('Defense' + str(card1_sprite.defence))
                    #         card1_sprite.card_active = False
                    #         card1_sprite.played = True
                    
                    # if card2_sprite.card_active:
                    #     if card2_sprite.x + 5 < pos[0] < card2_sprite.x + 80 and card2_sprite.y + 90 <= pos[1] < card2_sprite.y + 110:
                    #         print('Attack' + str(card2_sprite.attack))
                    #         card2_sprite.card_active = False
                    #         card2_sprite.played = True
                    #     if card2_sprite.x + 5 < pos[0] < card2_sprite.x + 80 and card2_sprite.y + 110 <= pos[1] <= card2_sprite.y + 130:
                    #         print('Defense' + str(card2_sprite.defence))
                    #         card2_sprite.card_active = False
                    #         card2_sprite.played = True
                    
                    # if card3_sprite.card_active:
                    #     if card3_sprite.x + 5 < pos[0] < card3_sprite.x + 80 and card3_sprite.y + 90 <= pos[1] < card3_sprite.y + 110:
                    #         print('Attack' + str(card3_sprite.attack))
                    #         card3_sprite.card_active = False
                    #         card3_sprite.played = True
                    #     if card3_sprite.x + 5 < pos[0] < card3_sprite.x + 80 and card3_sprite.y + 110 <= pos[1] <= card3_sprite.y + 130:
                    #         print('Defense' + str(card3_sprite.defence))
                    #         card3_sprite.card_active = False
                    #         card3_sprite.played = True
                    if card1_sprite.card_active:
                        if attack_button.collidepoint(pos):
                            print('Attack' + str(card1_sprite.attack))
                            card1_sprite.played = True
                            card1_sprite.card_active = False

                        if defense_button.collidepoint(pos):
                            print('Defense' + str(card1_sprite.defence))
                            card1_sprite.played = True
                            card1_sprite.card_active = False

                    if card2_sprite.card_active:
                        if attack_button.collidepoint(pos):
                            print('Attack' + str(card2_sprite.attack))
                            card2_sprite.played = True
                            card2_sprite.card_active = False

                        if defense_button.collidepoint(pos):
                            print('Defense' + str(card2_sprite.defence))
                            card2_sprite.played = True
                            card2_sprite.card_active = False

                    if card3_sprite.card_active:
                        if attack_button.collidepoint(pos):
                            print('Attack' + str(card3_sprite.attack))
                            card3_sprite.played = True
                            card3_sprite.card_active = False

                        if defense_button.collidepoint(pos):
                            print('Defense' + str(card3_sprite.defence))
                            card3_sprite.played = True
                            card3_sprite.card_active = False

            pg.draw.rect(screen, attack_color, attack_button, 0)
            screen.blit(attack_text, (attack_button.x + 20, attack_button.y))

            pg.draw.rect(screen, defense_color, defense_button, 0)
            screen.blit(defense_text, (defense_button.x + 20, defense_button.y))

            card1_sprite.draw(screen)
            card2_sprite.draw(screen)
            card3_sprite.draw(screen)
        
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
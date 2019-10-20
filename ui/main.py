import pygame as pg
from web3 import Web3, HTTPProvider
import json 
import time
import sys
import pdb
# import
def display_text(msg, textx, texty, screen, text_color=(0, 0, 0), background_color=None):
    msgFont = pg.font.SysFont('Comic Sans MS', 15)
    textSurface = msgFont.render(msg, True, text_color, background_color)
    textRect = textSurface.get_rect()
    textRect.center = (textx, texty)
    screen.blit(textSurface, textRect)

class  Card:
    def __init__(self, uid, name, image, attack, defence):
        self.id = uid
        self.name = name
        self.image = image
        self.attack = attack
        self.defence = defence
class CardSprite(pg.sprite.Sprite):
    def __init__(self, card, x = 0, y = 0):
        pg.sprite.Sprite.__init__(self)
        self.card = card
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
        
def get_cards(twinst, account):
    card_list = twinst.functions.getMyCards().call({"from": account})
    card_class_list = []
    all_card_sprites =[]

    start_x = 190
    start_y = 50
    i = 0

    for card in card_list:
        temp = twinst.functions.getCardById(card).call({"from": account})
        card_class_list.append(Card(card, temp[0], temp[1], temp[2], temp[3]))

    for card in card_class_list:
        if i < 3:
            all_card_sprites.append(CardSprite(card, start_x + i*110, start_y))
        else:
            all_card_sprites.append(CardSprite(card, start_x + (i-3)*110, start_y + 200))
        i = i + 1
    
    return card_list, card_class_list, all_card_sprites

def main(player):

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
    #####################################################
    w3 = Web3(HTTPProvider('http://localhost:8545'))
    print(w3.isConnected())
    if player == "0":
        print("0")
        account = "0x14b6f74d70931DFF8fBc33bbAEc6608D14E70949"
    else:
        print("1")
        account = "0xf98AE10Df6ea8946B02D5EA8d404971a8F614356"


    addr = "0xe1F73982eD697f41Ac6CDCB8421098B3dd011019"
    with open('TradeWars.json') as f:
        ABI = json.load(f)
    twinst = w3.eth.contract(address=addr, abi=ABI) 
    #####################################################

    # card1=Card("new", "blank.png", 10,10)
    # card2=Card("new1", "blank.png", 20,20)
    # card3 = Card("new2", "blank.png", 30, 30)
    
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


    wait_button = pg.Rect(270, 230, 100, 20)
    wait_text = myfont.render('WAITING', False, (255, 255, 255))
    wait_color = red_color
    # all_cards = []
    # for i in range(0,6):
    #     all_cards.append(card1)
    all_cards = []
    all_cards_class = []
    all_card_sprites = []
    turn = 0
    selected_cards = []
    selected_card = 0
    gamestatusfilter = twinst.events.GameStatus.createFilter(fromBlock="latest", argument_filters={"numPlayers":2})
    # gamestatusfilter = twinst.events.GameStatus.createFilter(fromBlock="latest")
    turnfilter = twinst.events.Turn.createFilter(fromBlock="latest")
    winfilter = twinst.events.Win.createFilter(fromBlock="latest")
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
                            card1_sprite.card_active = False
                            card2_sprite = selected_cards[1]
                            card2_sprite.x = 300
                            card2_sprite.y = 300
                            card2_sprite.highlight = False
                            card2_sprite.card_active = False
                            card3_sprite = selected_cards[2]
                            card3_sprite.x = 410
                            card3_sprite.y = 300
                            card3_sprite.card_active = False
                            card3_sprite.highlight = False
                            game_state = "waiting"
                            selectedcardids=[]
                            for card in selected_cards:
                                selectedcardids.append(card.card.id)
                            print(selectedcardids)
                            # pdb.set_trace()
                            twinst.functions.join(selectedcardids).transact({"from": account})
                        else:
                            selected_cards = []
                        print(selected_cards)
            screen.fill((30, 30, 30))
            for card_sprite in all_card_sprites:
                card_sprite.draw(screen)
            pg.draw.rect(screen, defense_color, join_button, 0)
            screen.blit(join_text, (join_button.x + 20, join_button.y))
        if game_state == "waiting":
            screen.fill((30,30,30))
            pg.draw.rect(screen, wait_color, wait_button, 0)
            screen.blit(wait_text, (wait_button.x, wait_button.y))
            defense_color = red_color
            pg.display.flip()
            while(True):
                for event in gamestatusfilter.get_new_entries():
                    print(event)
                    game_state = "display_cards" 
                if (game_state == "display_cards"):
                    break
                time.sleep(1)
                # time.sleep(10000)
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
                        all_cards, all_cards_class, all_card_sprites = get_cards(twinst, account)
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
            # screen.fill((30, 30, 30))
            # card1_sprite.draw(screen)
            pg.display.flip()
            while(True):
                for event in turnfilter.get_new_entries():
                    print(event)
                    if(event.player == account):
                        turn = event.turn
                        break
                if (event.player == account):
                    break
                time.sleep(1)

            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    selected_card = twinst.functions.selectCard().call({"from":account})
                    twinst.functions.selectCard().transact({"from":account})
                    pos = pg.mouse.get_pos()
                    print(selected_card)
                    if(card1_sprite.card.id == selected_card):
                        card1_sprite.card_active = True
                    if(card2_sprite.card.id == selected_card):
                        card2_sprite.card_active = True
                    if(card3_sprite.card.id == selected_card):
                        card3_sprite.card_active = True
                    if(turn == 0):
                        game_state = "attack_defence"
                    else:
                        game_state = "checkwin"
                    # if card1_sprite.x < pos[0] < card1_sprite.x + 100 and card1_sprite.y < pos[1] < card1_sprite.y + 150:
                    #     card1_sprite.card_active = True
                    # if card2_sprite.x < pos[0] < card2_sprite.x + 100 and card2_sprite.y < pos[1] < card2_sprite.y + 150:
                    #     card2_sprite.card_active = True
                    # if card3_sprite.x < pos[0] < card3_sprite.x + 100 and card3_sprite.y < pos[1] < card3_sprite.y + 150:
                    #     card3_sprite.card_active = True
                    
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
                    # if card1_sprite.card_active:
                    #     if attack_button.collidepoint(pos):
                    #         print('Attack' + str(card1_sprite.attack))
                    #         card1_sprite.played = True
                    #         card1_sprite.card_active = False

                    #     if defense_button.collidepoint(pos):
                    #         print('Defense' + str(card1_sprite.defence))
                    #         card1_sprite.played = True
                    #         card1_sprite.card_active = False

                    # if card2_sprite.card_active:
                    #     if attack_button.collidepoint(pos):
                    #         print('Attack' + str(card2_sprite.attack))
                    #         card2_sprite.played = True
                    #         card2_sprite.card_active = False

                    #     if defense_button.collidepoint(pos):
                    #         print('Defense' + str(card2_sprite.defence))
                    #         card2_sprite.played = True
                    #         card2_sprite.card_active = False

                    # if card3_sprite.card_active:
                    #     if attack_button.collidepoint(pos):
                    #         print('Attack' + str(card3_sprite.attack))
                    #         card3_sprite.played = True
                    #         card3_sprite.card_active = False

                    #     if defense_button.collidepoint(pos):
                    #         print('Defense' + str(card3_sprite.defence))
                    #         card3_sprite.played = True
                    #         card3_sprite.card_active = False

            pg.draw.rect(screen, attack_color, attack_button, 0)
            screen.blit(attack_text, (attack_button.x + 20, attack_button.y))

            pg.draw.rect(screen, defense_color, defense_button, 0)
            screen.blit(defense_text, (defense_button.x + 20, defense_button.y))

            card1_sprite.draw(screen)
            card2_sprite.draw(screen)
            card3_sprite.draw(screen)
        if game_state == "attack_defence":
            for event in events:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if attack_button.collidepoint(pos):
                        attri = 0
                        print('Attack')
                    else if defense_button.collidepoint(pos):
                        attri = 1
                        print('Defense')
                    if(card1_sprite.card.id == selected_card)
                        card1_sprite.played = True
                    if(card2_sprite.card.id == selected_card)
                        card2_sprite.played = True
                    if(card3_sprite.card.id == selected_card)
                        card3_sprite.played = True
                    game_state = "waitwin"
                    twinst.functions.chooseAttribute(attri).transact({"from":account});
            pg.draw.rect(screen, attack_color, attack_button, 0)
            screen.blit(attack_text, (attack_button.x + 20, attack_button.y))

            pg.draw.rect(screen, defense_color, defense_button, 0)
            screen.blit(defense_text, (defense_button.x + 20, defense_button.y))

            card1_sprite.draw(screen)
            card2_sprite.draw(screen)
            card3_sprite.draw(screen)
        if game_state == "checkwin":
            if(card1_sprite.card.id == selected_card)
                card1_sprite.played = True
            if(card2_sprite.card.id == selected_card)
                card2_sprite.played = True
            if(card3_sprite.card.id == selected_card)
                card3_sprite.played = True
            twinst.functions.checkWin().transact({"from":account});
            game_state = "waitwin"
        if game_state == "waitwin":
            pg.display.flip()
            while(True):
                for event in winfilter.get_new_entries():
                    print(event)
                    game_state = "display_cards"
                if(game_state == "display_cards"):
                    break
                time.sleep(1)
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
    print(sys.argv[1])
    main(sys.argv[1])
    pg.quit()
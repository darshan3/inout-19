pragma solidity ^0.5.8;

import "../node_modules/openzeppelin-solidity/contracts/math/SafeMath.sol";

contract TradeWars {
    using SafeMath for uint;

    struct Card {
        string image;
        uint attack;
        uint defence;
        string name;
    }
    
    mapping(uint => Card) public cards; // mapping from card id to card
    mapping(uint => address) private owner;

    uint status;
    address player1;
    address player2;
    uint[] player1_cards;
    uint[] player2_cards;
    uint player1_selected_card;
    uint player2_selected_card;
    uint numPlayers;
    uint turn = 0;
    uint currAttribute;
    address currPlayer;

    event GameStatus(uint status, address joiningPlayer, uint numPlayers);
    event Turn(address player);

    constructor() public {
        status = 0;
        turn = 1;
    }

    function join(uint[] memory selectedcards) public {
        require(status == 0);
        require(selectedcards.length == 3);
        if(numPlayers == 0){
            player1 = msg.sender;
            numPlayers +=1;
            for(uint i=0; i<3; i++){
                player1_cards.push(selectedcards[i]);
            }
            emit GameStatus(status, msg.sender, numPlayers);
        }
        else if(numPlayers == 1){
            player2 = msg.sender;
            numPlayers +=1;
            for(uint i=0; i<3; i++){
                player2_cards.push(selectedcards[i]);
            }
            status == 1;
            emit GameStatus(status, msg.sender, numPlayers);
            start();
        }
    }

    function start() private {
        turn = (turn+1)%2;
        if(turn == 1){
            currPlayer = player2;
            emit Turn(currPlayer);
        }
        else{
            currPlayer = player1;
            emit Turn(currPlayer);
        }
    }

    function selectCard() public returns (uint) {
        require(status == 1);
        require(msg.sender == currPlayer);
        if(msg.sender == player1 && player1_cards.length > 0){
            uint random_number = uint(blockhash(block.number-1))%(player1_cards.length);
            player1_selected_card = player1_cards[random_number];
            player1_cards[random_number] = player1_cards.length - 1;
            delete player1_cards[player1_cards.length - 1];
            player1_cards.length--;
            return player1_selected_card;
        }
        if(msg.sender == player2 && player2_cards.length > 0){
            uint random_number = uint(blockhash(block.number-1))%(player2_cards.length);
            player2_selected_card = player2_cards[random_number];
            player2_cards[random_number] = player2_cards.length - 1;
            delete player2_cards[player2_cards.length - 1];
            player2_cards.length--;
            return player2_selected_card;
        }
    }

    function chooseAttribute(uint i) public {
        require(status == 1);
        require(msg.sender == currPlayer);
        require(turn == 0);
        require(i<=1);
        currAttribute = i;
        turn+=1;
        if(msg.sender == player1)
            currPlayer = player2;
        else
            currPlayer = player1;
    }

    function checkWin() public {
        require(status == 1);
        require(turn == 1);
        if(currAttribute == 0)
            if(cards[player1_selected_card].attack > cards[player2_selected_card].attack)
                owner[player2_selected_card] = player1;
            else
                owner[player1_selected_card] = player1;
        else
            if(cards[player1_selected_card].defence > cards[player2_selected_card].defence)
                owner[player2_selected_card] = player1;
            else
                owner[player1_selected_card] = player2;
        start();
    }


}
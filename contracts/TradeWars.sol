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
    uint[] public cardIDs;

    uint status;
    address player1;
    address player2;
    uint[] player1_cards;
    uint[] player2_cards;
    uint[] my_cards;
    uint player1_selected_card;
    uint player2_selected_card;
    uint numPlayers;
    uint turn = 0;
    uint currAttribute;
    address currPlayer;

    event GameStatus(uint status, address joiningPlayer, uint numPlayers);
    event Turn(address player);
    event Win(address winner, uint card1, uint card2);

    constructor() public {
        status = 0;
        turn = 1;
    }

    function getMyCards() external returns (uint[] memory) {
        uint[] memory tmp_my_cards;
        my_cards = tmp_my_cards;
        for(uint i = 0; i<cardIDs.length; i++){
            if(owner[cardIDs[i]] == msg.sender)
                my_cards.push(cardIDs[i]);
        }

        return my_cards;
    }

    function getCardById(uint cardId) public view returns (string memory, string memory, uint, uint){
        require(owner[cardId] == msg.sender, "You do not own this card");
        Card memory card = cards[cardId];
        return(card.name, card.image, card.attack, card.defence);
    }

    function join(uint[] calldata selectedcards) external {
        require(status == 0, "status 0");
        require(selectedcards.length == 3, "3 cards");
        if(numPlayers == 0){
            player1 = msg.sender;
            numPlayers += 1;
            for(uint i = 0; i<3; i++){
                player1_cards.push(selectedcards[i]);
            }
            emit GameStatus(status, msg.sender, numPlayers);
            currPlayer = msg.sender;
        }
        else if(numPlayers == 1){
            player2 = msg.sender;
            numPlayers += 1;
            for(uint i = 0; i<3; i++){
                player2_cards.push(selectedcards[i]);
            }
            status = 1;
            emit GameStatus(status, msg.sender, numPlayers);
            start();
        }
    }

    function start() private {
        turn = (turn+1)%2;
        emit Turn(currPlayer);
    }

    function selectCard() external returns (uint) {
        require(status == 1, "status 1");
        require(msg.sender == currPlayer, "sender should be curr player");
        if(msg.sender == player1 && player1_cards.length > 0){
            uint random_number = uint((now)%(player1_cards.length));
            player1_selected_card = player1_cards[random_number];
            player1_cards[random_number] = player1_cards.length - 1;
            delete player1_cards[player1_cards.length - 1];
            player1_cards.length--;
            return player1_selected_card;
        }
        if(msg.sender == player2 && player2_cards.length > 0){
            uint random_number = uint((now)%(player2_cards.length));
            player2_selected_card = player2_cards[random_number];
            player2_cards[random_number] = player2_cards.length - 1;
            delete player2_cards[player2_cards.length - 1];
            player2_cards.length--;
            return player2_selected_card;
        }
    }

    function chooseAttribute(uint i) external {
        require(status == 1, "status 1");
        require(msg.sender == currPlayer, "sender should be curr player");
        require(turn == 0, "not your turn");
        require(i <= 1, "2 attrs");
        currAttribute = i;
        turn += 1;
        if(msg.sender == player1)
            currPlayer = player2;
        else
            currPlayer = player1;
        emit Turn(currPlayer);

    }

    function checkWin() external {
        require(status == 1, "status 1");
        require(turn == 1, "turn=1");
        address winner;

        if(currAttribute == 0)
            if(cards[player1_selected_card].attack > cards[player2_selected_card].attack)
                winner = player1;
            else
                winner = player2;
        else
            if(cards[player1_selected_card].defence > cards[player2_selected_card].defence)
                winner = player1;
            else
                winner = player2;

        owner[player1_selected_card] = winner;
        owner[player2_selected_card] = winner;
        
        emit Win(winner, player1_selected_card, player2_selected_card);
        currPlayer = winner;
        start();
    }

    function addCard(string memory _name, string memory _image, uint _attack, uint _defence) public returns (uint) {
        uint _listingHash = uint(keccak256(abi.encode(_name, _attack, _defence)));

        cards[_listingHash] = Card({
            name: _name,
            image: _image,
            attack: _attack,
            defence: _defence
        });
        
        owner[_listingHash] = msg.sender;
        cardIDs.push(_listingHash);
        return _listingHash;
    }

}
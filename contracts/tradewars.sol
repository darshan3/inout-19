pragma solidity >=0.4.21 <0.6.0;

import "../node_modules/openzeppelin-solidity/contracts/math/SafeMath.sol";

contract TradeWars {
    using SafeMath for uint;

    struct Card {
        string image;
        uint attr1;
        uint attr2;
        string name;
    }
    mapping(uint => Card) public cards; // mapping from card id to card
    mapping(uint => address) private owner;


    constructor() public {

    }

    function join()








}
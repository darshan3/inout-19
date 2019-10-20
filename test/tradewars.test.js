var tradewars = artifacts.require("TradeWars");

contract('TradeWars', async function (accounts) {
    let twinst;
    before(async() => {
        twinst = await tradewars.deployed();

        
        // assert.equal(cards.length, 3, "All cards not alloted to 1");
        // const twAddr = await twinst.
    });


    // getMyCards
    // join with 3 cards
    // choose 1 radnom card
    // play with attribute chooseAttribute
    // 2nd player chooses card.
    // 2nd player calls checkWin()
    

    it('adding cards', async function(){

        let card = await twinst.addCard.call("Card1", "Im1", 100, 100, {from: accounts[0]}) ;
        await twinst.addCard("Card1", "Im1", 100, 100, {from: accounts[0]}) ;
        console.log("card", card);
        await twinst.addCard("Card3", "Im3", 300, 300, {from: accounts[0]}) ;
        await twinst.addCard("Card5", "Im5", 500, 500, {from: accounts[0]}) ;
        
        await twinst.addCard("Card2", "Im2", 200, 200, {from: accounts[1]}) ;
        await twinst.addCard("Card4", "Im4", 400, 400, {from: accounts[1]}) ;
        await twinst.addCard("Card6", "Im6", 600, 600, {from: accounts[1]}) ;

        const card1 = await twinst.cards.call(card);
        console.log(card1);
        const card2 = await twinst.getCardById.call(card, {from: accounts[0]});
        console.log(card2);
        const myCards = await twinst.getMyCards.call();
        console.log(myCards);
        const myCards2 = await twinst.getMyCards.call({from: accounts[1]});
        await twinst.join(myCards);
        await twinst.join(myCards2, {from: accounts[1]});

        let currentCard1 = await twinst.selectCard.call();
        await twinst.selectCard();
        console.log(await twinst.getCardById.call(currentCard1, {from: accounts[0]}));

        await twinst.chooseAttribute(0);

        let currentCard2 = await twinst.selectCard.call({from: accounts[1]});
        await twinst.selectCard({from: accounts[1]});
        console.log(await twinst.getCardById.call(currentCard2, {from: accounts[1]}));

        await twinst.checkWin();




        
    })
    // it("should init name", async function () {
    //     const status = await twinst.status;
    //     assert.equal(status, 0, "status didnt initialize");
    // });
    it('init', async function(){
        // const cards2 = await twinst.getMyCards({from:accounts[1]});
        // console.log("account 2\n" ,cards2);   
        // assert.equal(cards2.length, 3, "All cards not alloted to 2");
    });

    

})
var tcr = artifacts.require("Tcr");
var token = artifacts.require("Token");
var twar = artifacts.require("TradeWars");

module.exports = function(deployer) {
  deployer.deploy(tcr, "DemoTcr", token.address, twar.address, [100, 60, 60]);
};
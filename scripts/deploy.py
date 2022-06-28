from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account, 
    deploy_mocks, 
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

def deploy_fund_me():
    account = get_account()
    
    # if on persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks 
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        # This uses the most recently deployed MockV3Aggregator
        price_feed_address = MockV3Aggregator[-1].address

    # since it makes a state change, you need "from"
    fund_me = FundMe.deploy(
        price_feed_address, 
        {"from": account},
        # Since it can't verify when we deploy locally, we do this verify programatically 
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()
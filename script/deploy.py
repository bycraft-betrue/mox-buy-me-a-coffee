from moccasin.config import get_active_network
from src import buy_me_a_coffee
from script.deploy_mocks import deploy_feed
from moccasin.boa_tools import VyperContract

def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    print("Deploying coffee...")
    coffee: VyperContract = buy_me_a_coffee.deploy(price_feed)
    print(f"Coffee deployed at {coffee.address}")

    active_network = get_active_network()
    if active_network.has_explorer() and active_network.is_local_or_forked_network is False:
        print("Verification ongoing!")
        result = active_network.moccasin_verify(coffee)
        result.wait_for_verification()
    return coffee



def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    # price_feed: VyperContract = deploy_feed() # just getting a mock address to test deploy 
    # this way moccasin will know whether to use sepolia price feed or mock price feed
    # without manually changing the price feed address in the script with if-elses
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"On network {active_network.name}")
    print(f"Using price feed at {price_feed.address}")
    return deploy_coffee(price_feed)
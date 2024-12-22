from eth_utils import to_wei
import boa
import random
from tests.conftest import SEND_VALUE

RANDOM_USER = boa.env.generate_address("non-owner")
# Initialize an empty array of strings with length 10
RANDOM_USERS = [""] * 10
for i in range(10):
    RANDOM_USERS[i] = boa.env.generate_address("non-owner")

RANDOM_VALUES = [0] * 10
for i in range(10):
    RANDOM_VALUES[i] = to_wei(random.randint(1, 3), "ether")

def test_price_feed_is_correct(coffee, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address

def test_starting_values(coffee, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffee):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()

def test_fund_with_money(coffee, account):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    # typically you want to avert two asserts in one test
    assert account.address == coffee.funders(0)
    assert coffee.funder_to_amount_funded(coffee.funders(0)) == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded, account):
    # Act & Assert
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded):
    # Act
    with boa.env.prank(coffee_funded.OWNER()):
        coffee_funded.withdraw()
    # Assert
    assert boa.env.get_balance(coffee_funded.address) == 0

def test_10_people_can_fund(coffee):
    # Arrange
    for i in range(10):
        boa.env.set_balance(RANDOM_USERS[i], RANDOM_VALUES[i])

    # Act
    for i in range(10):
        with boa.env.prank(RANDOM_USERS[i]):
            coffee.fund(value=RANDOM_VALUES[i])
    
    starting_fund_me_balance = boa.env.get_balance(coffee.address)
    starting_owner_balance = boa.env.get_balance(coffee.OWNER())

    with boa.env.prank(coffee.OWNER()):
        coffee.withdraw()

    # Assert
    assert boa.env.get_balance(coffee.address) == 0
    assert boa.env.get_balance(coffee.OWNER()) == starting_fund_me_balance + starting_owner_balance


def test_get_rate(coffee):
    assert coffee.get_eth_to_usd_rate(SEND_VALUE) > 0


# This file is part of Maker Keeper Framework.
#
# Copyright (C) 2017 reverendus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from web3 import EthereumTesterProvider
from web3 import Web3

from api import Address
from api.numeric import Wad
from api.token import DSToken


class TestERC20Token:
    def setup_method(self):
        self.web3 = Web3(EthereumTesterProvider())
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        self.token = DSToken.deploy(self.web3, ['ABC'])
        self.token.mint(Wad(1000000))
        self.our_address = Address(self.web3.eth.defaultAccount)
        self.second_address = Address(self.web3.eth.accounts[1])

    def test_total_supply(self):
        self.token.total_supply() == Wad(1000000)

    def test_balance_of(self):
        self.token.balance_of(self.our_address) == Wad(1000000)
        self.token.balance_of(self.second_address) == Wad(0)

    def test_transfer(self):
        # when
        self.token.transfer(self.second_address, Wad(500))

        # then
        self.token.balance_of(self.our_address) == Wad(999500)
        self.token.balance_of(self.second_address) == Wad(500)


class TestDSToken:
    def setup_method(self):
        self.web3 = Web3(EthereumTesterProvider())
        self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
        self.dstoken = DSToken.deploy(self.web3, ['ABC'])
        self.our_address = Address(self.web3.eth.defaultAccount)

    def test_mint(self):
        # when
        self.dstoken.mint(Wad(100000))

        # then
        assert self.dstoken.balance_of(self.our_address) == Wad(100000)

    def test_burn(self):
        # given
        self.dstoken.mint(Wad(100000))

        # when
        self.dstoken.burn(Wad(40000))

        # then
        assert self.dstoken.balance_of(self.our_address) == Wad(60000)
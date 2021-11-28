import json

from config import Config

class Balance:
    """ Balance manager -> increase - decrease and persistance balance  based on public key """

    balances = []

    def __init__(self):
        self.load_balances()

    def persistance_balance(self) -> None:
        """ Load balance """
        with open(Config.WALLET_BALANCE_FILE_NAME, "w") as file:
            json.dumps(self.balances, file)
        file.close()

    def load_balances(self) -> None:
        """ Persistance balance to file """
        with open(Config.WALLET_BALANCE_FILE_NAME, "r") as file:
            if file:
                try:
                    self.transactions = json.load(file)
                except:
                    self.transactions = []
        file.close()

    def increase_wallet_balance(self, public_key: str, amount)-> None:
        wallet = {
            "public_key": public_key,
            "balance": amount
        }
        data = json.dump(wallet)
        self.balances.append(data)


    def decrease_wallet_balance(self, public_key: str, amount)-> None:
        """ Decrease wallet balance """
        wallet = {
            "public_key": public_key,
            "balance": amount
        }
        data = json.dump(wallet)
        self.balances.append(data)

    def get_balance(self, public_key) :
        """ Get balance """
        try:
            return self.balances[public_key]
        except:
            return 0

    def update_balance(self, sender, recipient, amount, fee) -> None:
        """ Update balance """

        self.increase_wallet_balance(recipient, amount)
        self.decrease_wallet_balance(sender, amount + fee)
        print(self.balances)
        self.persistance_balance()
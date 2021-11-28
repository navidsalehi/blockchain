import hashlib
import json

class Transaction:
    """ Transaction manager new - list - detail """
    def __init__(self, sender, recipient, amount):
        pass

    def create_transaction(self, sender, recipient, amount):
        """ Create a new transaction """
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_id = self.generate_transaction_id()
        self.sign_transaction(sender.private_key)

    def generate_transaction_id(self):
        """ Generate a unique id for the transaction """
        return hashlib.sha256((str(self.sender) + str(self.recipient) + str(self.amount)).encode()).hexdigest()

    def to_json(self):
        """ Serialize the transaction to a json object """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def sign_transaction(self, private_key):
        """ Sign the transaction with the private key """
        self.signature = self.generate_signature(private_key)

    def generate_signature(self, private_key):
        """ Generate a signature for the transaction """
        return private_key.sign(self.transaction_id.encode())

    def verify_transaction(self):
        """ Verify the signature of the transaction """
        return self.sender.verify(self.signature, self.transaction_id.encode())

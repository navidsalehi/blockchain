import requests

class Node:
    """ 
    Blockchain nodes manager
    add - update - check status - brodcast transaction and sync between nodes
    """

    def __init__(self, port, host, node_id):
        self.port = port
        self.host = host
        self.node_id = node_id
        self.nodes = set()
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, node):
        """
        Add a new node to the list of nodes
        """
        self.nodes.add(node)
    
    def reslove_conflicts(self, node):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        """
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False
    
    def delete_node(self, node):
        """
        :param node: Node to be deleted
        :return:
        """
        self.nodes.remove(node)

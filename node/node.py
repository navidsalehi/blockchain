import requests
import json
import requests

from config import Config


class Node:
    """
    Blockchain nodes manager
    add - update - check status - brodcast transaction and sync between nodes
    system will check node status every 10 miniutes
    node will be deleted if it is not responding after 3 attempts
    """

    nodes = []

    def __init__(self):
        """
        Initialize blockchain
        """
        self.nodes = set()
        self.load_nodes()

    def register_node(self, name: str, host: str, port: int)-> bool:
        """
        Add a new node to the list of nodes
        """
        node = {
            "name": name, 
            "port": port, 
            "host": host,
            "attempt" : 0
        }
        self.load_nodes()
        if node not in self.nodes:
            self.nodes.append(node)
            self.persistant_nodes()
            # self.brodcast_new_node(node)
            return True
        else:
            return False


    def reslove_conflicts(self, node):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        """
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")

            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def load_nodes(self):
        """Load nodes from node list file"""
        with open(Config.NODE_LIST_FILE_NAME, "r") as file:
            if file:
                try:
                    self.nodes = json.load(file)
                except:
                    self.nodes = []
        file.close()


    def persistant_nodes(self):
        """Persistant nodes to nodes.json"""
        with open(Config().NODE_LIST_FILE_NAME, "w") as file:
            json.dump(list(self.nodes), file)
        file.close()

    def check_node_status(self, node):
        """
        Check node health
        if node is not responding, increase attempt 
        and delete node if attempt is more than 3
        """
        node_url = f"http://{node['host']}:{node['port']}/node/status"
        r = requests.get(node_url)
        if r.status_code == 200:
            return True
        else:
            self.nodes.update(node, attempt=node['attempt']+1)
            self.persistant_nodes()
        
        if node['attempt'] > 3:
            self.nodes.remove(node)
            self.persistant_nodes()

    def brodcast_new_node(self, node):
        """Brodcast new node to all registered nodes """
        for n in self.nodes:
            requests.post(f"http://{n['host']}:{n['port']}/node/register", json=node)
        
    def brodcast_new_transaction(self, transaction):
        """Brodcast new transaction to all registered nodes """
        for n in self.nodes:
            requests.post(f"http://{n['host']}:{n['port']}/node/transaction/new", json=transaction)
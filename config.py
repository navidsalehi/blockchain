from dataclasses import dataclass

@dataclass
class Config:
    """ Blockchain configs """

    # persistence configs 
    BLOCKS_FILE_NAME = "data/blocks.json"
    MEMPOOL_FILE_NAME = "data/mempool.json"
    WALLET_BALANCE_FILE_NAME = "data/balance.json"
    SEED_WORDS_FILE_NAME = "data/seed_word_list.txt"

    # transaction configs
    TRANSACTION_FEE = 0.02
    MINING_REWARD_SENDER = "THE BLOCKCHAIN"
    MINING_REWARD_RECIPIENT = "MINING REWARD"
    MINING_REWARD = 50

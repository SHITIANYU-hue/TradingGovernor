import json

from web3 import Web3
from web3.types import LogReceipt, TxData
import logging

'''
w3: Web3 provider
log: Log receipt
tx: Transaction Data

returns: is Native Coin Event Data or not(bool), Tuple about the detail Native Coin Event Data
         Native Coin Contract is 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 
         the Native Coin Event are `Deposit` or `Withdrawal`
'''
def native_coin_filter(w3, log: LogReceipt, tx: TxData = None):
    if len(log['topics']) > 0:
        # WETH <-> ETH
        # 一条log是一条日志数据，也是一个触发的事件
        # address 存放log触发的所在合约地址
        # topics[0] 存放触发的事件的id（哈希）
        # topics[0]、[1]、[2]、[3] 存放的是事件的一些数据，topics[0]一般都有，默认是存放事件的哈希id。
        # topics数组可能不满4个，可以只有0到2，甚至一个都没有。每个topics数组的元素存放字节数组，并且一定是32个字节共256bit，高位补0，补齐256位。
        # 除了topics可以存放数据，data也可以存放数据。data存放十六进制数字（例，0x1e2b3c...7d8e9f），长度是不固定的，一般是256位（32字节）为一组进行读取，长度一般是32字节的整数倍。
        if log['address'] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' and log['topics'][0].hex() in ['0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c', '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65']:
            address_0x = '0x' + '00' * 20
            transaction_hash = log['transactionHash'].hex()
            block_number = log['blockNumber']
            pair_address = address_0x
            protocol = 'Deposit_Withdrawal'

            from_address = '0x' + log['topics'][1].hex()[26:]
            to_address = from_address
            data = log['data'].hex()
            from_amount = int(data, 16)
            to_amount = from_amount

            tx_origin = get_tx_origin(w3, transaction_hash, tx)

            # 依靠Deposit事件的哈希id进行识别
            if log['topics'][0].hex() == '0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c':  # Deposit
                to_token = log['address']
                from_token = address_0x
                # print("Deposit")
                return True, (
                    transaction_hash, block_number, from_address, to_address, str(
                        from_amount), str(to_amount),
                    from_token,
                    to_token, tx_origin, pair_address, protocol)

            # 依靠Withdrawal事件的哈希id进行识别
            elif log['topics'][0].hex() == '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65':  # Withdrawal
                from_token = log['address']
                to_token = address_0x
                # print("Withdrawal")
                return True, (
                    transaction_hash, block_number, from_address, to_address, str(
                        from_amount), str(to_amount),
                    from_token,
                    to_token, tx_origin, pair_address, protocol)

            else:
                logging.warning(
                    f"log[{log['blockNumber']}-{log['transactionHash'].hex()}-{log['logIndex']}] amount calculate error!")
                return False, ()
        else:
            return False, ()
    else:
        return False, ()


def get_tx_origin(w3, transaction_hash, tx):
    if tx is not None:
        return tx["from"]
    # 获取交易的发起者地址
    return w3.eth.get_transaction(transaction_hash)['from']


if __name__ == '__main__':
    w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/1vSGEJ78c6cVpaXsQxP3fA6D0mKVBGMs'))
    test_case = '0x115ed3f'  # block number
    logs = w3.eth.get_logs({
        'fromBlock': test_case,
        'toBlock': test_case,
    })

    for log in logs:
        (error, res) = native_coin_filter(w3, log)
        if error:
            print(res)
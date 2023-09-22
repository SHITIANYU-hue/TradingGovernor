import random
import numpy as np

# 定义一个用户交易策略类
class UserStrategy:
    def __init__(self, market_state, inflation_level, agent_states):
        self.market_state = market_state
        self.inflation_level = inflation_level
        self.agent_states = agent_states

    def update(self, market_state, inflation_level, agent_states):
        # 更新用户策略的内部状态
        self.market_state = market_state
        self.inflation_level = inflation_level
        self.agent_states = agent_states

    def choose_action(self,agent_id):
        # 基于市场状态和通货膨胀水平选择行动
        market_price = self.market_state['price']
        wealth = self.agent_states[agent_id]['wealth']

        # 选择保守或激进策略（根据通货膨胀水平）
        if self.inflation_level < -0.05:
            if market_price < 100 and wealth > 0:
                # 保守策略：如果市场价格低于100且有足够的财富，就买入
                return 1
        else:
            if market_price > 120 and wealth > 0:
                # 激进策略：如果市场价格高于120且有足够的财富，就卖出
                return -1

        # 否则，保持不动
        return 0


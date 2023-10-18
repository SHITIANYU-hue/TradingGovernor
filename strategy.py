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


class EconomicControlStrategy:
    def __init__(self, market_state, inflation_level, agent_states):
        self.market_state = market_state
        self.inflation_level = inflation_level
        self.agent_states = agent_states

    def calculate_multipliers(self):
        # 在这里根据market_state、inflation_level和agent_states等参数动态计算需求和供应的调整倍数
        # 你可以使用更复杂的逻辑来计算这些倍数，考虑更多的因素

        # 默认值为1.0，即不调整需求和供应
        demand_multiplier = 1.0  
        supply_multiplier = 1.0  

        # 根据市场价格调整需求和供应
        if self.market_state['price'] > 120:
            demand_multiplier *= 0.9  # 将需求降低到90%
            supply_multiplier *= 1.1  # 将供应增加到110%

        # 根据通货膨胀水平调整需求和供应
        if self.inflation_level > 0.05:
            demand_multiplier *= 0.8  # 将需求降低到80%
            supply_multiplier *= 1.2  # 将供应增加到120%

        # 根据智能体的财富状况调整需求和供应
        for agent_state in self.agent_states:
            wealth = agent_state['wealth']
            if wealth < 800:
                demand_multiplier *= 1.2  # 将需求增加到120%
            elif wealth > 1200:
                supply_multiplier *= 0.8  # 将供应降低到80%

        # 更复杂的逻辑可以根据需要添加

        return demand_multiplier, supply_multiplier
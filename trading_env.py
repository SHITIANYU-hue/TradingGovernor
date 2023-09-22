import random
import numpy as np
import pandas as pd

class MultiAgentTradingEnv:
    def __init__(self, num_agents, obs_data_len, step_len, df, fee, max_position=5, deal_col_name='Price'):
        self.num_agents = num_agents
        self.obs_data_len = obs_data_len
        self.step_len = step_len
        self.df = df
        self.fee = fee
        self.max_position = max_position
        self.deal_col_name = deal_col_name
        self.inflation_level = 0.0  # 初始通货膨胀水平设为0
        self.reset()

    def reset(self):
        # 初始化市场状态和智能体状态
        self.market_state = {
            'price': 100,  # 初始市场价格
            'demand': 0,
            'supply': 0,
            'money_supply': 1000,  # 初始货币供应量
            'date': self.df['date'][0],  # 初始日期
            'high': self.df['high'][0],  # 初始最高价
            'low': self.df['low'][0],    # 初始最低价
            'open': self.df['open'][0],  # 初始开盘价
            'close': self.df['close'][0]  # 初始收盘价
        }
        self.agent_states = [{'position': 0, 'wealth': 1000} for _ in range(self.num_agents)]

    def step(self, actions):
        # 根据智能体的行动计算总需求和总供应
        total_demand = sum(actions[:self.num_agents])
        total_supply = sum(actions[self.num_agents:])

        # 更新市场状态
        self.market_state['demand'] = total_demand
        self.market_state['supply'] = total_supply

        # 基于需求和供应更新市场价格
        # 可以根据算法来计算市场价格变化，例如，从DataFrame中获取实际价格并应用一些逻辑
        # 这里使用示例中的简单算法
        price_change = (total_demand - total_supply) * 0.1
        self.market_state['price'] += price_change

        # 在这里更新日期和其他市场属性
        current_index = self.df[self.df['date'] == self.market_state['date']].index[0]
        next_index = current_index + 1
        if next_index < len(self.df):
            self.market_state['date'] = self.df['date'][next_index]
            self.market_state['high'] = self.df['high'][next_index]
            self.market_state['low'] = self.df['low'][next_index]
            self.market_state['open'] = self.df['open'][next_index]
            self.market_state['close'] = self.df['close'][next_index]


        # 计算通货膨胀率
        inflation_rate = price_change / self.market_state['price']

        # 更新通货膨胀水平
        self.inflation_level += inflation_rate

        # 计算货币供应变化
        money_supply_change = price_change * 10
        self.market_state['money_supply'] += money_supply_change

        # 执行智能体的行动
        rewards = []
        for i in range(self.num_agents):
            position = self.agent_states[i]['position']
            action = actions[i]

            if action == 1 and position < self.max_position:
                position += 1
                reward = (self.market_state['price'] - 100) * position - self.fee
            elif action == -1 and position > -self.max_position:
                position -= 1
                reward = (100 - self.market_state['price']) * position - self.fee
            else:
                reward = 0

            # 计算税收
            tax = 0.1 * reward
            reward -= tax

            # 基于奖励和价格变化更新智能体的财富
            self.agent_states[i]['position'] = position
            self.agent_states[i]['wealth'] += reward + money_supply_change

            rewards.append(reward)

        # 创建观察和完成标志（仅用于演示的简化版本）
        observations = [self.market_state[attr] for attr in self.market_state.keys()] + [a['position'] for a in self.agent_states]
        done = False

        return observations, rewards, done



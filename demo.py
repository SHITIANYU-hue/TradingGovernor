
import pandas as pd
import numpy as np
import random
# 创建一个示例DataFrame
num_rows = 1000  # 假设有1000行数据 (这个数据的格式参考的NTU的trading master 论文：https://drive.google.com/drive/folders/1R9FJc6QAXXhMdW4AsJkPiyTPGAN_sNtw)
data = {
    'tic': ['BTC'] * num_rows,
    'date': pd.date_range(start='2013-04-29 23:59:59', periods=num_rows, freq='D'),
    'high': np.random.uniform(80, 150, num_rows),
    'low': np.random.uniform(70, 130, num_rows),
    'open': np.random.uniform(75, 140, num_rows),
    'close': np.random.uniform(75, 140, num_rows),
    'adjcp': np.random.uniform(70, 150, num_rows),
    'zopen': np.random.uniform(-0.1, 0.1, num_rows),
    'zhigh': np.random.uniform(-0.1, 0.1, num_rows),
    'zlow': np.random.uniform(-0.1, 0.1, num_rows),
    'zadjcp': np.random.uniform(-0.1, 0.1, num_rows),
    'zclose': np.random.uniform(-0.1, 0.1, num_rows),
    'zd_5': np.random.uniform(-0.2, 0.2, num_rows),
    'zd_10': np.random.uniform(-0.2, 0.2, num_rows),
    'zd_15': np.random.uniform(-0.2, 0.2, num_rows),
    'zd_20': np.random.uniform(-0.2, 0.2, num_rows),
    'zd_25': np.random.uniform(-0.2, 0.2, num_rows),
    'zd_30': np.random.uniform(-0.2, 0.2, num_rows)
}

df = pd.DataFrame(data)

# 创建环境
from trading_env import MultiAgentTradingEnv
from strategy import UserStrategy, EconomicControlStrategy
num_agents = 10  # 假设有10个智能体
obs_data_len = 256
step_len = 128
fee = 0.1
max_position = 5
deal_col_name = 'close'  # 使用'close'列作为交易价格

env = MultiAgentTradingEnv(num_agents, obs_data_len, step_len, df, fee, max_position, deal_col_name)

# 现在，可以使用这个环境来模拟交易，智能体可以访问和使用df中的特征数据
# 创建环境
# 用于演示的用户策略列表
# 创建用户策略列表时传递market_state和inflation_level参数
# 运行模拟
for _ in range(10):
    # 创建用户策略列表时传递market_state和inflation_level参数
    user_strategies = [UserStrategy(env.market_state, env.inflation_level, env.agent_states) for _ in range(num_agents)]
    user_actions = []  # 存储每个代理的行动
    for agent_id in range(num_agents):
        # 为每个代理调用update方法，传递新的观测值
        user_strategies[agent_id].update(env.market_state, env.inflation_level, env.agent_states)
        
        # 为每个代理选择用户策略行动
        user_action = user_strategies[agent_id].choose_action(agent_id)
        user_actions.append(user_action)
    print('strategy',user_actions)
    strategy=EconomicControlStrategy(env.market_state, env.inflation_level, env.agent_states).calculate_multipliers()
    print('economic strategy',strategy)
    # 运行环境并输出结果
    observations, rewards, done = env.step(user_actions,strategy)
    print("Observations:", observations)
    print("Rewards:", rewards)
    print("Market State:", env.market_state)
    print("Agent States:", env.agent_states)
    print("通货膨胀水平:", env.inflation_level)
    print("===")


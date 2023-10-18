# TradingGovernor

## Data collect:

每一行拿出来数据分别是，交易哈希，区块号，交易的from地址，交易的to地址，from的金额，to的金额，from代币地址，to代币地址，交易的发起人，pair地址，还有协议名



## Done:

### 买家建模：


#### 买家的观测：
市场+local observation


#### 买家的收益（reward）计算：

如果买家智能体采取的行动是买入（action == 1）并且当前持仓未达到最大允许仓位（position < self.max_position），则执行以下操作：
增加买家智能体的持仓（position += 1），表示买入了一单位的资产。
计算奖励（reward）：奖励等于当前市场价格与100之间的差值乘以持仓数量（position），然后减去交易费用（self.fee）。
这个奖励的计算方式表示买家在当前价格低于100的情况下购买资产，如果价格上升，他们将获得正奖励，否则将获得负奖励。

如果买家智能体采取的行动是卖出（action == -1）并且当前持仓未达到最小允许仓位（position > -self.max_position），则执行以下操作：
减少买家智能体的持仓（position -= 1），表示卖出了一单位的资产。
计算奖励（reward）：奖励等于100与当前市场价格之间的差值乘以持仓数量（position），然后减去交易费用（self.fee）。
这个奖励的计算方式表示买家在当前价格高于100的情况下卖出资产，如果价格下降，他们将获得正奖励，否则将获得负奖励。
如果买家智能体采取的行动不是买入或卖出（action 不等于 1 且不等于 -1），则将奖励（reward）设为0，表示没有交易行为。

### 交易建模:

可以见代码批注

### 公平性建模:

考虑对买家的收益进行征税：
计算税收
tax = 0.1 * reward
reward -= tax



## 说明文档（建模思路）：

经济模型结构
市场状态（Market State）：
价格（Price）：市场上交易资产的价格。
需求（Demand）：市场上的总需求。
供应（Supply）：市场上的总供应。
货币供应量（Money Supply）：市场上的货币总量。
日期（Date）：当前市场日期。
最高价（High）：当日最高价格。
最低价（Low）：当日最低价格。
开盘价（Open）：当日开盘价格。
收盘价（Close）：当日收盘价格。
智能体状态（Agent States）：
头寸（Position）：每个智能体持有的资产数量。
财富（Wealth）：每个智能体的总财富。

模型交互
智能体行为（Agent Actions）：
买入（1）：智能体选择买入资产。
卖出（-1）：智能体选择卖出资产。
不操作（0）：智能体选择保持当前头寸。
市场响应：
智能体的买卖行为影响市场的总需求和总供应。
市场根据需求和供应的变化调整价格。
通货膨胀和货币供应：
市场价格的变化导致通货膨胀水平的调整。
通货膨胀水平影响货币供应量。

经济控制策略
经济控制输入（Economic Control Input）：
需求倍数（Demand Multiplier）：调整市场需求的倍数。
供应倍数（Supply Multiplier）：调整市场供应的倍数。
经济控制策略（Economic Control Strategy）：
根据市场状态、通货膨胀水平和智能体状态等信息，动态计算需求和供应的调整倍数。
调整倍数可以根据不同因素（例如市场价格、通货膨胀率、智能体财富等）进行动态调整，以模拟实际经济中的宏观调控。

![Alt text](figure/framework.png?raw=true "仿真框架")
![Alt text](figure/demo.png?raw=true "仿真运行效果（待优化）")




## TO DO 


1. 真实数据建模
2. 调控策略建模
3. 用户策略优化
4. 可视化

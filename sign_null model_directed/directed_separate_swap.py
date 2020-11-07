# -*- coding: utf-8 -*-
"""该模块是有向符号网络1阶零模型的构造方法之一:
   将原始网络模型，通过正负边分别随机断边重连零模型函数，生成有向符号网络1阶零模型
   
   全局声明：
       + : weight = 1
       - : weight = 2
"""


import matplotlib.pyplot as plt
import networkx as nx
import random
import copy


def sign_network_swap(G0, nswap=1, max_tries=100, paradox='false'):    
    """正负边分别随机断边重连零模型函数
    
    输入：
        G0: 原始网络模型
        nswap: 断边交换次数
        max_tries：最大尝试次数
        
    输出：
        G：按要求断边重连1阶零模型
    """
    
    G = copy.deepcopy(G0)  # 深层次拷贝，不会产生任何映射
    n = 0
    swapcount = 0
    a = dict(G.degree())  # 形成所有节点-度字典
    keys, degrees = zip(*a.items()) 
    cdf = nx.utils.cumulative_distribution(degrees)  # 由degrees求取cdf
    
    while swapcount < nswap:
        (ui, xi) = nx.utils.discrete_sequence(2, cdistribution=cdf)
    
        if ui == xi:
            continue  # 来源相同，跳过
        
        u = keys[ui]  # 转换索引标签
        x = keys[xi]
        
        # 从相邻中统一选择目标
        if len(list(G[u])) > 0 and len(list(G[x])) > 0:
            v = random.choice(list(G[u]))
            y = random.choice(list(G[x]))
            if v == y:
                continue
        else:
            continue
        
        # 该部分进行断边交换重连
        if ((paradox.lower() == 'true' and (u in G[v])) or 
            (paradox.lower() == 'true' and (x in G[y]))):
                continue
        else:
            G[u][v]['weight']
            G[x][y]['weight'] = G[x][y]['weight']
            G[u][v]['weight']
            if G[u][v]['weight'] != G[x][y]['weight']:
                swapcount += 1
                
        if n >= max_tries:
            e = ('Maximum number of swap attempts (%s) exceeded '%n 
                 + 'before desired swaps achieved (%s).'%nswap)
            print(nx.NetworkXAlgorithmError(e))
            break
        
        n += 1
        
        if n%1000000 == 0:
            print('swap times=', swapcount, 'try times=', n)
    
    return G

    
#%%  

# 计算原始网络模型并（G0）
G0 = nx.read_edgelist('filename.txt', 
                      create_using=nx.DiGraph(), nodetype=int, data=(('weight', float),))       
# 计算基于正负边分别随机断边重连的有向符号网络1阶零模型（G3）
G3 = sign_network_swap(G0, 60000, 100000)    

   
#%% 可视化

# G0可视化
# 按权重划分为正边和负边
p_edge = [(u, v) for (u, v, d) in G0.edges(data = True) if d['weight'] <= 1]
n_edge = [(u, v) for (u, v, d) in G0.edges(data = True) if d['weight'] > 1]
# 首先画出节点
pos = nx.spring_layout(G0)
nx.draw_networkx_nodes(G0, pos)
# 再分别画出正边和负边
nx.draw_networkx_edges(G0, pos, edgelist = p_edge)
nx.draw_networkx_edges(G0, pos, edgelist = n_edge, style = 'dashed')
plt.show()


# G3可视化
# 按权重划分为正边和负边
p_edge = [(u, v) for (u, v, d) in G3.edges(data = True) if d['weight'] <= 1]
n_edge = [(u, v) for (u, v, d) in G3.edges(data = True) if d['weight'] > 1]
# 首先画出节点
pos = nx.spring_layout(G3)
nx.draw_networkx_nodes(G3, pos)
# 再分别画出正边和负边
nx.draw_networkx_edges(G3, pos, edgelist = p_edge)
nx.draw_networkx_edges(G3, pos, edgelist = n_edge, style = 'dashed')
plt.show()
    

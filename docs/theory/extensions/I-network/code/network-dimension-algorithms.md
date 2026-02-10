# I1: 网络维度计算算法

## 1. 概述

复杂网络的有效维数计算方法。

## 2. 网络盒计数法 (Network Box Counting)

### 2.1 算法描述

对于网络 $G = (V, E)$，定义盒计数维度：

$$d_B^N = \lim_{\ell_B \to \infty} \frac{\log N_B(\ell_B)}{\log \ell_B}$$

其中 $N_B(\ell_B)$ 是覆盖网络所需的最小盒子数，盒子直径为 $\ell_B$。

### 2.2 贪心算法

```python
def network_box_counting(G, max_box_size):
    """
    计算网络盒计数维度
    
    Parameters:
    G: NetworkX图对象
    max_box_size: 最大盒子尺寸
    
    Returns:
    d_B: 盒计数维度
    """
    N_B_list = []
    
    for l_B in range(1, max_box_size + 1):
        # 贪心覆盖
        boxes = greedy_box_covering(G, l_B)
        N_B_list.append(len(boxes))
    
    # 线性拟合求斜率
    log_l = np.log(range(1, max_box_size + 1))
    log_N = np.log(N_B_list)
    
    slope, _ = np.polyfit(log_l, log_N, 1)
    return -slope

def greedy_box_covering(G, l_B):
    """贪心盒子覆盖算法"""
    uncovered = set(G.nodes())
    boxes = []
    
    while uncovered:
        # 选择度数最高的未覆盖节点作为盒子中心
        center = max(uncovered, key=lambda n: G.degree(n))
        
        # 创建盒子：距离center不超过l_B的所有节点
        box = set(nx.single_source_shortest_path_length(
            G, center, cutoff=l_B).keys())
        
        boxes.append(box)
        uncovered -= box
    
    return boxes
```

## 3. 网络谱维度法 (Network Spectral Dimension)

### 3.1 图拉普拉斯

对于网络 $G$，定义归一化拉普拉斯矩阵：

$$\mathcal{L}_{ij} = \delta_{ij} - \frac{A_{ij}}{\sqrt{k_i k_j}}$$

其中 $A$ 是邻接矩阵，$k_i$ 是节点 $i$ 的度。

### 3.2 谱维度计算

$$d_s^N = 2 \lim_{\lambda \to 0} \frac{\log \rho(\lambda)}{\log \lambda}$$

其中 $\rho(\lambda)$ 是态密度。

### 3.3 算法实现

```python
def network_spectral_dimension(G, num_eigenvalues=1000):
    """
    计算网络谱维度
    
    Parameters:
    G: NetworkX图对象
    num_eigenvalues: 计算的特征值数量
    
    Returns:
    d_s: 谱维度
    """
    # 计算归一化拉普拉斯
    L = nx.normalized_laplacian_matrix(G)
    
    # 计算前num_eigenvalues个特征值
    eigenvalues = scipy.sparse.linalg.eigsh(
        L, k=num_eigenvalues, which='SM', return_eigenvectors=False
    )
    
    # 取正特征值
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    
    # 拟合态密度
    log_lambda = np.log(eigenvalues)
    log_rho = np.log([compute_dos(L, lam) for lam in eigenvalues])
    
    slope, _ = np.polyfit(log_lambda, log_rho, 1)
    return 2 * slope

def compute_dos(eigenvalues, lambda_val, sigma=0.01):
    """计算态密度 (高斯展宽)"""
    dos = np.sum(np.exp(-((eigenvalues - lambda_val) / sigma)**2))
    return dos / (len(eigenvalues) * sigma * np.sqrt(np.pi))
```

## 4. 网络变分算法 (Network Variational Method)

### 4.1 主方程离散化

网络版本的主方程：

$$d_{\text{eff}}^N = \arg\min_{d} \left[ \langle L \rangle_d - T \cdot H_d + \Lambda_N(d) \right]$$

其中：
- $\langle L \rangle_d$: 平均路径长度
- $H_d$: 路由熵
- $\Lambda_N(d)$: 网络修正

### 4.2 优化算法

```python
def network_variational_dimension(G, T=1.0):
    """
    使用变分原理计算网络有效维数
    
    Parameters:
    G: NetworkX图对象
    T: 温度参数
    
    Returns:
    d_eff: 有效维数
    """
    def free_energy(d):
        # 能量项：平均路径长度
        E = average_path_length(G, d)
        
        # 熵项：路由熵
        S = routing_entropy(G, d)
        
        # 修正项
        Lambda = topology_correction(G, d)
        
        return E - T * S + Lambda
    
    # 最小化自由能
    from scipy.optimize import minimize_scalar
    result = minimize_scalar(free_energy, bounds=(1, 10), method='bounded')
    
    return result.x

def average_path_length(G, d):
    """计算平均路径长度"""
    # 使用维度d的度量重新加权
    lengths = dict(nx.shortest_path_length(G))
    total = sum(sum(dists.values()) for dists in lengths.values())
    return total / (G.number_of_nodes() * (G.number_of_nodes() - 1))

def routing_entropy(G, d):
    """计算路由熵"""
    # 基于最短路径分布计算熵
    path_lengths = []
    for source in G.nodes():
        lengths = nx.single_source_shortest_path_length(G, source)
        path_lengths.extend(lengths.values())
    
    # 计算分布
    unique, counts = np.unique(path_lengths, return_counts=True)
    probs = counts / counts.sum()
    
    return -np.sum(probs * np.log(probs))

def topology_correction(G, d):
    """拓扑修正项"""
    # 基于聚类系数和度分布
    C = nx.average_clustering(G)
    return -C * np.log(d)
```

## 5. 算法比较

| 算法 | 复杂度 | 适用网络 | 精度 |
|------|--------|----------|------|
| 盒计数 | $O(N^2)$ | 小规模 | 中等 |
| 谱维度 | $O(N^3)$ | 中规模 | 高 |
| 变分法 | $O(N^2 \log N)$ | 大规模 | 高 |

## 6. 数值实验

### 6.1 标准网络测试

```python
# 测试网络
networks = {
    'BA_scale_free': nx.barabasi_albert_graph(1000, 3),
    'WS_small_world': nx.watts_strogatz_graph(1000, 4, 0.1),
    'ER_random': nx.erdos_renyi_graph(1000, 0.01),
    'Grid': nx.grid_2d_graph(32, 32)
}

results = {}
for name, G in networks.items():
    d_box = network_box_counting(G, max_box_size=20)
    d_spectral = network_spectral_dimension(G)
    d_variational = network_variational_dimension(G)
    
    results[name] = {
        'box_counting': d_box,
        'spectral': d_spectral,
        'variational': d_variational
    }
```

## 7. 预期结果

### 定理 I1.1: 网络维度存在性

对于任何有限连通网络，有效维数 $d_{\text{eff}}^N$ 存在且唯一。

### 定理 I1.2: 无标度网络维度

对于Barabási-Albert无标度网络：

$$d_{\text{eff}}^N \sim \frac{\log N}{\log \log N}$$

### 定理 I1.3: 小世界网络维度

对于Watts-Strogatz小世界网络：

$$d_{\text{eff}}^N = d_{\text{regular}} + \Delta d(p)$$

其中 $p$ 是重连概率，$\Delta d(p)$ 是小世界修正。

## 参考文献

1. Song, C., et al. (2005). Self-similarity of complex networks.
2. Roch, S. (2008). Gaps in the spectrum of random graphs.
3. Goh, K. I., et al. (2001). Spectra and eigenvectors of scale-free networks.
4. Boguñá, M., et al. (2009). Navigability of complex networks.

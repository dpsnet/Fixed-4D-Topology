"""
轻量级MLP实现 - 纯NumPy
用于网络受限环境下的实验验证
"""
import numpy as np
from typing import Tuple, List, Callable, Optional

class NumPyMLP:
    """使用NumPy实现的多层感知机"""
    
    def __init__(self, layer_sizes: List[int], activation: str = 'relu'):
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        self.params = {}
        self.activations = []
        self._init_params()
        self.activation_fn = self._get_activation(activation)
        self.activation_deriv = self._get_activation_deriv(activation)
        
    def _get_activation(self, name: str) -> Callable:
        activations = {
            'relu': lambda x: np.maximum(0, x),
            'tanh': np.tanh,
            'sigmoid': lambda x: 1 / (1 + np.exp(-np.clip(x, -500, 500)))
        }
        return activations.get(name, activations['relu'])
    
    def _get_activation_deriv(self, name: str) -> Callable:
        derivs = {
            'relu': lambda x: (x > 0).astype(float),
            'tanh': lambda x: 1 - np.tanh(x)**2,
            'sigmoid': lambda x: {
                'sigmoid': lambda x: 1 / (1 + np.exp(-np.clip(x, -500, 500)))
            }.get(name, lambda x: (x > 0).astype(float))(x) * (1 - {
                'sigmoid': lambda x: 1 / (1 + np.exp(-np.clip(x, -500, 500)))
            }.get(name, lambda x: (x > 0).astype(float))(x))
        }
        return derivs.get(name, derivs['relu'])
    
    def _init_params(self):
        """Xavier初始化"""
        np.random.seed(42)
        for i in range(self.num_layers - 1):
            scale = np.sqrt(2.0 / (self.layer_sizes[i] + self.layer_sizes[i+1]))
            self.params[f'W{i}'] = np.random.randn(
                self.layer_sizes[i], self.layer_sizes[i+1]
            ) * scale
            self.params[f'b{i}'] = np.zeros(self.layer_sizes[i+1])
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """前向传播，同时保存中间激活"""
        self.activations = [x]
        current = x
        
        for i in range(self.num_layers - 1):
            z = current @ self.params[f'W{i}'] + self.params[f'b{i}']
            if i < self.num_layers - 2:  # 隐藏层
                current = self.activation_fn(z)
            else:  # 输出层
                current = z  # 线性输出
            self.activations.append(current)
        
        return current
    
    def compute_fisher(self, x: np.ndarray, y: np.ndarray, 
                       loss_fn: Callable) -> np.ndarray:
        """计算Fisher信息矩阵"""
        # 简化的Fisher计算：梯度外积
        grads = self._compute_gradients(x, y, loss_fn)
        return np.outer(grads, grads)
    
    def _compute_gradients(self, x: np.ndarray, y: np.ndarray,
                          loss_fn: Callable) -> np.ndarray:
        """计算梯度（向量化）"""
        # 前向传播
        output = self.forward(x)
        loss, dloss = loss_fn(output, y)
        
        # 反向传播
        grads = []
        delta = dloss
        
        for i in range(self.num_layers - 2, -1, -1):
            a_prev = self.activations[i]
            
            # 计算梯度
            dw = a_prev.T @ delta / x.shape[0]
            db = np.mean(delta, axis=0)
            
            grads.extend([dw.flatten(), db.flatten()])
            
            if i > 0:
                delta = delta @ self.params[f'W{i}'].T
                delta *= self.activation_deriv(self.activations[i])
        
        return np.concatenate([g.flatten() for g in grads])
    
    def count_parameters(self) -> int:
        """统计参数数量"""
        return sum(p.size for p in self.params.values())
    
    def get_parameter_vector(self) -> np.ndarray:
        """获取参数向量"""
        return np.concatenate([p.flatten() for p in self.params.values()])
    
    def set_parameter_vector(self, params: np.ndarray):
        """从向量设置参数"""
        idx = 0
        for i in range(self.num_layers - 1):
            size_w = self.layer_sizes[i] * self.layer_sizes[i+1]
            self.params[f'W{i}'] = params[idx:idx+size_w].reshape(
                self.layer_sizes[i], self.layer_sizes[i+1]
            )
            idx += size_w
            
            size_b = self.layer_sizes[i+1]
            self.params[f'b{i}'] = params[idx:idx+size_b]
            idx += size_b


def mse_loss(output: np.ndarray, target: np.ndarray) -> Tuple[float, np.ndarray]:
    """MSE损失及其导数"""
    diff = output - target
    loss = 0.5 * np.mean(diff ** 2)
    dloss = diff / target.shape[0]
    return loss, dloss


def generate_synthetic_data(n_samples: int, input_dim: int, 
                            output_dim: int, noise: float = 0.1) -> Tuple[np.ndarray, np.ndarray]:
    """生成合成回归数据"""
    np.random.seed(42)
    X = np.random.randn(n_samples, input_dim)
    # 真实的低维映射
    true_W = np.random.randn(input_dim, output_dim)
    y = X @ true_W + noise * np.random.randn(n_samples, output_dim)
    return X, y


if __name__ == '__main__':
    # 测试
    print("Testing NumPy MLP implementation...")
    mlp = NumPyMLP([10, 50, 50, 5], activation='relu')
    print(f"Parameters: {mlp.count_parameters()}")
    
    X, y = generate_synthetic_data(100, 10, 5)
    output = mlp.forward(X)
    print(f"Output shape: {output.shape}")
    print("✓ NumPy MLP implementation ready")

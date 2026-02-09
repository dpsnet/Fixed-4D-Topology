#!/usr/bin/env python3
"""
H方向: 量子维度数值模拟
使用iTEBD (无限时间演化块 decimation) 算法计算自旋链的纠缠维度
"""
import numpy as np
from scipy.linalg import expm
from typing import Tuple, List
import sys
import os
import json
from datetime import datetime

class iTEBDSimulator:
    """
    无限时间演化块 decimation (iTEBD) 模拟器
    用于计算一维量子自旋链的纠缠维度
    """
    
    def __init__(self, bond_dim: int = 20, spin_dim: int = 2):
        """
        初始化iTEBD模拟器
        
        Args:
            bond_dim: MPS键维度 (虚拟维度)
            spin_dim: 物理自旋维度 (2 for spin-1/2)
        """
        self.bond_dim = bond_dim
        self.spin_dim = spin_dim
        self.GammaA = None  # A位点张量
        self.GammaB = None  # B位点张量
        self.Lambda = None  # 奇异值向量
        
        self._initialize_mps()
    
    def _initialize_mps(self):
        """初始化MPS为乘积态 |000...>"""
        # Gamma张量: [bond_dim, spin_dim, bond_dim]
        self.GammaA = np.zeros((self.bond_dim, self.spin_dim, self.bond_dim))
        self.GammaB = np.zeros((self.bond_dim, self.spin_dim, self.bond_dim))
        
        # 初始化为简单乘积态
        self.GammaA[0, 0, 0] = 1.0
        self.GammaB[0, 0, 0] = 1.0
        
        # Lambda: 键上的奇异值
        self.Lambda = np.zeros(self.bond_dim)
        self.Lambda[0] = 1.0
    
    def heisenberg_hamiltonian(self, J: float = 1.0, h: float = 0.0) -> np.ndarray:
        """
        构造海森堡哈密顿量门
        H = J * (S_x S_x + S_y S_y + S_z S_z) - h * S_z
        """
        # Pauli矩阵
        Sx = np.array([[0, 1], [1, 0]]) / 2
        Sy = np.array([[0, -1j], [1j, 0]]) / 2
        Sz = np.array([[1, 0], [0, -1]]) / 2
        
        # 两体相互作用
        H_int = J * (np.kron(Sx, Sx) + np.kron(Sy, Sy) + np.kron(Sz, Sz))
        
        # 单体场
        H_field = -h * (np.kron(Sz, np.eye(2)) + np.kron(np.eye(2), Sz))
        
        H = H_int + H_field
        
        # 小时间步演化门 (一阶Trotter)
        dt = 0.01
        U = expm(-1j * H * dt).reshape(self.spin_dim, self.spin_dim, 
                                                  self.spin_dim, self.spin_dim)
        
        return U
    
    def apply_gate(self, U: np.ndarray):
        """应用两体演化门并更新MPS"""
        # 构造theta张量
        # theta = GammaA * Lambda * GammaB * Lambda
        theta = np.tensordot(self.GammaA, np.diag(self.Lambda), axes=([2], [0]))
        theta = np.tensordot(theta, self.GammaB, axes=([2], [0]))
        theta = np.tensordot(theta, np.diag(self.Lambda), axes=([3], [0]))
        
        # theta: [bondA, spinA, spinB, bondB]
        theta = np.tensordot(theta, U, axes=([1, 2], [2, 3]))
        # theta: [bondA, bondB, spinA, spinB]
        theta = theta.transpose(0, 2, 3, 1)
        
        # SVD分解
        theta_mat = theta.reshape(self.bond_dim * self.spin_dim, 
                                  self.spin_dim * self.bond_dim)
        
        U_svd, S, Vh = np.linalg.svd(theta_mat, full_matrices=False)
        
        # 截断到bond_dim
        chi = min(self.bond_dim, len(S))
        U_svd = U_svd[:, :chi]
        S = S[:chi]
        Vh = Vh[:chi, :]
        
        # 归一化
        S = S / np.linalg.norm(S)
        
        # 更新张量
        self.GammaA = U_svd.reshape(self.bond_dim, self.spin_dim, chi)[:, :, :self.bond_dim]
        self.GammaB = Vh.reshape(chi, self.spin_dim, self.bond_dim)[:self.bond_dim, :, :]
        self.Lambda = np.zeros(self.bond_dim)
        self.Lambda[:chi] = S
    
    def compute_entanglement_entropy(self) -> float:
        """计算纠缠熵 S = -sum(lambda^2 log(lambda^2))"""
        lambda_sq = self.Lambda ** 2
        lambda_sq = lambda_sq[lambda_sq > 1e-15]  # 避免数值问题
        
        entropy = -np.sum(lambda_sq * np.log(lambda_sq))
        return entropy
    
    def compute_quantum_dimension(self) -> float:
        """
        计算量子维度
        d_q = exp(S) 其中 S 是纠缠熵
        """
        S = self.compute_entanglement_entropy()
        d_q = np.exp(S)
        return d_q
    
    def run_simulation(self, n_steps: int = 100) -> List[dict]:
        """
        运行iTEBD模拟
        
        Returns:
            记录每步的纠缠熵和量子维度
        """
        U = self.heisenberg_hamiltonian(J=1.0, h=0.0)
        
        history = []
        for step in range(n_steps):
            self.apply_gate(U)
            
            if step % 10 == 0:
                S = self.compute_entanglement_entropy()
                d_q = self.compute_quantum_dimension()
                
                history.append({
                    'step': step,
                    'entropy': float(S),
                    'quantum_dimension': float(d_q),
                    'max_singular': float(self.Lambda[0])
                })
                
                print(f"  Step {step:4d}: S={S:.4f}, d_q={d_q:.4f}, "
                      f"lambda_max={self.Lambda[0]:.4f}")
        
        return history


def run_h_direction_experiment():
    """运行H方向实验"""
    print("=" * 70)
    print("H方向: 量子维度数值模拟 (iTEBD)")
    print("=" * 70)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'experiments': []
    }
    
    # 不同键维度的实验
    bond_dims = [10, 20, 40]
    
    for bond_dim in bond_dims:
        print(f"\n📊 键维度: {bond_dim}")
        
        sim = iTEBDSimulator(bond_dim=bond_dim, spin_dim=2)
        history = sim.run_simulation(n_steps=200)
        
        final_state = history[-1] if history else None
        
        exp_result = {
            'bond_dim': bond_dim,
            'final_entropy': final_state['entropy'] if final_state else 0,
            'final_quantum_dimension': final_state['quantum_dimension'] if final_state else 0,
            'history': history
        }
        
        results['experiments'].append(exp_result)
        
        print(f"   最终纠缠熵: {exp_result['final_entropy']:.4f}")
        print(f"   最终量子维度: {exp_result['final_quantum_dimension']:.4f}")
    
    # 保存结果
    with open('results_h_quantum_dimension.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ 结果已保存: results_h_quantum_dimension.json")
    
    return results


if __name__ == '__main__':
    run_h_direction_experiment()

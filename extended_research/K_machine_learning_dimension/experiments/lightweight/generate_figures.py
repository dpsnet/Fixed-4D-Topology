#!/usr/bin/env python3
"""
生成论文图表 (纯ASCII/文本格式，无需matplotlib)
"""
import json
import os


def print_bar_chart(title, labels, values, width=50):
    """打印ASCII条形图"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    
    max_val = max(values) if values else 1
    for label, val in zip(labels, values):
        bar_len = int((val / max_val) * width) if max_val > 0 else 0
        bar = '█' * bar_len
        print(f"{label:15s} |{bar:<{width}s}| {val:.2f}")


def print_line_plot(title, x_label, y_label, x_vals, y_vals, width=60, height=15):
    """打印ASCII折线图"""
    print(f"\n{'='*60}")
    print(f"📈 {title}")
    print(f"{'='*60}")
    
    if not y_vals:
        print("(无数据)")
        return
    
    y_min, y_max = min(y_vals), max(y_vals)
    y_range = y_max - y_min if y_max != y_min else 1
    
    # 构建图形
    grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # 绘制坐标轴
    for i in range(height):
        grid[i][0] = '│'
    for j in range(width):
        grid[-1][j] = '─'
    grid[-1][0] = '└'
    
    # 绘制数据点
    for i, (x, y) in enumerate(zip(x_vals, y_vals)):
        x_pos = int((i / max(len(x_vals)-1, 1)) * (width - 5)) + 3
        y_pos = height - 2 - int(((y - y_min) / y_range) * (height - 3))
        y_pos = max(0, min(height-2, y_pos))
        grid[y_pos][x_pos] = '●'
    
    # 添加标签
    print(f"{y_label}")
    for row in grid:
        print(''.join(row))
    print(f"{x_label}")
    print(f"  范围: [{min(x_vals):.0f}, {max(x_vals):.0f}] {y_label}: [{y_min:.2f}, {y_max:.2f}]")


def generate_all_figures():
    """生成所有图表"""
    
    # 加载E1数据
    if os.path.exists('results_e1_lightweight.json'):
        with open('results_e1_lightweight.json') as f:
            e1_data = json.load(f)
        
        labels = [c['name'] for c in e1_data['configurations']]
        d_effs = [c['estimates']['fisher']['d_eff_pr'] for c in e1_data['configurations']]
        ratios = [c['estimates']['fisher']['d_eff_pr'] / c['total_params'] * 100 
                  for c in e1_data['configurations']]
        
        print_bar_chart("E1: 不同架构的有效维度 (d_eff)", labels, d_effs)
        print_bar_chart("E1: 有效维度比例 (d_eff/N %)", labels, ratios)
    
    # 加载E2数据
    if os.path.exists('results_e2_lightweight.json'):
        with open('results_e2_lightweight.json') as f:
            e2_data = json.load(f)
        
        # 深度实验
        depth_exp = e2_data['experiments'][0]
        depths = [c['depth'] for c in depth_exp['configs']]
        depth_ratios = [c['d_eff_ratio'] * 100 for c in depth_exp['configs']]
        
        print_line_plot("E2: 深度 vs 有效维度比例", 
                       "深度 (层数)", "d_eff/N (%)", 
                       depths, depth_ratios)
        
        # 宽度实验
        width_exp = e2_data['experiments'][1]
        widths = [c['width'] for c in width_exp['configs']]
        width_ratios = [c['d_eff_ratio'] * 100 for c in width_exp['configs']]
        
        print_line_plot("E2: 宽度 vs 有效维度比例",
                       "隐藏层宽度", "d_eff/N (%)",
                       widths, width_ratios)
    
    # 加载E3数据
    if os.path.exists('results_e3_lightweight.json'):
        with open('results_e3_lightweight.json') as f:
            e3_data = json.load(f)
        
        trace = e3_data['training_traces'][0]
        epochs = [e['epoch'] for e in trace['epochs']]
        d_effs = [e['d_eff'] for e in trace['epochs']]
        losses = [e['loss'] for e in trace['epochs']]
        
        print_line_plot("E3: 训练过程中有效维度演化",
                       "Epoch", "d_eff",
                       epochs, d_effs)
        
        print_line_plot("E3: 训练损失曲线",
                       "Epoch", "Loss",
                       epochs, losses)
    
    print(f"\n{'='*60}")
    print("图表生成完成")
    print(f"{'='*60}")


if __name__ == '__main__':
    generate_all_figures()

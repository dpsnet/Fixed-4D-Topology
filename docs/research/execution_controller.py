#!/usr/bin/env python3
"""
AI研究执行控制器
实现任务驱动的并行研究执行框架
"""

import yaml
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import heapq

class TaskStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskType(Enum):
    ACQUIRE = "acquire"
    READ = "read"
    COMPUTE = "compute"
    PROVE = "prove"
    WRITE = "write"
    SETUP = "setup"
    RESEARCH = "research"
    SYNTHESIZE = "synthesize"

@dataclass
class Task:
    id: str
    direction: str
    phase: int = 1
    title: str = ""
    type: TaskType = TaskType.READ
    priority: int = 50
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    checkpoints: List[str] = field(default_factory=list)
    estimated_effort: str = "1h"
    actual_effort: str = ""
    milestone: bool = False
    created: str = ""
    completed: str = ""
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = TaskType(self.type)
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
    
    @property
    def priority_score(self) -> int:
        """计算动态优先级分数"""
        score = self.priority
        
        # 里程碑任务加权
        if self.milestone:
            score += 20
            
        # 依赖就绪加权
        if self.status == TaskStatus.PENDING and self.dependencies:
            score += 10
            
        return score
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "direction": self.direction,
            "phase": self.phase,
            "title": self.title,
            "type": self.type.value,
            "priority": self.priority,
            "status": self.status.value,
            "dependencies": self.dependencies,
            "blocks": self.blocks,
            "deliverables": self.deliverables,
            "checkpoints": self.checkpoints,
            "estimated_effort": self.estimated_effort,
            "actual_effort": self.actual_effort,
            "milestone": self.milestone,
            "created": self.created,
            "completed": self.completed
        }

class ExecutionController:
    """研究执行控制器"""
    
    def __init__(self, tasks_file: str = "tasks/initial_tasks.yaml"):
        self.tasks_file = Path(tasks_file)
        self.tasks: Dict[str, Task] = {}
        self.direction_weights = {
            "kleinian": 40,
            "padic": 35,
            "maass": 25,
            "shared": 30
        }
        self.max_parallel = 5
        self.running = False
        
        # 统计
        self.stats = {
            "tasks_created": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "direction_progress": {
                "kleinian": 0,
                "padic": 0,
                "maass": 0
            }
        }
        
        self.load_tasks()
    
    def load_tasks(self):
        """加载任务数据库"""
        if not self.tasks_file.exists():
            print(f"任务文件不存在: {self.tasks_file}")
            return
            
        with open(self.tasks_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        for task_data in data.get('tasks', []):
            task = Task(**task_data)
            self.tasks[task.id] = task
            
        self.direction_weights = data.get('global', {}).get('direction_weights', self.direction_weights)
        self.stats["tasks_created"] = len(self.tasks)
        
        # 初始化方向进度
        for direction in ["kleinian", "padic", "maass"]:
            self.update_direction_progress(direction)
        
        print(f"已加载 {len(self.tasks)} 个任务")
    
    def save_tasks(self):
        """保存任务状态"""
        data = {
            "meta": {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "total_tasks": len(self.tasks)
            },
            "global": {
                "direction_weights": self.direction_weights,
                "execution_mode": "adaptive",
                "max_parallel_tasks": self.max_parallel
            },
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "active_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.ACTIVE],
            "completed_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.COMPLETED],
            "blocked_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]
        }
        
        # 保存带时间戳的快照
        snapshot_file = Path(f"snapshots/snapshot_{datetime.now():%Y%m%d_%H%M%S}.json")
        snapshot_file.parent.mkdir(exist_ok=True)
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 更新主文件
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    
    def calculate_priority(self, task: Task) -> int:
        """计算任务动态优先级"""
        score = task.priority
        
        # 1. 方向战略权重 (0-40分)
        score += self.direction_weights.get(task.direction, 30)
        
        # 2. 阻塞影响
        blocked_count = len(task.blocks)
        score += min(20, blocked_count * 5)
        
        # 3. 里程碑加权
        if task.milestone:
            score += 15
        
        return score
    
    def update_dependencies(self):
        """更新所有任务的依赖状态"""
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
                
            # 检查依赖是否完成
            def dep_is_completed(dep_id):
                dep_task = self.tasks.get(dep_id)
                return dep_task is not None and dep_task.status == TaskStatus.COMPLETED
            
            deps_completed = all(dep_is_completed(dep_id) for dep_id in task.dependencies)
            
            if deps_completed and task.status == TaskStatus.BLOCKED:
                task.status = TaskStatus.PENDING
                self.log(f"任务 {task.id} 解阻塞")
    
    def get_ready_tasks(self) -> List[Task]:
        """获取所有就绪的任务"""
        ready = []
        for task in self.tasks.values():
            if task.status != TaskStatus.PENDING:
                continue
                
            # 检查依赖
            def is_completed(dep_id):
                dep_task = self.tasks.get(dep_id)
                return dep_task is not None and dep_task.status == TaskStatus.COMPLETED
            
            deps_completed = all(is_completed(dep_id) for dep_id in task.dependencies)
            
            if deps_completed:
                ready.append(task)
        
        return ready
    
    def select_next_tasks(self, n: int = 3) -> List[Task]:
        """选择接下来要执行的任务"""
        ready = self.get_ready_tasks()
        
        # 计算优先级
        for task in ready:
            task.priority = self.calculate_priority(task)
        
        # 按优先级排序
        ready.sort(key=lambda t: t.priority_score, reverse=True)
        
        return ready[:n]
    
    def start_task(self, task: Task):
        """开始执行任务并立即保存YAML"""
        task.status = TaskStatus.ACTIVE
        task.created = datetime.now().isoformat()
        self.save_tasks()
        self.log(f"开始任务: {task.id} - {task.title} (已保存到YAML)")
    
    def complete_task(self, task: Task, actual_effort: str = ""):
        """标记任务完成并立即保存YAML"""
        task.status = TaskStatus.COMPLETED
        task.completed = datetime.now().isoformat()
        if actual_effort:
            task.actual_effort = actual_effort
        
        self.stats["tasks_completed"] += 1
        self.update_direction_progress(task.direction)
        
        # 立即保存YAML - 确保数据持久化
        self.save_tasks()
        
        self.log(f"完成任务: {task.id} (已保存到YAML)")
        
        # 检查是否解锁新任务
        self.update_dependencies()
    
    def fail_task(self, task: Task, reason: str = ""):
        """标记任务失败并立即保存YAML"""
        task.status = TaskStatus.FAILED
        self.stats["tasks_failed"] += 1
        self.save_tasks()
        self.log(f"任务失败: {task.id} - {reason} (已保存到YAML)")
    
    def block_task(self, task: Task, reason: str = ""):
        """阻塞任务并立即保存YAML"""
        task.status = TaskStatus.BLOCKED
        self.save_tasks()
        self.log(f"任务阻塞: {task.id} - {reason} (已保存到YAML)")
    
    def update_direction_progress(self, direction: str):
        """更新方向进展"""
        direction_tasks = [t for t in self.tasks.values() if t.direction == direction]
        if not direction_tasks:
            return
            
        completed = len([t for t in direction_tasks if t.status == TaskStatus.COMPLETED])
        total = len(direction_tasks)
        self.stats["direction_progress"][direction] = round(completed / total * 100)
    
    def get_dashboard(self) -> str:
        """生成仪表板显示"""
        lines = []
        lines.append("=" * 60)
        lines.append("AI研究执行仪表板")
        lines.append(f"更新时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lines.append("=" * 60)
        lines.append("")
        
        # 方向进展
        lines.append("方向进展:")
        for direction, progress in self.stats["direction_progress"].items():
            bar = "█" * (progress // 5) + "░" * (20 - progress // 5)
            lines.append(f"  {direction:12} [{bar}] {progress}%")
        lines.append("")
        
        # 任务统计
        active = len([t for t in self.tasks.values() if t.status == TaskStatus.ACTIVE])
        pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        blocked = len([t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED])
        
        lines.append("任务统计:")
        lines.append(f"  活跃: {active} | 就绪: {pending} | 完成: {completed} | 阻塞: {blocked}")
        lines.append("")
        
        # 高优先级就绪任务
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        lines.append("高优先级就绪任务 (Top 5):")
        for i, task in enumerate(ready[:5], 1):
            priority = self.calculate_priority(task)
            lines.append(f"  {i}. {task.id} [{task.direction}] {task.title[:40]}... (P:{priority})")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        
        # 输出到控制台
        print(log_entry)
        
        # 保存到日志文件
        log_file = Path(f"logs/execution_{datetime.now():%Y-%m-%d}.log")
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def run_cycle(self):
        """执行一个工作周期"""
        # 1. 更新依赖状态
        self.update_dependencies()
        
        # 2. 选择下一个任务
        current_active = len([t for t in self.tasks.values() if t.status == TaskStatus.ACTIVE])
        if current_active < self.max_parallel:
            next_tasks = self.select_next_tasks(self.max_parallel - current_active)
            for task in next_tasks:
                self.start_task(task)
        
        # 3. 保存状态
        self.save_tasks()
        
        # 4. 显示仪表板
        print("\n" + self.get_dashboard() + "\n")
    
    def run(self, cycles: Optional[int] = None, interval: int = 60):
        """运行主循环"""
        self.running = True
        cycle_count = 0
        
        self.log("执行控制器启动")
        
        try:
            while self.running:
                self.run_cycle()
                cycle_count += 1
                
                if cycles and cycle_count >= cycles:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log("执行控制器停止")
            self.save_tasks()
    
    def execute_task(self, task_id: str, auto_complete: bool = False) -> bool:
        """执行单个任务 (模拟或真实执行)"""
        task = self.tasks.get(task_id)
        if not task:
            self.log(f"任务不存在: {task_id}")
            return False
        
        self.start_task(task)
        
        # 这里可以实现真实的任务执行逻辑
        # 目前为模拟
        if auto_complete:
            time.sleep(1)  # 模拟执行时间
            self.complete_task(task, task.estimated_effort)
            return True
        
        return True
    
    def generate_report(self) -> str:
        """生成执行报告"""
        lines = []
        lines.append("# 研究执行报告")
        lines.append(f"\n生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lines.append("\n## 总体统计\n")
        
        total = len(self.tasks)
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        active = len([t for t in self.tasks.values() if t.status == TaskStatus.ACTIVE])
        pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        
        lines.append(f"- 总任务数: {total}")
        lines.append(f"- 已完成: {completed} ({completed/total*100:.1f}%)")
        lines.append(f"- 进行中: {active}")
        lines.append(f"- 待执行: {pending}")
        lines.append("")
        
        # 各方向统计
        lines.append("## 各方向进展\n")
        for direction in ["kleinian", "padic", "maass"]:
            dir_tasks = [t for t in self.tasks.values() if t.direction == direction]
            dir_completed = len([t for t in dir_tasks if t.status == TaskStatus.COMPLETED])
            if dir_tasks:
                pct = dir_completed / len(dir_tasks) * 100
                lines.append(f"- **{direction}**: {dir_completed}/{len(dir_tasks)} ({pct:.1f}%)")
        
        lines.append("")
        
        # 即将执行的任务
        lines.append("## 即将执行的高优先级任务\n")
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        for task in ready[:10]:
            lines.append(f"- {task.id}: {task.title}")
        
        return "\n".join(lines)


def main():
    """主入口"""
    controller = ExecutionController()
    
    # 显示初始仪表板
    print(controller.get_dashboard())
    
    # 保存初始状态
    controller.save_tasks()
    
    # 生成报告
    report = controller.generate_report()
    with open("logs/initial_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n初始报告已保存到 logs/initial_report.md")
    print("\n使用方法:")
    print("  python execution_controller.py --dashboard  # 显示仪表板")
    print("  python execution_controller.py --report     # 生成报告")
    print("  python execution_controller.py --run        # 启动执行循环")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        controller = ExecutionController()
        
        if sys.argv[1] == "--dashboard":
            print(controller.get_dashboard())
        elif sys.argv[1] == "--report":
            report = controller.generate_report()
            print(report)
            with open("logs/report.md", 'w', encoding='utf-8') as f:
                f.write(report)
        elif sys.argv[1] == "--run":
            controller.run()
        else:
            main()
    else:
        main()

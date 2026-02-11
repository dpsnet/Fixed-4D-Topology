#!/usr/bin/env python3
"""
Phase 2 研究执行控制器
专门用于严格性提升阶段(L4→L1)的任务追踪和管理

基于 execution_controller.py，专门针对Phase 2任务优化
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
    IN_PROGRESS = "in_progress"  # Phase 2新增状态
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskType(Enum):
    ACQUIRE = "acquire"
    READ = "read"
    COMPUTE = "compute"
    PROVE = "prove"  # Phase 2核心任务类型
    WRITE = "write"
    SETUP = "setup"
    RESEARCH = "research"
    SYNTHESIZE = "synthesize"

class RigorLevel(Enum):
    L1 = "L1"  # 完整证明
    L2 = "L2"  # 严格框架+计算验证
    L3 = "L3"  # 启发式+强数值证据
    L4 = "L4"  # 猜想/推测

@dataclass
class Task:
    id: str
    direction: str
    phase: int = 2  # Phase 2固定
    title: str = ""
    type: TaskType = TaskType.RESEARCH
    priority: int = 50
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    checkpoints: List[str] = field(default_factory=list)
    estimated_effort: str = "1w"  # Phase 2使用周为单位
    actual_effort: str = ""
    milestone: bool = False
    created: str = ""
    completed: str = ""
    # Phase 2新增字段
    rigor_level: Optional[RigorLevel] = None
    conjecture: Optional[int] = None  # 1 or 2
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = TaskType(self.type)
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)
        if isinstance(self.rigor_level, str):
            self.rigor_level = RigorLevel(self.rigor_level)
    
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
            
        # L1证明任务额外加权
        if self.rigor_level == RigorLevel.L1:
            score += 15
            
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
            "completed": self.completed,
            "rigor_level": self.rigor_level.value if self.rigor_level else None,
            "conjecture": self.conjecture
        }

@dataclass
class Milestone:
    """Phase 2里程碑"""
    id: str
    name: str
    date: str
    tasks: List[str]
    status: str = "pending"
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "tasks": self.tasks,
            "status": self.status
        }

class Phase2ExecutionController:
    """Phase 2研究执行控制器 - 严格性提升专用"""
    
    def __init__(self, tasks_file: str = "tasks/phase2_tasks.yaml"):
        self.tasks_file = Path(tasks_file)
        self.tasks: Dict[str, Task] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.direction_weights = {
            "kleinian": 40,
            "padic": 35,
            "maass": 25,
            "shared": 30
        }
        self.max_parallel = 5
        self.running = False
        
        # Phase 2进度追踪
        self.rigor_progress = {
            1: {"L4": True, "L3": False, "L2": False, "L1": False},  # 猜想1
            2: {"L4": True, "L3": False, "L2": False, "L1": False}   # 猜想2
        }
        
        # 统计
        self.stats = {
            "tasks_created": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "direction_progress": {
                "kleinian": 0,
                "padic": 0,
                "maass": 0,
                "shared": 0
            },
            "rigor_distribution": {
                "L4": 0,
                "L3": 0,
                "L2": 0,
                "L1": 0
            }
        }
        
        self.load_tasks()
    
    def load_tasks(self):
        """加载Phase 2任务数据库"""
        if not self.tasks_file.exists():
            print(f"任务文件不存在: {self.tasks_file}")
            return
            
        with open(self.tasks_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # 加载任务
        for task_data in data.get('tasks', []):
            task = Task(**task_data)
            self.tasks[task.id] = task
            
        # 加载里程碑
        for ms_data in data.get('milestones', []):
            ms = Milestone(**ms_data)
            self.milestones[ms.id] = ms
            
        self.direction_weights = data.get('global', {}).get('direction_weights', self.direction_weights)
        self.stats["tasks_created"] = len(self.tasks)
        
        # 初始化进度
        for direction in ["kleinian", "padic", "maass", "shared"]:
            self.update_direction_progress(direction)
        
        # 更新严格性分布
        self.update_rigor_distribution()
        
        print(f"已加载 {len(self.tasks)} 个Phase 2任务")
        print(f"已加载 {len(self.milestones)} 个里程碑")
    
    def save_tasks(self):
        """保存任务状态"""
        data = {
            "meta": {
                "version": "2.0",
                "last_updated": datetime.now().isoformat(),
                "total_tasks": len(self.tasks),
                "phase": 2,
                "phase_name": "严格性提升阶段"
            },
            "global": {
                "direction_weights": self.direction_weights,
                "execution_mode": "adaptive",
                "max_parallel_tasks": self.max_parallel,
                "rigor_target": {
                    "conjecture_1": {"current": "L4", "target": "L1"},
                    "conjecture_2": {"current": "L4", "target": "L1"}
                }
            },
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "milestones": [ms.to_dict() for ms in self.milestones.values()],
            "active_tasks": [t.id for t in self.tasks.values() if t.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS]],
            "completed_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.COMPLETED],
            "blocked_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]
        }
        
        # 保存带时间戳的快照
        snapshot_file = Path(f"snapshots/phase2_snapshot_{datetime.now():%Y%m%d_%H%M%S}.json")
        snapshot_file.parent.mkdir(exist_ok=True)
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 更新主文件
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    
    def update_rigor_distribution(self):
        """更新严格性分布统计"""
        distribution = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}
        for task in self.tasks.values():
            if task.rigor_level:
                distribution[task.rigor_level.value] += 1
        self.stats["rigor_distribution"] = distribution
    
    def calculate_priority(self, task: Task) -> int:
        """计算任务动态优先级（Phase 2优化版）"""
        score = task.priority
        
        # 1. 方向战略权重
        score += self.direction_weights.get(task.direction, 30)
        
        # 2. 阻塞影响
        blocked_count = len(task.blocks)
        score += min(20, blocked_count * 5)
        
        # 3. 里程碑加权
        if task.milestone:
            score += 15
        
        # 4. 严格性级别加权（L1任务优先级更高）
        if task.rigor_level == RigorLevel.L1:
            score += 10
        elif task.rigor_level == RigorLevel.L2:
            score += 5
            
        # 5. 关键路径上的任务加权
        if task.id.startswith("P2-C1-T") or task.id.startswith("P2-C2-T"):
            score += 5  # 核心猜想任务
            
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
            if task.status not in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]:
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
        """开始执行任务"""
        task.status = TaskStatus.IN_PROGRESS if task.type == TaskType.RESEARCH else TaskStatus.ACTIVE
        task.created = datetime.now().isoformat()
        self.save_tasks()
        self.log(f"开始任务: {task.id} - {task.title} [严格性: {task.rigor_level.value if task.rigor_level else 'N/A'}]")
    
    def complete_task(self, task: Task, actual_effort: str = ""):
        """标记任务完成"""
        task.status = TaskStatus.COMPLETED
        task.completed = datetime.now().isoformat()
        if actual_effort:
            task.actual_effort = actual_effort
        
        self.stats["tasks_completed"] += 1
        self.update_direction_progress(task.direction)
        self.update_rigor_distribution()
        
        # 检查里程碑
        self.check_milestones()
        
        # 立即保存YAML
        self.save_tasks()
        
        self.log(f"完成任务: {task.id} (严格性: {task.rigor_level.value if task.rigor_level else 'N/A'})")
        
        # 检查是否解锁新任务
        self.update_dependencies()
    
    def check_milestones(self):
        """检查里程碑状态"""
        for ms in self.milestones.values():
            if ms.status == "completed":
                continue
                
            # 检查所有相关任务是否完成
            all_completed = all(
                self.tasks.get(t_id) and self.tasks[t_id].status == TaskStatus.COMPLETED
                for t_id in ms.tasks
            )
            
            if all_completed:
                ms.status = "completed"
                self.log(f"🎉 里程碑达成: {ms.name} ({ms.id})")
    
    def fail_task(self, task: Task, reason: str = ""):
        """标记任务失败"""
        task.status = TaskStatus.FAILED
        self.stats["tasks_failed"] += 1
        self.save_tasks()
        self.log(f"任务失败: {task.id} - {reason}")
    
    def block_task(self, task: Task, reason: str = ""):
        """阻塞任务"""
        task.status = TaskStatus.BLOCKED
        self.save_tasks()
        self.log(f"任务阻塞: {task.id} - {reason}")
    
    def update_direction_progress(self, direction: str):
        """更新方向进展"""
        direction_tasks = [t for t in self.tasks.values() if t.direction == direction]
        if not direction_tasks:
            return
            
        completed = len([t for t in direction_tasks if t.status == TaskStatus.COMPLETED])
        total = len(direction_tasks)
        self.stats["direction_progress"][direction] = round(completed / total * 100)
    
    def get_rigor_dashboard(self) -> str:
        """生成严格性进展仪表板"""
        lines = []
        lines.append("=" * 70)
        lines.append("Phase 2 严格性提升仪表板")
        lines.append(f"更新时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lines.append("=" * 70)
        lines.append("")
        
        # 猜想严格性进展
        lines.append("📊 猜想严格性进展:")
        lines.append("")
        for conj in [1, 2]:
            lines.append(f"  猜想{conj}: L4 → L1")
            # L4→L3进度
            l4_to_l3_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L3]
            l4_to_l3_completed = len([t for t in l4_to_l3_tasks if t.status == TaskStatus.COMPLETED])
            l4_to_l3_total = len(l4_to_l3_tasks)
            progress = (l4_to_l3_completed / l4_to_l3_total * 100) if l4_to_l3_total > 0 else 0
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            lines.append(f"    L4→L3: [{bar}] {progress:.0f}% ({l4_to_l3_completed}/{l4_to_l3_total})")
            
            # L3→L2进度
            l3_to_l2_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L2]
            l3_to_l2_completed = len([t for t in l3_to_l2_tasks if t.status == TaskStatus.COMPLETED])
            l3_to_l2_total = len(l3_to_l2_tasks)
            progress = (l3_to_l2_completed / l3_to_l2_total * 100) if l3_to_l2_total > 0 else 0
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            lines.append(f"    L3→L2: [{bar}] {progress:.0f}% ({l3_to_l2_completed}/{l3_to_l2_total})")
            
            # L2→L1进度
            l2_to_l1_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L1]
            l2_to_l1_completed = len([t for t in l2_to_l1_tasks if t.status == TaskStatus.COMPLETED])
            l2_to_l1_total = len(l2_to_l1_tasks)
            progress = (l2_to_l1_completed / l2_to_l1_total * 100) if l2_to_l1_total > 0 else 0
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            lines.append(f"    L2→L1: [{bar}] {progress:.0f}% ({l2_to_l1_completed}/{l2_to_l1_total})")
            lines.append("")
        
        return "\n".join(lines)
    
    def get_dashboard(self) -> str:
        """生成完整仪表板显示"""
        lines = []
        lines.append(self.get_rigor_dashboard())
        
        # 方向进展
        lines.append("📈 方向进展:")
        for direction, progress in self.stats["direction_progress"].items():
            bar = "█" * (progress // 5) + "░" * (20 - progress // 5)
            lines.append(f"  {direction:12} [{bar}] {progress}%")
        lines.append("")
        
        # 任务统计
        active = len([t for t in self.tasks.values() if t.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS]])
        pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        blocked = len([t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED])
        
        lines.append("📋 任务统计:")
        lines.append(f"  进行中: {active} | 就绪: {pending} | 完成: {completed} | 阻塞: {blocked}")
        lines.append("")
        
        # 里程碑状态
        lines.append("🏆 里程碑状态:")
        for ms in sorted(self.milestones.values(), key=lambda m: m.date):
            status_icon = "✅" if ms.status == "completed" else "⏳" if ms.status == "in_progress" else "🔘"
            lines.append(f"  {status_icon} {ms.id}: {ms.name} ({ms.date})")
        lines.append("")
        
        # 高优先级就绪任务
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        lines.append("🔥 高优先级就绪任务 (Top 5):")
        for i, task in enumerate(ready[:5], 1):
            priority = self.calculate_priority(task)
            rigor = f"[{task.rigor_level.value}]" if task.rigor_level else "[N/A]"
            lines.append(f"  {i}. {task.id} {rigor} {task.title[:35]}... (P:{priority})")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[Phase2] [{timestamp}] {message}"
        
        # 输出到控制台
        print(log_entry)
        
        # 保存到日志文件
        log_file = Path(f"logs/phase2_execution_{datetime.now():%Y-%m-%d}.log")
        log_file.parent.mkdir(exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def run_cycle(self):
        """执行一个工作周期"""
        # 1. 更新依赖状态
        self.update_dependencies()
        
        # 2. 选择下一个任务
        current_active = len([t for t in self.tasks.values() if t.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS]])
        if current_active < self.max_parallel:
            next_tasks = self.select_next_tasks(self.max_parallel - current_active)
            for task in next_tasks:
                if task.status == TaskStatus.PENDING:
                    self.start_task(task)
        
        # 3. 保存状态
        self.save_tasks()
        
        # 4. 显示仪表板
        print("\n" + self.get_dashboard() + "\n")
    
    def run(self, cycles: Optional[int] = None, interval: int = 60):
        """运行主循环"""
        self.running = True
        cycle_count = 0
        
        self.log("Phase 2 执行控制器启动")
        
        try:
            while self.running:
                self.run_cycle()
                cycle_count += 1
                
                if cycles and cycle_count >= cycles:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log("Phase 2 执行控制器停止")
            self.save_tasks()
    
    def execute_task(self, task_id: str, auto_complete: bool = False) -> bool:
        """执行单个任务"""
        task = self.tasks.get(task_id)
        if not task:
            self.log(f"任务不存在: {task_id}")
            return False
        
        self.start_task(task)
        
        if auto_complete:
            time.sleep(1)
            self.complete_task(task, task.estimated_effort)
            return True
        
        return True
    
    def generate_report(self) -> str:
        """生成Phase 2执行报告"""
        lines = []
        lines.append("# Phase 2 研究执行报告")
        lines.append(f"\n生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lines.append("\n## 总体统计\n")
        
        total = len(self.tasks)
        completed = len([t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED])
        active = len([t for t in self.tasks.values() if t.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS]])
        pending = len([t for t in self.tasks.values() if t.status == TaskStatus.PENDING])
        
        lines.append(f"- 总任务数: {total}")
        lines.append(f"- 已完成: {completed} ({completed/total*100:.1f}%)")
        lines.append(f"- 进行中: {active}")
        lines.append(f"- 待执行: {pending}")
        lines.append("")
        
        # 各方向统计
        lines.append("## 各方向进展\n")
        for direction in ["kleinian", "padic", "maass", "shared"]:
            dir_tasks = [t for t in self.tasks.values() if t.direction == direction]
            dir_completed = len([t for t in dir_tasks if t.status == TaskStatus.COMPLETED])
            if dir_tasks:
                pct = dir_completed / len(dir_tasks) * 100
                lines.append(f"- **{direction}**: {dir_completed}/{len(dir_tasks)} ({pct:.1f}%)")
        
        lines.append("")
        
        # 严格性分布
        lines.append("## 严格性级别分布\n")
        for level in ["L4", "L3", "L2", "L1"]:
            count = self.stats["rigor_distribution"][level]
            lines.append(f"- **{level}**: {count} 个任务")
        
        lines.append("")
        
        # 里程碑状态
        lines.append("## 里程碑状态\n")
        for ms in sorted(self.milestones.values(), key=lambda m: m.date):
            status = "✅ 完成" if ms.status == "completed" else "⏳ 进行中" if ms.status == "in_progress" else "🔘 待开始"
            lines.append(f"- **{ms.name}** ({ms.id}): {status} (目标: {ms.date})")
        
        lines.append("")
        
        # 即将执行的高优先级任务
        lines.append("## 即将执行的高优先级任务\n")
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        for task in ready[:10]:
            rigor = f"[{task.rigor_level.value}]" if task.rigor_level else "[N/A]"
            lines.append(f"- {task.id} {rigor}: {task.title}")
        
        return "\n".join(lines)
    
    def generate_rigor_escalation_plan(self) -> str:
        """生成严格性提升计划摘要"""
        lines = []
        lines.append("# 严格性提升计划摘要")
        lines.append(f"\n生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        
        for conj in [1, 2]:
            lines.append(f"\n## 猜想{conj} 提升路径\n")
            
            # L4→L3
            lines.append("### L4 → L3（理论框架建立）\n")
            l4_l3_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L3]
            for task in l4_l3_tasks:
                status = "✅" if task.status == TaskStatus.COMPLETED else "🔄" if task.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS] else "⬜"
                lines.append(f"- {status} {task.id}: {task.title}")
            
            # L3→L2
            lines.append("\n### L3 → L2（严格化与计算验证）\n")
            l3_l2_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L2]
            for task in l3_l2_tasks:
                status = "✅" if task.status == TaskStatus.COMPLETED else "🔄" if task.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS] else "⬜"
                lines.append(f"- {status} {task.id}: {task.title}")
            
            # L2→L1
            lines.append("\n### L2 → L1（完整证明）\n")
            l2_l1_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L1]
            for task in l2_l1_tasks:
                status = "✅" if task.status == TaskStatus.COMPLETED else "🔄" if task.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS] else "⬜"
                lines.append(f"- {status} {task.id}: {task.title}")
        
        return "\n".join(lines)


def main():
    """主入口"""
    controller = Phase2ExecutionController()
    
    # 显示初始仪表板
    print(controller.get_dashboard())
    
    # 保存初始状态
    controller.save_tasks()
    
    # 生成报告
    report = controller.generate_report()
    with open("logs/phase2_initial_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 生成提升计划摘要
    plan = controller.generate_rigor_escalation_plan()
    with open("logs/rigor_escalation_summary.md", 'w', encoding='utf-8') as f:
        f.write(plan)
    
    print("\n初始报告已保存到 logs/phase2_initial_report.md")
    print("提升计划摘要已保存到 logs/rigor_escalation_summary.md")
    print("\n使用方法:")
    print("  python execution_phase2.py --dashboard  # 显示仪表板")
    print("  python execution_phase2.py --report     # 生成完整报告")
    print("  python execution_phase2.py --plan       # 显示提升计划")
    print("  python execution_phase2.py --run        # 启动执行循环")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        controller = Phase2ExecutionController()
        
        if sys.argv[1] == "--dashboard":
            print(controller.get_dashboard())
        elif sys.argv[1] == "--report":
            report = controller.generate_report()
            print(report)
            with open("logs/phase2_report.md", 'w', encoding='utf-8') as f:
                f.write(report)
        elif sys.argv[1] == "--plan":
            plan = controller.generate_rigor_escalation_plan()
            print(plan)
        elif sys.argv[1] == "--run":
            controller.run()
        elif sys.argv[1].startswith("--complete-"):
            task_id = sys.argv[1][11:]
            if task_id in controller.tasks:
                controller.complete_task(controller.tasks[task_id])
                print(f"任务 {task_id} 已标记为完成")
            else:
                print(f"任务不存在: {task_id}")
        else:
            main()
    else:
        main()

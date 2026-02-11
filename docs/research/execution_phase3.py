#!/usr/bin/env python3
"""
Phase 3 研究执行控制器
专门用于L2→L1严格证明阶段的任务追踪和管理

基于 execution_phase2.py，专门针对Phase 3任务优化
- 新增L1证明任务管理
- 专家咨询追踪
- 论文写作进度
- 里程碑倒计时
"""

import yaml
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum
import heapq

class TaskStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskType(Enum):
    PROVE = "prove"  # Phase 3核心任务类型：严格证明
    WRITE = "write"
    RESEARCH = "research"
    CONSULT = "consult"  # Phase 3新增：专家咨询
    SETUP = "setup"
    SYNTHESIZE = "synthesize"
    IMPLEMENTATION = "implementation"  # 数值实现/计算任务

class RigorLevel(Enum):
    L1 = "L1"  # 完整证明
    L2 = "L2"  # 严格框架+计算验证
    L3 = "L3"  # 启发式+强数值证据
    L4 = "L4"  # 猜想/推测

class ConsultationStatus(Enum):
    """专家咨询状态"""
    PLANNED = "planned"
    CONTACTED = "contacted"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    FEEDBACK_INTEGRATED = "feedback_integrated"

@dataclass
class ExpertConsultation:
    """专家咨询记录"""
    expert_name: str
    institution: str
    specialty: str
    status: ConsultationStatus = ConsultationStatus.PLANNED
    contact_date: Optional[str] = None
    meeting_date: Optional[str] = None
    feedback_received: bool = False
    feedback_summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    integrated_into_tasks: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "expert_name": self.expert_name,
            "institution": self.institution,
            "specialty": self.specialty,
            "status": self.status.value,
            "contact_date": self.contact_date,
            "meeting_date": self.meeting_date,
            "feedback_received": self.feedback_received,
            "feedback_summary": self.feedback_summary,
            "recommendations": self.recommendations,
            "integrated_into_tasks": self.integrated_into_tasks
        }

@dataclass
class Task:
    id: str
    direction: str
    phase: int = 3  # Phase 3固定
    title: str = ""
    type: TaskType = TaskType.RESEARCH
    priority: int = 50
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    checkpoints: List[str] = field(default_factory=list)
    estimated_effort: str = "12w"  # Phase 3任务周期较长
    actual_effort: str = ""
    milestone: bool = False
    created: str = ""
    completed: str = ""
    rigor_level: Optional[RigorLevel] = None
    conjecture: Optional[int] = None  # 1 or 2
    # Phase 3扩展字段
    started: str = ""  # 任务开始日期
    progress: str = ""  # 任务进度描述
    description: str = ""  # 任务详细描述
    effort: str = ""  # 替代estimated_effort的字段
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = TaskType(self.type)
        if isinstance(self.status, str):
            # 处理大小写不敏感的状态
            status_str = self.status.upper() if isinstance(self.status, str) else self.status
            if status_str == 'ACTIVE':
                self.status = TaskStatus.ACTIVE
            else:
                self.status = TaskStatus(self.status)
        if isinstance(self.rigor_level, str):
            self.rigor_level = RigorLevel(self.rigor_level)
    
    @property
    def priority_score(self) -> int:
        """计算动态优先级分数"""
        score = self.priority
        
        # 里程碑任务加权
        if self.milestone:
            score += 25
            
        # 依赖就绪加权
        if self.status == TaskStatus.PENDING and self.dependencies:
            score += 10
            
        # L1证明任务额外加权（Phase 3核心）
        if self.rigor_level == RigorLevel.L1:
            score += 20
            
        # 专家咨询任务加权（影响后续证明）
        if self.type == TaskType.CONSULT:
            score += 15
            
        return score
    
    @property
    def estimated_weeks(self) -> int:
        """从estimated_effort解析周数"""
        try:
            if self.estimated_effort.endswith('w'):
                return int(self.estimated_effort[:-1])
            return 12  # 默认值
        except:
            return 12
    
    def to_dict(self) -> Dict:
        result = {
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
        # 只在有值时添加可选字段
        if self.started:
            result["started"] = self.started
        if self.progress:
            result["progress"] = self.progress
        if self.description:
            result["description"] = self.description
        if self.effort:
            result["effort"] = self.effort
        return result

@dataclass
class Milestone:
    """Phase 3里程碑"""
    id: str
    name: str
    date: str
    tasks: List[str]
    status: str = "pending"
    description: str = ""
    note: str = ""
    progress: Dict = field(default_factory=dict)  # 进度详情
    
    def to_dict(self) -> Dict:
        result = {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "tasks": self.tasks,
            "status": self.status,
            "description": self.description,
            "note": self.note
        }
        if self.progress:
            result["progress"] = self.progress
        return result
    
    @property
    def days_until(self) -> int:
        """计算距离里程碑还有多少天"""
        try:
            milestone_date = datetime.strptime(self.date, '%Y-%m-%d')
            today = datetime.now()
            delta = milestone_date - today
            return delta.days
        except:
            return -1

class Phase3ExecutionController:
    """Phase 3研究执行控制器 - L2→L1严格证明专用"""
    
    def __init__(self, tasks_file: str = "tasks/phase3_tasks.yaml"):
        self.tasks_file = Path(tasks_file)
        self.tasks: Dict[str, Task] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.expert_consultations: Dict[str, ExpertConsultation] = {}
        self.direction_weights = {
            "kleinian": 40,
            "padic": 35,
            "maass": 25,
            "shared": 30
        }
        self.max_parallel = 3  # Phase 3减少并行，专注深度
        self.running = False
        
        # Phase 3进度追踪
        self.rigor_progress = {
            1: {"L4": True, "L3": True, "L2": True, "L1": False},  # 猜想1
            2: {"L4": True, "L3": True, "L2": True, "L1": False}   # 猜想2
        }
        
        # 论文写作进度
        self.writing_progress = {
            "conjecture_1_paper": {"status": "not_started", "completion": 0},
            "conjecture_2_paper": {"status": "not_started", "completion": 0},
            "unified_overview": {"status": "not_started", "completion": 0}
        }
        
        # 统计
        self.stats = {
            "tasks_created": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "expert_consultations_completed": 0,
            "proof_pages_written": 0,
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
        self.initialize_expert_consultations()
    
    def initialize_expert_consultations(self):
        """初始化专家咨询记录"""
        experts = [
            ("Robert Benedetto", "Amherst College", "p-adic dynamics"),
            ("Juan Rivera-Letelier", "University of Rochester", "arithmetic dynamics"),
            ("Richard Taylor", "Stanford University", "Langlands program"),
            ("Peter Sarnak", "IAS/Princeton", "automorphic forms"),
            ("Curt McMullen", "Harvard University", "complex dynamics, thermodynamic formalism")
        ]
        
        for name, institution, specialty in experts:
            key = f"{name.lower().replace(' ', '_')}"
            self.expert_consultations[key] = ExpertConsultation(
                expert_name=name,
                institution=institution,
                specialty=specialty
            )
    
    def load_tasks(self):
        """加载Phase 3任务数据库"""
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
        
        print(f"已加载 {len(self.tasks)} 个Phase 3任务")
        print(f"已加载 {len(self.milestones)} 个里程碑")
        print(f"已配置 {len(self.expert_consultations)} 个专家咨询")
    
    def save_tasks(self):
        """保存任务状态"""
        data = {
            "meta": {
                "version": "3.0",
                "last_updated": datetime.now().isoformat(),
                "total_tasks": len(self.tasks),
                "phase": 3,
                "phase_name": "L2→L1严格证明阶段"
            },
            "global": {
                "direction_weights": self.direction_weights,
                "execution_mode": "rigorous",
                "max_parallel_tasks": self.max_parallel,
                "rigor_target": {
                    "conjecture_1": {"current": "L2", "target": "L1"},
                    "conjecture_2": {"current": "L2", "target": "L1"}
                }
            },
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "milestones": [ms.to_dict() for ms in self.milestones.values()],
            "expert_consultations": {
                k: v.to_dict() for k, v in self.expert_consultations.items()
            },
            "writing_progress": self.writing_progress,
            "active_tasks": [t.id for t in self.tasks.values() if t.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS]],
            "completed_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.COMPLETED],
            "blocked_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]
        }
        
        # 保存带时间戳的快照
        snapshot_file = Path(f"snapshots/phase3_snapshot_{datetime.now():%Y%m%d_%H%M%S}.json")
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
        """计算任务动态优先级（Phase 3优化版）"""
        score = task.priority
        
        # 1. 方向战略权重
        score += self.direction_weights.get(task.direction, 30)
        
        # 2. 阻塞影响
        blocked_count = len(task.blocks)
        score += min(25, blocked_count * 5)
        
        # 3. 里程碑加权
        if task.milestone:
            score += 20
        
        # 4. 严格性级别加权（L1任务优先级最高）
        if task.rigor_level == RigorLevel.L1:
            score += 20
        
        # 5. 专家咨询任务加权（影响后续所有证明）
        if task.type == TaskType.CONSULT:
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
        task.status = TaskStatus.IN_PROGRESS if task.type in [TaskType.PROVE, TaskType.RESEARCH] else TaskStatus.ACTIVE
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
        
        # 更新严格性进度
        if task.rigor_level == RigorLevel.L1 and task.conjecture:
            # 检查是否完成该猜想的所有L1任务
            conj_l1_tasks = [t for t in self.tasks.values() 
                            if t.conjecture == task.conjecture and t.rigor_level == RigorLevel.L1]
            conj_l1_completed = [t for t in conj_l1_tasks if t.status == TaskStatus.COMPLETED]
            if len(conj_l1_completed) == len(conj_l1_tasks):
                self.rigor_progress[task.conjecture]["L1"] = True
                self.log(f"🎉 猜想{task.conjecture} L2→L1完成!")
        
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
    
    def get_milestone_countdown(self) -> str:
        """生成里程碑倒计时"""
        lines = []
        lines.append("📅 里程碑倒计时:")
        lines.append("")
        
        for ms in sorted(self.milestones.values(), key=lambda m: m.date):
            if ms.status == "completed":
                continue
                
            days = ms.days_until
            if days >= 0:
                if days <= 30:
                    urgency = "🔴"
                elif days <= 90:
                    urgency = "🟡"
                else:
                    urgency = "🟢"
                lines.append(f"  {urgency} {ms.id}: {ms.name}")
                lines.append(f"     目标: {ms.date} ({days}天)")
            else:
                lines.append(f"  ⚠️ {ms.id}: {ms.name} (已过期)")
        
        return "\n".join(lines)
    
    def update_expert_consultation(self, expert_key: str, status: ConsultationStatus, 
                                    meeting_date: Optional[str] = None,
                                    feedback_summary: str = "",
                                    recommendations: List[str] = None):
        """更新专家咨询状态"""
        if expert_key not in self.expert_consultations:
            self.log(f"专家不存在: {expert_key}")
            return
            
        consultation = self.expert_consultations[expert_key]
        consultation.status = status
        
        if meeting_date:
            consultation.meeting_date = meeting_date
        if feedback_summary:
            consultation.feedback_summary = feedback_summary
            consultation.feedback_received = True
        if recommendations:
            consultation.recommendations = recommendations
            
        if status == ConsultationStatus.COMPLETED:
            self.stats["expert_consultations_completed"] += 1
            self.log(f"专家咨询完成: {consultation.expert_name}")
        
        self.save_tasks()
    
    def get_expert_consultation_status(self) -> str:
        """生成专家咨询状态报告"""
        lines = []
        lines.append("👥 专家咨询状态:")
        lines.append("")
        
        # 按专业领域分组
        padic_experts = [c for c in self.expert_consultations.values() if "p-adic" in c.specialty or "arithmetic" in c.specialty]
        langlands_experts = [c for c in self.expert_consultations.values() if "Langlands" in c.specialty or "automorphic" in c.specialty]
        thermo_experts = [c for c in self.expert_consultations.values() if "complex" in c.specialty or "thermodynamic" in c.specialty]
        
        lines.append("  p-adic方向:")
        for c in padic_experts:
            status_icon = "✅" if c.status == ConsultationStatus.COMPLETED else "🔄" if c.status == ConsultationStatus.SCHEDULED else "⬜"
            lines.append(f"    {status_icon} {c.expert_name} ({c.institution})")
        
        lines.append("")
        lines.append("  Langlands方向:")
        for c in langlands_experts:
            status_icon = "✅" if c.status == ConsultationStatus.COMPLETED else "🔄" if c.status == ConsultationStatus.SCHEDULED else "⬜"
            lines.append(f"    {status_icon} {c.expert_name} ({c.institution})")
        
        lines.append("")
        lines.append("  热力学形式:")
        for c in thermo_experts:
            status_icon = "✅" if c.status == ConsultationStatus.COMPLETED else "🔄" if c.status == ConsultationStatus.SCHEDULED else "⬜"
            lines.append(f"    {status_icon} {c.expert_name} ({c.institution})")
        
        return "\n".join(lines)
    
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
        lines.append("Phase 3 L2→L1严格证明仪表板")
        lines.append(f"更新时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lines.append("=" * 70)
        lines.append("")
        
        # 猜想严格性进展
        lines.append("📊 L2→L1证明进展:")
        lines.append("")
        for conj in [1, 2]:
            conj_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L1]
            completed = len([t for t in conj_tasks if t.status == TaskStatus.COMPLETED])
            total = len(conj_tasks)
            progress = (completed / total * 100) if total > 0 else 0
            bar = "█" * int(progress / 5) + "░" * (20 - int(progress / 5))
            lines.append(f"  猜想{conj} L2→L1: [{bar}] {progress:.0f}% ({completed}/{total})")
        
        return "\n".join(lines)
    
    def get_dashboard(self) -> str:
        """生成完整仪表板显示"""
        lines = []
        lines.append(self.get_rigor_dashboard())
        lines.append("")
        
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
        
        # 里程碑倒计时
        lines.append(self.get_milestone_countdown())
        lines.append("")
        
        # 专家咨询状态
        lines.append(self.get_expert_consultation_status())
        lines.append("")
        
        # 高优先级就绪任务
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        lines.append("🔥 高优先级就绪任务 (Top 5):")
        for i, task in enumerate(ready[:5], 1):
            priority = self.calculate_priority(task)
            rigor = f"[{task.rigor_level.value}]" if task.rigor_level else "[N/A]"
            task_type = "📝" if task.type == TaskType.WRITE else "📐" if task.type == TaskType.PROVE else "👥" if task.type == TaskType.CONSULT else "🔬"
            lines.append(f"  {i}. {task_type} {task.id} {rigor} {task.title[:30]}... (P:{priority})")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[Phase3] [{timestamp}] {message}"
        
        # 输出到控制台
        print(log_entry)
        
        # 保存到日志文件
        log_file = Path(f"logs/phase3_execution_{datetime.now():%Y-%m-%d}.log")
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
        
        self.log("Phase 3 执行控制器启动 - L2→L1严格证明阶段")
        
        try:
            while self.running:
                self.run_cycle()
                cycle_count += 1
                
                if cycles and cycle_count >= cycles:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log("Phase 3 执行控制器停止")
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
        """生成Phase 3执行报告"""
        lines = []
        lines.append("# Phase 3 L2→L1严格证明执行报告")
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
        lines.append(f"- 专家咨询完成: {self.stats['expert_consultations_completed']}/{len(self.expert_consultations)}")
        lines.append("")
        
        # 猜想进展
        lines.append("## 猜想证明进展\n")
        for conj in [1, 2]:
            conj_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L1]
            conj_completed = len([t for t in conj_tasks if t.status == TaskStatus.COMPLETED])
            if conj_tasks:
                pct = conj_completed / len(conj_tasks) * 100
                lines.append(f"- **猜想{conj} L1证明**: {conj_completed}/{len(conj_tasks)} ({pct:.1f}%)")
        
        lines.append("")
        
        # 里程碑状态
        lines.append("## 里程碑状态\n")
        for ms in sorted(self.milestones.values(), key=lambda m: m.date):
            status = "✅ 完成" if ms.status == "completed" else "⏳ 进行中" if ms.status == "in_progress" else "🔘 待开始"
            days = ms.days_until
            days_str = f" ({days}天)" if days >= 0 else " (已过期)"
            lines.append(f"- **{ms.name}** ({ms.id}): {status} (目标: {ms.date}{days_str})")
        
        lines.append("")
        
        # 专家咨询状态
        lines.append("## 专家咨询状态\n")
        for key, consultation in self.expert_consultations.items():
            status = "✅" if consultation.status == ConsultationStatus.COMPLETED else "🔄" if consultation.status == ConsultationStatus.SCHEDULED else "⬜"
            lines.append(f"- {status} **{consultation.expert_name}** ({consultation.institution}): {consultation.specialty}")
        
        lines.append("")
        
        # 即将执行的高优先级任务
        lines.append("## 即将执行的高优先级任务\n")
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        for task in ready[:10]:
            rigor = f"[{task.rigor_level.value}]" if task.rigor_level else "[N/A]"
            lines.append(f"- {task.id} {rigor}: {task.title}")
        
        return "\n".join(lines)
    
    def generate_l1_proof_plan(self) -> str:
        """生成L1证明计划摘要"""
        lines = []
        lines.append("# L2→L1严格证明计划")
        lines.append(f"\n生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        
        for conj in [1, 2]:
            lines.append(f"\n## 猜想{conj} L2→L1证明路径\n")
            
            # 获取所有L1任务
            l1_tasks = [t for t in self.tasks.values() if t.conjecture == conj and t.rigor_level == RigorLevel.L1]
            l1_tasks.sort(key=lambda t: t.priority, reverse=True)
            
            # 按依赖关系排序（拓扑排序近似）
            for task in l1_tasks:
                status = "✅" if task.status == TaskStatus.COMPLETED else "🔄" if task.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS] else "⬜"
                deps = f" (依赖: {', '.join(task.dependencies)})" if task.dependencies else ""
                lines.append(f"- {status} **{task.id}**: {task.title}{deps}")
                lines.append(f"  预计: {task.estimated_effort}")
                lines.append("")
        
        # 关键依赖：专家咨询
        lines.append("\n## 关键支持：专家咨询\n")
        lines.append("专家咨询是所有L1证明的前提条件:\n")
        for key, consultation in self.expert_consultations.items():
            if consultation.status != ConsultationStatus.COMPLETED:
                lines.append(f"- ⬜ **{consultation.expert_name}**: {consultation.specialty}")
        
        return "\n".join(lines)


def main():
    """主入口"""
    controller = Phase3ExecutionController()
    
    # 显示初始仪表板
    print(controller.get_dashboard())
    
    # 保存初始状态
    controller.save_tasks()
    
    # 生成报告
    report = controller.generate_report()
    with open("logs/phase3_initial_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 生成L1证明计划
    plan = controller.generate_l1_proof_plan()
    with open("logs/l1_proof_plan.md", 'w', encoding='utf-8') as f:
        f.write(plan)
    
    print("\n初始报告已保存到 logs/phase3_initial_report.md")
    print("L1证明计划已保存到 logs/l1_proof_plan.md")
    print("\n使用方法:")
    print("  python execution_phase3.py --dashboard  # 显示仪表板")
    print("  python execution_phase3.py --report     # 生成完整报告")
    print("  python execution_phase3.py --plan       # 显示L1证明计划")
    print("  python execution_phase3.py --run        # 启动执行循环")
    print("  python execution_phase3.py --consult <expert_key> <status>  # 更新专家咨询状态")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        controller = Phase3ExecutionController()
        
        if sys.argv[1] == "--dashboard":
            print(controller.get_dashboard())
        elif sys.argv[1] == "--report":
            report = controller.generate_report()
            print(report)
            with open("logs/phase3_report.md", 'w', encoding='utf-8') as f:
                f.write(report)
        elif sys.argv[1] == "--plan":
            plan = controller.generate_l1_proof_plan()
            print(plan)
        elif sys.argv[1] == "--run":
            controller.run()
        elif sys.argv[1] == "--consult" and len(sys.argv) >= 4:
            expert_key = sys.argv[2]
            status = ConsultationStatus(sys.argv[3])
            controller.update_expert_consultation(expert_key, status)
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

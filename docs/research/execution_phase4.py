#!/usr/bin/env python3
"""
Phase 4 研究执行控制器
专门用于专家咨询与期刊投稿阶段的任务追踪和管理

基于 execution_phase3.py，专门针对Phase 4任务优化
- 专家联系状态追踪
- 论文写作进度管理
- 投稿流程管理
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
    PREPARE = "prepare"  # Phase 4新增：准备材料
    CONSULT = "consult"  # 专家咨询
    SYNTHESIZE = "synthesize"  # 综合反馈
    WRITE = "write"  # 论文撰写
    SETUP = "setup"  # 准备投稿
    SUBMIT = "submit"  # 正式投稿
    RESEARCH = "research"

class ConsultationStatus(Enum):
    """专家咨询状态"""
    PLANNED = "planned"
    CONTACTED = "contacted"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    FEEDBACK_INTEGRATED = "feedback_integrated"

class SubmissionStatus(Enum):
    """投稿状态"""
    NOT_STARTED = "not_started"
    PREPARING = "preparing"
    READY = "ready"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    REVISION_REQUESTED = "revision_requested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

@dataclass
class ExpertConsultation:
    """专家咨询记录"""
    expert_name: str = ""
    institution: str = ""
    specialty: str = ""
    name: str = ""  # Alias for expert_name
    status: ConsultationStatus = ConsultationStatus.PLANNED
    contact_date: Optional[str] = None
    meeting_date: Optional[str] = None
    feedback_received: bool = False
    feedback_summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    integrated_into_tasks: List[str] = field(default_factory=list)
    task_id: str = ""
    
    def __post_init__(self):
        # Handle name/expert_name alias
        if self.name and not self.expert_name:
            self.expert_name = self.name
        elif self.expert_name and not self.name:
            self.name = self.expert_name
            
    def to_dict(self) -> Dict:
        return {
            "name": self.name or self.expert_name,
            "expert_name": self.expert_name or self.name,
            "institution": self.institution,
            "specialty": self.specialty,
            "status": self.status.value,
            "contact_date": self.contact_date,
            "meeting_date": self.meeting_date,
            "feedback_received": self.feedback_received,
            "feedback_summary": self.feedback_summary,
            "recommendations": self.recommendations,
            "integrated_into_tasks": self.integrated_into_tasks,
            "task_id": self.task_id
        }

@dataclass
class SubmissionTracking:
    """投稿追踪记录"""
    journal: str
    submission_system: str
    manuscript_number: Optional[str] = None
    submission_date: Optional[str] = None
    current_status: SubmissionStatus = SubmissionStatus.NOT_STARTED
    status_history: List[Dict] = field(default_factory=list)
    suggested_reviewers: List[Dict] = field(default_factory=list)
    excluded_reviewers: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "journal": self.journal,
            "submission_system": self.submission_system,
            "manuscript_number": self.manuscript_number,
            "submission_date": self.submission_date,
            "current_status": self.current_status.value,
            "status_history": self.status_history,
            "suggested_reviewers": self.suggested_reviewers,
            "excluded_reviewers": self.excluded_reviewers
        }

@dataclass
class Task:
    id: str
    direction: str
    phase: int = 4  # Phase 4固定
    title: str = ""
    type: TaskType = TaskType.RESEARCH
    priority: int = 50
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = field(default_factory=list)
    blocks: List[str] = field(default_factory=list)
    deliverables: List[str] = field(default_factory=list)
    checkpoints: List[str] = field(default_factory=list)
    estimated_effort: str = "4w"
    actual_effort: str = ""
    milestone: bool = False
    created: str = ""
    completed: str = ""
    # Phase 4扩展字段
    started: str = ""
    progress: str = ""
    description: str = ""
    expert_category: str = ""
    section: int = 0
    conjecture: Optional[int] = None
    journal: str = ""
    expert_info: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if isinstance(self.type, str):
            self.type = TaskType(self.type)
        if isinstance(self.status, str):
            status_str = self.status.upper() if isinstance(self.status, str) else self.status
            if status_str == 'ACTIVE':
                self.status = TaskStatus.ACTIVE
            else:
                try:
                    self.status = TaskStatus(self.status)
                except:
                    self.status = TaskStatus.PENDING
    
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
            
        # 投稿任务最高优先级
        if self.type == TaskType.SUBMIT:
            score += 30
            
        # 专家咨询任务加权（影响论文撰写）
        if self.type == TaskType.CONSULT:
            score += 20
            
        # 论文撰写任务加权
        if self.type == TaskType.WRITE and self.conjecture:
            score += 15
            
        return score
    
    @property
    def estimated_weeks(self) -> int:
        """从estimated_effort解析周数"""
        try:
            if self.estimated_effort.endswith('w'):
                return int(self.estimated_effort[:-1])
            return 4
        except:
            return 4
    
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
            "completed": self.completed
        }
        if self.started:
            result["started"] = self.started
        if self.progress:
            result["progress"] = self.progress
        if self.description:
            result["description"] = self.description
        if self.expert_category:
            result["expert_category"] = self.expert_category
        if self.section:
            result["section"] = self.section
        if self.conjecture:
            result["conjecture"] = self.conjecture
        if self.journal:
            result["journal"] = self.journal
        if self.expert_info:
            result["expert_info"] = self.expert_info
        return result

@dataclass
class Milestone:
    """Phase 4里程碑"""
    id: str
    name: str
    date: str
    tasks: List[str]
    status: str = "pending"
    description: str = ""
    note: str = ""
    deliverables: List[str] = field(default_factory=list)
    expected_duration: str = ""
    
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
        if self.deliverables:
            result["deliverables"] = self.deliverables
        if self.expected_duration:
            result["expected_duration"] = self.expected_duration
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

class Phase4ExecutionController:
    """Phase 4研究执行控制器 - 专家咨询与期刊投稿专用"""
    
    def __init__(self, tasks_file: str = "tasks/phase4_tasks.yaml"):
        self.tasks_file = Path(tasks_file)
        self.tasks: Dict[str, Task] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.expert_consultations: Dict[str, ExpertConsultation] = {}
        self.submission_tracking: Optional[SubmissionTracking] = None
        self.direction_weights = {
            "kleinian": 40,
            "padic": 35,
            "maass": 25,
            "shared": 30
        }
        self.max_parallel = 4
        self.running = False
        
        # 论文写作进度
        self.paper_writing_progress = {
            "introduction": {"status": "not_started", "completion": 0},
            "conjecture1_proof": {"status": "not_started", "completion": 0},
            "conjecture2_proof": {"status": "not_started", "completion": 0},
            "unified_framework": {"status": "not_started", "completion": 0},
            "numerical_verification": {"status": "not_started", "completion": 0},
            "integration": {"status": "not_started", "completion": 0}
        }
        
        # 统计
        self.stats = {
            "tasks_created": 0,
            "tasks_completed": 0,
            "tasks_failed": 0,
            "expert_consultations_completed": 0,
            "expert_consultations_scheduled": 0,
            "paper_sections_completed": 0,
            "submission_ready": False,
            "direction_progress": {
                "kleinian": 0,
                "padic": 0,
                "maass": 0,
                "shared": 0
            }
        }
        
        self.load_tasks()
    
    def load_tasks(self):
        """加载Phase 4任务数据库"""
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
            
        # 加载专家咨询
        for key, expert_data in data.get('expert_consultations', {}).items():
            self.expert_consultations[key] = ExpertConsultation(**expert_data)
            
        # 加载投稿追踪
        sub_data = data.get('submission_tracking', {})
        if sub_data:
            self.submission_tracking = SubmissionTracking(
                journal=sub_data.get('journal', 'Annals of Mathematics'),
                submission_system=sub_data.get('submission_system', 'ScholarOne Manuscripts')
            )
            
        self.direction_weights = data.get('global', {}).get('direction_weights', self.direction_weights)
        self.stats["tasks_created"] = len(self.tasks)
        
        # 初始化进度
        for direction in ["kleinian", "padic", "maass", "shared"]:
            self.update_direction_progress(direction)
        
        # 更新专家咨询统计
        self.update_expert_stats()
        
        print(f"已加载 {len(self.tasks)} 个Phase 4任务")
        print(f"已加载 {len(self.milestones)} 个里程碑")
        print(f"已配置 {len(self.expert_consultations)} 个专家咨询")
    
    def save_tasks(self):
        """保存任务状态"""
        data = {
            "meta": {
                "version": "4.0",
                "last_updated": datetime.now().isoformat(),
                "total_tasks": len(self.tasks),
                "phase": 4,
                "phase_name": "专家咨询与期刊投稿阶段"
            },
            "global": {
                "direction_weights": self.direction_weights,
                "execution_mode": "publication_focused",
                "max_parallel_tasks": self.max_parallel
            },
            "tasks": [task.to_dict() for task in self.tasks.values()],
            "milestones": [ms.to_dict() for ms in self.milestones.values()],
            "expert_consultations": {
                k: v.to_dict() for k, v in self.expert_consultations.items()
            },
            "submission_tracking": self.submission_tracking.to_dict() if self.submission_tracking else {},
            "active_tasks": [t.id for t in self.tasks.values() if t.status in [TaskStatus.ACTIVE, TaskStatus.IN_PROGRESS]],
            "completed_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.COMPLETED],
            "blocked_tasks": [t.id for t in self.tasks.values() if t.status == TaskStatus.BLOCKED]
        }
        
        # 保存带时间戳的快照
        snapshot_file = Path(f"snapshots/phase4_snapshot_{datetime.now():%Y%m%d_%H%M%S}.json")
        snapshot_file.parent.mkdir(exist_ok=True)
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 更新主文件
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    
    def update_expert_stats(self):
        """更新专家咨询统计"""
        completed = sum(1 for c in self.expert_consultations.values() 
                       if c.status == ConsultationStatus.COMPLETED)
        scheduled = sum(1 for c in self.expert_consultations.values() 
                       if c.status in [ConsultationStatus.SCHEDULED, ConsultationStatus.CONTACTED])
        self.stats["expert_consultations_completed"] = completed
        self.stats["expert_consultations_scheduled"] = scheduled
    
    def calculate_priority(self, task: Task) -> int:
        """计算任务动态优先级（Phase 4优化版）"""
        score = task.priority
        
        # 1. 方向战略权重
        score += self.direction_weights.get(task.direction, 30)
        
        # 2. 阻塞影响
        blocked_count = len(task.blocks)
        score += min(25, blocked_count * 5)
        
        # 3. 里程碑加权
        if task.milestone:
            score += 20
        
        # 4. 投稿任务优先级最高
        if task.type == TaskType.SUBMIT:
            score += 30
        
        # 5. 专家咨询任务加权（影响后续所有任务）
        if task.type == TaskType.CONSULT:
            score += 20
            
        # 6. 论文撰写任务加权
        if task.type == TaskType.WRITE and task.conjecture:
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
    
    def select_next_tasks(self, n: int = 4) -> List[Task]:
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
        task.status = TaskStatus.IN_PROGRESS if task.type in [TaskType.WRITE, TaskType.RESEARCH] else TaskStatus.ACTIVE
        task.started = datetime.now().isoformat()
        self.save_tasks()
        self.log(f"开始任务: {task.id} - {task.title}")
    
    def complete_task(self, task: Task, actual_effort: str = ""):
        """标记任务完成"""
        task.status = TaskStatus.COMPLETED
        task.completed = datetime.now().isoformat()
        if actual_effort:
            task.actual_effort = actual_effort
        
        self.stats["tasks_completed"] += 1
        self.update_direction_progress(task.direction)
        
        # 更新专家咨询统计
        if task.type == TaskType.CONSULT:
            self.update_expert_stats()
            
        # 更新论文写作进度
        if task.type == TaskType.WRITE and task.conjecture:
            self.paper_writing_progress[f"conjecture{task.conjecture}_proof"]["status"] = "completed"
            self.paper_writing_progress[f"conjecture{task.conjecture}_proof"]["completion"] = 100
            
        # 更新投稿状态
        if task.type == TaskType.SUBMIT:
            self.stats["submission_ready"] = True
            if self.submission_tracking:
                self.submission_tracking.current_status = SubmissionStatus.SUBMITTED
                self.submission_tracking.submission_date = datetime.now().isoformat()
        
        # 检查里程碑
        self.check_milestones()
        
        # 立即保存YAML
        self.save_tasks()
        
        self.log(f"完成任务: {task.id}")
        
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
            self.log(f"专家咨询完成: {consultation.expert_name}")
        
        self.update_expert_stats()
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
            c_status = c.status if isinstance(c.status, ConsultationStatus) else ConsultationStatus(c.status)
            status_icon = "✅" if c_status == ConsultationStatus.COMPLETED else "🔄" if c_status == ConsultationStatus.SCHEDULED else "⬜"
            feedback = "📧" if c.feedback_received else ""
            expert_name = c.expert_name or c.name
            lines.append(f"    {status_icon} {expert_name} ({c.institution}) {feedback}")
        
        lines.append("")
        lines.append("  Langlands方向:")
        for c in langlands_experts:
            c_status = c.status if isinstance(c.status, ConsultationStatus) else ConsultationStatus(c.status)
            status_icon = "✅" if c_status == ConsultationStatus.COMPLETED else "🔄" if c_status == ConsultationStatus.SCHEDULED else "⬜"
            feedback = "📧" if c.feedback_received else ""
            expert_name = c.expert_name or c.name
            lines.append(f"    {status_icon} {expert_name} ({c.institution}) {feedback}")
        
        lines.append("")
        lines.append("  热力学形式:")
        for c in thermo_experts:
            c_status = c.status if isinstance(c.status, ConsultationStatus) else ConsultationStatus(c.status)
            status_icon = "✅" if c_status == ConsultationStatus.COMPLETED else "🔄" if c_status == ConsultationStatus.SCHEDULED else "⬜"
            feedback = "📧" if c.feedback_received else ""
            expert_name = c.expert_name or c.name
            lines.append(f"    {status_icon} {expert_name} ({c.institution}) {feedback}")
        
        # 统计
        total = len(self.expert_consultations)
        completed = self.stats["expert_consultations_completed"]
        scheduled = self.stats["expert_consultations_scheduled"]
        lines.append("")
        lines.append(f"  进度: {completed}/{total} 完成, {scheduled} 已安排")
        
        return "\n".join(lines)
    
    def get_paper_writing_status(self) -> str:
        """生成论文写作进度报告"""
        lines = []
        lines.append("📝 论文写作进度:")
        lines.append("")
        
        # 统计已完成章节
        completed = sum(1 for v in self.paper_writing_progress.values() if v["status"] == "completed")
        total = len(self.paper_writing_progress)
        progress_pct = (completed / total * 100) if total > 0 else 0
        bar = "█" * int(progress_pct / 5) + "░" * (20 - int(progress_pct / 5))
        lines.append(f"  总体进度: [{bar}] {progress_pct:.0f}% ({completed}/{total})")
        lines.append("")
        
        for section, info in self.paper_writing_progress.items():
            status_icon = "✅" if info["status"] == "completed" else "🔄" if info["status"] == "in_progress" else "⬜"
            bar = "█" * (info["completion"] // 5) + "░" * (20 - info["completion"] // 5)
            lines.append(f"  {status_icon} {section:25} [{bar}] {info['completion']}%")
        
        return "\n".join(lines)
    
    def get_submission_status(self) -> str:
        """生成投稿状态报告"""
        lines = []
        lines.append("📤 投稿状态:")
        lines.append("")
        
        if self.submission_tracking:
            st = self.submission_tracking
            status_icon = {
                SubmissionStatus.NOT_STARTED: "⬜",
                SubmissionStatus.PREPARING: "🔄",
                SubmissionStatus.READY: "📋",
                SubmissionStatus.SUBMITTED: "📤",
                SubmissionStatus.UNDER_REVIEW: "👀",
                SubmissionStatus.ACCEPTED: "✅",
                SubmissionStatus.REJECTED: "❌"
            }.get(st.current_status, "⬜")
            
            lines.append(f"  {status_icon} 目标期刊: {st.journal}")
            lines.append(f"     投稿系统: {st.submission_system}")
            lines.append(f"     当前状态: {st.current_status.value}")
            
            if st.manuscript_number:
                lines.append(f"     稿件编号: {st.manuscript_number}")
            if st.submission_date:
                lines.append(f"     投稿日期: {st.submission_date}")
        else:
            lines.append("  ⬜ 尚未配置投稿追踪")
        
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
    
    def get_dashboard(self) -> str:
        """生成完整仪表板显示"""
        lines = []
        lines.append("=" * 70)
        lines.append("Phase 4 专家咨询与期刊投稿仪表板")
        lines.append(f"更新时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        lines.append("=" * 70)
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
        
        # 论文写作进度
        lines.append(self.get_paper_writing_status())
        lines.append("")
        
        # 投稿状态
        lines.append(self.get_submission_status())
        lines.append("")
        
        # 高优先级就绪任务
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        lines.append("🔥 高优先级就绪任务 (Top 5):")
        for i, task in enumerate(ready[:5], 1):
            priority = self.calculate_priority(task)
            task_type = "📝" if task.type == TaskType.WRITE else "👥" if task.type == TaskType.CONSULT else "📤" if task.type == TaskType.SUBMIT else "🔬"
            lines.append(f"  {i}. {task_type} {task.id} {task.title[:30]}... (P:{priority})")
        
        lines.append("")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[Phase4] [{timestamp}] {message}"
        
        # 输出到控制台
        print(log_entry)
        
        # 保存到日志文件
        log_file = Path(f"logs/phase4_execution_{datetime.now():%Y-%m-%d}.log")
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
        
        self.log("Phase 4 执行控制器启动 - 专家咨询与期刊投稿阶段")
        
        try:
            while self.running:
                self.run_cycle()
                cycle_count += 1
                
                if cycles and cycle_count >= cycles:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.log("Phase 4 执行控制器停止")
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
        """生成Phase 4执行报告"""
        lines = []
        lines.append("# Phase 4 专家咨询与期刊投稿执行报告")
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
            c_status = consultation.status if isinstance(consultation.status, ConsultationStatus) else ConsultationStatus(consultation.status)
            status = "✅" if c_status == ConsultationStatus.COMPLETED else "🔄" if c_status == ConsultationStatus.SCHEDULED else "⬜"
            feedback = " | 📧 已收到反馈" if consultation.feedback_received else ""
            expert_name = consultation.expert_name or consultation.name
            lines.append(f"- {status} **{expert_name}** ({consultation.institution}){feedback}")
        
        lines.append("")
        
        # 论文写作进度
        lines.append("## 论文写作进度\n")
        for section, info in self.paper_writing_progress.items():
            status = "✅ 完成" if info["status"] == "completed" else "🔄 进行中" if info["status"] == "in_progress" else "🔘 待开始"
            lines.append(f"- **{section}**: {status} ({info['completion']}%)")
        
        lines.append("")
        
        # 投稿状态
        lines.append("## 投稿状态\n")
        if self.submission_tracking:
            st = self.submission_tracking
            lines.append(f"- **目标期刊**: {st.journal}")
            lines.append(f"- **当前状态**: {st.current_status.value}")
            if st.manuscript_number:
                lines.append(f"- **稿件编号**: {st.manuscript_number}")
            if st.submission_date:
                lines.append(f"- **投稿日期**: {st.submission_date}")
        
        lines.append("")
        
        # 即将执行的高优先级任务
        lines.append("## 即将执行的高优先级任务\n")
        ready = self.get_ready_tasks()
        ready.sort(key=lambda t: self.calculate_priority(t), reverse=True)
        
        for task in ready[:10]:
            lines.append(f"- {task.id}: {task.title}")
        
        return "\n".join(lines)
    
    def generate_publication_plan(self) -> str:
        """生成发表计划摘要"""
        lines = []
        lines.append("# Phase 4 发表计划")
        lines.append(f"\n生成时间: {datetime.now():%Y-%m-%d %H:%M:%S}")
        
        lines.append("\n## 时间线\n")
        lines.append("```")
        lines.append("2026-02  Phase 4 启动")
        lines.append("  │")
        lines.append("  ▼")
        lines.append("2026-03 ── 2026-04  专家咨询阶段 (M7)")
        lines.append("  │")
        lines.append("  ▼")
        lines.append("2026-05 ── 2026-07  论文撰写阶段 (M8)")
        lines.append("  │")
        lines.append("  ▼")
        lines.append("2026-08  投稿至Annals of Mathematics (M9)")
        lines.append("  │")
        lines.append("  ▼")
        lines.append("2026-09 ── 2027-03  审稿期 (预计6-12个月) (M10)")
        lines.append("  │")
        lines.append("  ▼")
        lines.append("2027-04 ── 2028-01  修改与接受 (M11)")
        lines.append("```")
        
        lines.append("\n## 专家咨询计划\n")
        for key, c in self.expert_consultations.items():
            status_str = c.status.value if isinstance(c.status, ConsultationStatus) else str(c.status)
            lines.append(f"### {c.expert_name or c.name}")
            lines.append(f"- 机构: {c.institution}")
            lines.append(f"- 专业: {c.specialty}")
            lines.append(f"- 当前状态: {status_str}")
            lines.append("")
        
        lines.append("\n## 论文结构\n")
        lines.append("1. 引言 (Introduction)")
        lines.append("2. 背景 (Background)")
        lines.append("3. 猜想1证明: 函子性维数公式")
        lines.append("4. 猜想2证明: 统一压力原理")
        lines.append("5. 统一框架 (Unified Framework)")
        lines.append("6. 数值验证 (Numerical Verification)")
        lines.append("7. 结论与未来方向")
        lines.append("附录: 技术细节")
        
        lines.append("\n## 投稿准备清单\n")
        lines.append("- [ ] 论文PDF (LaTeX生成)")
        lines.append("- [ ] 补充材料 (数据和代码)")
        lines.append("- [ ] 封面信")
        lines.append("- [ ] 推荐审稿人名单")
        lines.append("- [ ] 回避审稿人名单 (如有)")
        lines.append("- [ ] 作者信息和ORCID")
        
        return "\n".join(lines)


def main():
    """主入口"""
    controller = Phase4ExecutionController()
    
    # 显示初始仪表板
    print(controller.get_dashboard())
    
    # 保存初始状态
    controller.save_tasks()
    
    # 生成报告
    report = controller.generate_report()
    with open("logs/phase4_initial_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    # 生成发表计划
    plan = controller.generate_publication_plan()
    with open("logs/publication_plan.md", 'w', encoding='utf-8') as f:
        f.write(plan)
    
    print("\n初始报告已保存到 logs/phase4_initial_report.md")
    print("发表计划已保存到 logs/publication_plan.md")
    print("\n使用方法:")
    print("  python execution_phase4.py --dashboard   # 显示仪表板")
    print("  python execution_phase4.py --report      # 生成完整报告")
    print("  python execution_phase4.py --plan        # 显示发表计划")
    print("  python execution_phase4.py --run         # 启动执行循环")
    print("  python execution_phase4.py --consult <expert_key> <status>  # 更新专家咨询状态")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        controller = Phase4ExecutionController()
        
        if sys.argv[1] == "--dashboard":
            print(controller.get_dashboard())
        elif sys.argv[1] == "--report":
            report = controller.generate_report()
            print(report)
            with open("logs/phase4_report.md", 'w', encoding='utf-8') as f:
                f.write(report)
        elif sys.argv[1] == "--plan":
            plan = controller.generate_publication_plan()
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

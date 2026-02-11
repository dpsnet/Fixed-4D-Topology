#!/usr/bin/env python3
"""
里程碑检查脚本

功能:
- 自动检查任务进度
- 生成进度报告
- 预警延迟风险
- 更新里程碑状态

用法:
    python milestone_checker.py [--report] [--update] [--alert]

选项:
    --report    生成进度报告
    --update    更新里程碑状态
    --alert     检查并发送延迟预警
    --all       执行所有操作
"""

import yaml
import json
import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    ACTIVE = "active"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class RiskLevel(Enum):
    """风险等级枚举"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Task:
    """任务数据结构"""
    id: str
    title: str
    status: TaskStatus
    progress: str
    progress_percentage: Optional[int]
    started: Optional[str]
    completed: Optional[str]
    estimated_effort: str
    milestone: bool
    conjecture: Optional[int]


@dataclass
class Milestone:
    """里程碑数据结构"""
    id: str
    name: str
    description: str
    date: str
    tasks: List[str]
    status: str
    progress: Dict


class MilestoneChecker:
    """里程碑检查器主类"""
    
    def __init__(self, tasks_file: str):
        self.tasks_file = Path(tasks_file)
        self.data = None
        self.tasks: Dict[str, Task] = {}
        self.milestones: Dict[str, Milestone] = {}
        self.load_data()
        
    def load_data(self):
        """加载任务数据"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                self.data = yaml.safe_load(f)
            self._parse_tasks()
            self._parse_milestones()
        except Exception as e:
            print(f"错误: 无法加载任务文件: {e}")
            sys.exit(1)
    
    def _parse_tasks(self):
        """解析任务数据"""
        if 'tasks' not in self.data:
            return
            
        for task_data in self.data['tasks']:
            if isinstance(task_data, dict) and 'id' in task_data:
                # 处理状态值的大小写
                status_str = task_data.get('status', 'pending')
                try:
                    status = TaskStatus(status_str.lower())
                except ValueError:
                    # 如果无法匹配，默认pending
                    status = TaskStatus.PENDING
                
                task = Task(
                    id=task_data['id'],
                    title=task_data.get('title', ''),
                    status=status,
                    progress=task_data.get('progress', ''),
                    progress_percentage=task_data.get('progress_percentage'),
                    started=task_data.get('started'),
                    completed=task_data.get('completed'),
                    estimated_effort=task_data.get('estimated_effort', ''),
                    milestone=task_data.get('milestone', False),
                    conjecture=task_data.get('conjecture')
                )
                self.tasks[task.id] = task
    
    def _parse_milestones(self):
        """解析里程碑数据"""
        if 'milestones' not in self.data:
            return
            
        for ms_data in self.data['milestones']:
            milestone = Milestone(
                id=ms_data['id'],
                name=ms_data['name'],
                description=ms_data.get('description', ''),
                date=ms_data.get('date', ''),
                tasks=ms_data.get('tasks', []),
                status=ms_data.get('status', 'pending'),
                progress=ms_data.get('progress', {})
            )
            self.milestones[milestone.id] = milestone
    
    def calculate_milestone_progress(self, milestone_id: str) -> Dict:
        """计算里程碑进度"""
        if milestone_id not in self.milestones:
            return {}
        
        milestone = self.milestones[milestone_id]
        total = len(milestone.tasks)
        
        if total == 0:
            return {
                'total': 0,
                'completed': 0,
                'active': 0,
                'pending': 0,
                'percentage': 0
            }
        
        completed = sum(1 for t in milestone.tasks 
                       if t in self.tasks and self.tasks[t].status == TaskStatus.COMPLETED)
        active = sum(1 for t in milestone.tasks 
                    if t in self.tasks and self.tasks[t].status == TaskStatus.ACTIVE)
        pending = total - completed - active
        
        return {
            'total': total,
            'completed': completed,
            'active': active,
            'pending': pending,
            'percentage': round((completed / total) * 100, 1)
        }
    
    def check_risks(self) -> List[Dict]:
        """检查延迟风险"""
        risks = []
        today = datetime.now()
        
        for ms_id, milestone in self.milestones.items():
            if milestone.status == 'completed':
                continue
            
            # 解析目标日期
            try:
                target_date = datetime.strptime(milestone.date, '%Y-%m-%d')
            except:
                continue
            
            # 计算剩余天数
            days_remaining = (target_date - today).days
            
            # 计算进度
            progress = self.calculate_milestone_progress(ms_id)
            percentage = progress.get('percentage', 0)
            
            # 计算时间进度
            if 'phase_start_date' in self.data.get('meta', {}):
                try:
                    start_date = datetime.strptime(
                        self.data['meta']['phase_start_date'], '%Y-%m-%d'
                    )
                    total_days = (target_date - start_date).days
                    elapsed_days = (today - start_date).days
                    time_percentage = (elapsed_days / total_days) * 100 if total_days > 0 else 0
                except:
                    time_percentage = 0
            else:
                time_percentage = 0
            
            # 判断风险等级
            risk_level = RiskLevel.LOW
            if percentage < time_percentage - 20:
                risk_level = RiskLevel.CRITICAL
            elif percentage < time_percentage - 10:
                risk_level = RiskLevel.HIGH
            elif percentage < time_percentage:
                risk_level = RiskLevel.MEDIUM
            elif days_remaining < 30 and percentage < 80:
                risk_level = RiskLevel.HIGH
            elif days_remaining < 60 and percentage < 50:
                risk_level = RiskLevel.MEDIUM
            
            if risk_level != RiskLevel.LOW:
                risks.append({
                    'milestone_id': ms_id,
                    'milestone_name': milestone.name,
                    'target_date': milestone.date,
                    'days_remaining': days_remaining,
                    'progress_percentage': percentage,
                    'time_percentage': round(time_percentage, 1),
                    'risk_level': risk_level.value,
                    'message': self._generate_risk_message(
                        milestone.name, percentage, time_percentage, days_remaining
                    )
                })
        
        return risks
    
    def _generate_risk_message(self, name: str, progress: float, 
                               time_progress: float, days: int) -> str:
        """生成风险警告消息"""
        if progress < time_progress - 20:
            return f"严重延迟: {name} 进度落后时间线 {time_progress - progress:.1f}%"
        elif progress < time_progress - 10:
            return f"显著延迟: {name} 进度落后时间线 {time_progress - progress:.1f}%"
        elif progress < time_progress:
            return f"轻微延迟: {name} 进度略落后于时间线"
        elif days < 30 and progress < 80:
            return f"时间紧迫: {name} 仅剩{days}天，完成度{progress:.1f}%"
        elif days < 60 and progress < 50:
            return f"进度警告: {name} 完成度过低，可能无法按时完成"
        return ""
    
    def generate_report(self) -> str:
        """生成进度报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("Phase 3 里程碑进度报告")
        lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 70)
        lines.append("")
        
        # 总体统计
        lines.append("【总体统计】")
        total_tasks = len(self.tasks)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        active = sum(1 for t in self.tasks.values() if t.status == TaskStatus.ACTIVE)
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        
        lines.append(f"  总任务数: {total_tasks}")
        lines.append(f"  已完成: {completed} ({completed/total_tasks*100:.1f}%)")
        lines.append(f"  进行中: {active}")
        lines.append(f"  待开始: {pending}")
        lines.append("")
        
        # 里程碑详细进度
        lines.append("【里程碑进度】")
        for ms_id, milestone in self.milestones.items():
            progress = self.calculate_milestone_progress(ms_id)
            status_icon = "✅" if milestone.status == "completed" else "🟡" if milestone.status == "active" else "⏳"
            lines.append(f"\n{status_icon} {milestone.name} ({ms_id})")
            lines.append(f"   目标日期: {milestone.date}")
            lines.append(f"   进度: {progress.get('completed', 0)}/{progress.get('total', 0)} 任务完成 ({progress.get('percentage', 0):.1f}%)")
            if progress.get('active', 0) > 0:
                lines.append(f"   进行中任务: {progress['active']} 个")
        
        lines.append("")
        
        # 活跃任务
        lines.append("【活跃任务】")
        active_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.ACTIVE]
        if active_tasks:
            for task in sorted(active_tasks, key=lambda x: x.id):
                progress_str = f" ({task.progress_percentage}%)" if task.progress_percentage else ""
                conj_str = f"[C{task.conjecture}] " if task.conjecture else ""
                lines.append(f"  • {task.id}: {conj_str}{task.title}{progress_str}")
        else:
            lines.append("  无活跃任务")
        
        lines.append("")
        
        # 风险警告
        risks = self.check_risks()
        lines.append("【风险警告】")
        if risks:
            for risk in sorted(risks, key=lambda x: x['risk_level'], reverse=True):
                risk_icon = "🔴" if risk['risk_level'] == 'critical' else "🟠" if risk['risk_level'] == 'high' else "🟡"
                lines.append(f"\n{risk_icon} {risk['milestone_name']}")
                lines.append(f"   风险等级: {risk['risk_level'].upper()}")
                lines.append(f"   目标日期: {risk['target_date']} (剩余 {risk['days_remaining']} 天)")
                lines.append(f"   进度: {risk['progress_percentage']:.1f}% (时间线: {risk['time_percentage']:.1f}%)")
                lines.append(f"   警告: {risk['message']}")
        else:
            lines.append("  ✅ 当前无重大风险")
        
        lines.append("")
        lines.append("=" * 70)
        lines.append("报告结束")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def update_milestone_status(self):
        """更新里程碑状态"""
        updated = []
        
        for ms_id, milestone in self.milestones.items():
            old_status = milestone.status
            progress = self.calculate_milestone_progress(ms_id)
            
            # 自动状态判断
            if progress.get('percentage', 0) >= 100:
                new_status = 'completed'
            elif progress.get('active', 0) > 0 or progress.get('percentage', 0) > 0:
                new_status = 'active'
            else:
                new_status = 'pending'
            
            if new_status != old_status:
                updated.append({
                    'milestone': ms_id,
                    'name': milestone.name,
                    'old_status': old_status,
                    'new_status': new_status
                })
                
                # 更新内存中的状态
                milestone.status = new_status
        
        return updated
    
    def save_updates(self):
        """保存更新到文件"""
        try:
            # 更新原始数据
            if 'milestones' in self.data:
                for i, ms_data in enumerate(self.data['milestones']):
                    ms_id = ms_data['id']
                    if ms_id in self.milestones:
                        ms_data['status'] = self.milestones[ms_id].status
                        # 更新进度信息
                        progress = self.calculate_milestone_progress(ms_id)
                        ms_data['progress'] = progress
            
            # 更新时间戳
            if 'meta' in self.data:
                self.data['meta']['last_updated'] = datetime.now().isoformat()
            
            # 写回文件
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                yaml.dump(self.data, f, allow_unicode=True, sort_keys=False)
            
            return True
        except Exception as e:
            print(f"错误: 保存更新失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='里程碑检查脚本',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python milestone_checker.py --report           # 仅生成报告
    python milestone_checker.py --all              # 执行所有操作
    python milestone_checker.py --report --alert   # 生成报告并检查风险
        """
    )
    parser.add_argument('--report', action='store_true', help='生成进度报告')
    parser.add_argument('--update', action='store_true', help='更新里程碑状态')
    parser.add_argument('--alert', action='store_true', help='检查延迟风险')
    parser.add_argument('--all', action='store_true', help='执行所有操作')
    parser.add_argument('--file', type=str, 
                       default='../../tasks/phase3_tasks.yaml',
                       help='任务文件路径')
    
    args = parser.parse_args()
    
    # 确定要执行的操作
    do_report = args.all or args.report or not (args.update or args.alert)
    do_update = args.all or args.update
    do_alert = args.all or args.alert
    
    # 查找任务文件
    script_dir = Path(__file__).parent
    tasks_file = script_dir / args.file
    
    if not tasks_file.exists():
        # 尝试其他路径
        alt_paths = [
            script_dir / '../../tasks/phase3_tasks.yaml',
            script_dir / '../../../tasks/phase3_tasks.yaml',
            Path('/mnt/e/FiberGravity-DynamicCoupling/GitHub_Repositories/Fixed-4D-Topology/docs/research/tasks/phase3_tasks.yaml')
        ]
        for path in alt_paths:
            if path.exists():
                tasks_file = path
                break
    
    if not tasks_file.exists():
        print(f"错误: 找不到任务文件: {tasks_file}")
        sys.exit(1)
    
    # 创建检查器
    checker = MilestoneChecker(str(tasks_file))
    
    # 生成报告
    if do_report:
        report = checker.generate_report()
        print(report)
        print()
    
    # 检查风险
    if do_alert:
        risks = checker.check_risks()
        if risks:
            print("⚠️  发现风险警告:")
            for risk in risks:
                print(f"  - {risk['milestone_name']}: {risk['message']}")
        else:
            print("✅ 未发现重大风险")
        print()
    
    # 更新状态
    if do_update:
        updates = checker.update_milestone_status()
        if updates:
            print("📝 里程碑状态更新:")
            for update in updates:
                print(f"  - {update['name']}: {update['old_status']} → {update['new_status']}")
            
            # 保存到文件
            if checker.save_updates():
                print("\n✅ 更新已保存到文件")
            else:
                print("\n❌ 保存更新失败")
        else:
            print("ℹ️  无状态变更")


if __name__ == '__main__':
    main()

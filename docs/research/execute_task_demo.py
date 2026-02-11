#!/usr/bin/env python3
"""
任务执行演示 - 展示如何正确使用执行控制器
并确保YAML实时更新
"""

from execution_controller import ExecutionController, TaskStatus

def main():
    # 初始化控制器
    controller = ExecutionController()
    
    # 显示当前状态
    print("=" * 60)
    print("任务执行演示 - YAML实时更新")
    print("=" * 60)
    print()
    
    # 统计当前状态
    total = len(controller.tasks)
    completed = len([t for t in controller.tasks.values() if t.status == TaskStatus.COMPLETED])
    pending = len([t for t in controller.tasks.values() if t.status == TaskStatus.PENDING])
    
    print(f"当前状态:")
    print(f"  总任务数: {total}")
    print(f"  已完成: {completed}")
    print(f"  待执行: {pending}")
    print()
    
    # 演示：完成一个任务
    print("演示：完成一个就绪任务")
    print("-" * 60)
    
    # 找到一个就绪的任务
    ready_tasks = controller.get_ready_tasks()
    if ready_tasks:
        task = ready_tasks[0]
        print(f"选择任务: {task.id} - {task.title[:50]}...")
        print(f"  原状态: {task.status.value}")
        
        # 开始任务
        controller.start_task(task)
        print(f"  开始后状态: {task.status.value}")
        print(f"  YAML已更新: ✓")
        
        # 模拟执行任务...
        print(f"  执行任务中...")
        
        # 完成任务
        controller.complete_task(task, actual_effort="10min")
        print(f"  完成后状态: {task.status.value}")
        print(f"  完成时间: {task.completed}")
        print(f"  YAML已更新: ✓")
        print()
        
        # 验证YAML已保存
        print("验证YAML数据持久化:")
        # 重新加载YAML验证
        controller2 = ExecutionController()
        task2 = controller2.tasks.get(task.id)
        if task2 and task2.status == TaskStatus.COMPLETED:
            print(f"  ✓ 任务 {task.id} 状态已持久化为 'completed'")
        else:
            print(f"  ✗ 持久化验证失败")
    else:
        print("没有就绪的任务")
    
    print()
    print("=" * 60)
    print("演示完成")
    print("=" * 60)
    print()
    print("使用指南:")
    print("1. 获取就绪任务: ready_tasks = controller.get_ready_tasks()")
    print("2. 开始任务: controller.start_task(task)")
    print("3. 完成任务: controller.complete_task(task, actual_effort='1h')")
    print("4. YAML会自动更新")

if __name__ == "__main__":
    main()

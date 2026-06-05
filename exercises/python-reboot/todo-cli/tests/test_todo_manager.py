from todo_manager import TodoManager
import pytest


def test_add_task_with_priority(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study", priority="high")

    tasks = manager.get_tasks()

    assert tasks[0].priority == "high"
    assert len(tasks) == 1
    assert tasks[0].title == "study"
    assert tasks[0].done is False


def test_mark_done(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")

    manager.mark_done(0)

    tasks = manager.get_tasks()

    assert tasks[0].done is True


def test_remove_task_by_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")
    manager.add_task("sleep")

    manager.remove_task_by_index(0)

    tasks = manager.get_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "sleep"
    assert tasks[0].index == 0


def test_get_tasks_undone(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")
    manager.add_task("sleep")

    manager.mark_done(0)

    tasks = manager.get_tasks(undone=True)

    assert len(tasks) == 1
    assert tasks[0].title == "sleep"
    assert tasks[0].done is False


def test_get_tasks_priority(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study", priority="low")
    manager.add_task("sleep")

    tasks = manager.get_tasks(priority="low")

    assert len(tasks) == 1
    assert tasks[0].priority == "low"


def test_get_tasks_sort_desc(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")
    manager.add_task("sleep")
    manager.add_task("dinner")

    tasks = manager.get_tasks(sort="desc")

    assert len(tasks) == 3
    assert tasks[0].title == "dinner"
    assert tasks[1].title == "sleep"
    assert tasks[2].title == "study"


def test_get_tasks_keyword(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")
    manager.add_task("sleep")
    manager.add_task("dinner Sleep")

    tasks = manager.get_tasks(keyword="sleep")

    titles = [t.title for t in tasks]
    assert len(tasks) == 2
    assert "sleep" in titles
    assert "dinner Sleep" in titles


def test_mark_done_invalid_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")

    with pytest.raises(ValueError):
        manager.mark_done(999)


def test_remove_invalid_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")

    with pytest.raises(ValueError):
        manager.remove_task_by_index(999)


def test_keyword_empty(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("study")

    tasks = manager.get_tasks(keyword="")

    assert len(tasks) == 1


def test_get_tasks_sort_by_priority(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "todo.json"))

    manager.add_task("task1", priority="low")
    manager.add_task("task2", priority="medium")
    manager.add_task("task3", priority="high")

    tasks = manager.get_tasks(sort="priority")

    assert tasks[0].priority == "high"
    assert tasks[1].priority == "medium"
    assert tasks[2].priority == "low"


def test_get_tasks_sort_by_priority_then_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("task1", priority="high")
    manager.add_task("task2", priority="low")
    manager.add_task("task3", priority="high")

    tasks = manager.get_tasks(sort="priority")

    titles = [t.title for t in tasks]

    assert titles == ["task1", "task3", "task2"]


def test_get_tasks_sort_by_status_priority_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path / "test.json"))

    manager.add_task("task1", priority="low")  # undone, low, index 0
    manager.add_task("task2", priority="high")  # undone, high, index 1
    manager.add_task("task3", priority="high")  # done, high, index 2
    manager.add_task("task4", priority="medium")  # undone, medium, index 3

    manager.mark_done(2)

    tasks = manager.get_tasks(sort="smart")

    titles = [task.title for task in tasks]

    assert titles == ["task2", "task4", "task1", "task3"]

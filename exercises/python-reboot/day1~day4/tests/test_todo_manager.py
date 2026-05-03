from todo_manager import TodoManager

def test_add_task(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))
    
    manager.add_task("study")
    
    tasks = manager.get_tasks()
    
    assert len(tasks) == 1
    assert tasks[0].title == "study"
    assert tasks[0].done is False
    
def test_mark_done(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json")) 
    
    manager.add_task("study")
    
    manager.mark_done(0)
    
    tasks = manager.get_tasks()
    
    assert tasks[0].done is True
    
def test_remove_task_by_index(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))
    
    manager.add_task("study")
    manager.add_task("sleep")
    
    manager.remove_task_by_index(0)
    
    tasks = manager.get_tasks()
    
    assert len(tasks) == 1
    assert tasks[0].title == "sleep"
    assert tasks[0].index == 0
    
def test_get_tasks_undone(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))
    
    manager.add_task("study")
    manager.add_task("sleep")
    
    manager.mark_done(0)
    
    tasks = manager.get_tasks(undone=True)
    
    assert len(tasks) == 1
    assert tasks[0].title == "sleep"
    assert tasks[0].done is False
    
def test_get_tasks_sort_desc(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))
    
    manager.add_task("study")
    manager.add_task("sleep")
    manager.add_task("dinner")
    
    tasks = manager.get_tasks(sort="desc")
    
    assert len(tasks) == 3
    assert tasks[0].title == "dinner"
    assert tasks[1].title == "sleep"
    assert tasks[2].title == "study"
    
def test_get_tasks_keyword(tmp_path):
    manager = TodoManager(file_path=str(tmp_path/"test.json"))
    
    manager.add_task("study")
    manager.add_task("sleep")
    manager.add_task("dinner Sleep")
    
    tasks = manager.get_tasks(keyword="sleep")
    
    titles = [t.title for t in tasks]
    assert len(tasks) == 2
    assert "sleep" in titles
    assert "dinner Sleep" in titles
    
    
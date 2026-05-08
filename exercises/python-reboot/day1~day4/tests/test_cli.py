import sys
from todo import main
import pytest
    
def test_cli_list_empty(tmp_path, capsys):
    file_path = tmp_path/"todo.json"
    
    sys.argv = ["todo.py", "--file", str(file_path),"list"]
    
    main()
    
    captured = capsys.readouterr()
    
    assert "タスクはありません" in captured.out
    
def test_cli_add_and_list(tmp_path, capsys):
    file_path = tmp_path/"todo.json"
    
    #add
    sys.argv = ["todo.py", "--file", str(file_path), "add", "study"]
    main()
    
    #list
    sys.argv = ["todo.py", "--file", str(file_path),"list"]
    main()
    
    captured = capsys.readouterr()
    
    assert "study" in captured.out
    
def test_cli_invalid_priority(tmp_path):
    file_path = tmp_path/ "todo.json"
    
    sys.argv = ["todo.py", "--file", str(file_path), "add", "study", "--priority", "xxx"]
    
    with pytest.raises(SystemExit):
        main()
        
def test_cli_add_with_priority_and_list(tmp_path, capsys):
    file_path = tmp_path/"todo.json"
    sys.argv = ["todo.py","--file",str(file_path),"add", "study", "--priority","high"]
    main()
    
    sys.argv = ["todo.py", "--file",str(file_path), "list"]
    main()
    
    captured = capsys.readouterr()
    
    assert "study" in captured.out
    assert "(high)" in captured.out
    
def test_cli_sort_by_priority(tmp_path, capsys):
    file_path = tmp_path/ "todo.json"
    
    sys.argv = ["todo.py", "--file", str(file_path), "add", "task1", "--priority", "low"]
    main()
    
    sys.argv = ["todo.py", "--file", str(file_path), "add", "task2", "--priority", "high"]
    main()
    
    sys.argv = ["todo.py", "--file", str(file_path), "list", "--sort", "priority"]
    main()
    
    captured = capsys.readouterr()
    
    task_lines = [line for line in captured.out.splitlines() if "[ ]" in line]
    assert "task2" in task_lines[0]
        
def test_cli_list_grouped(tmp_path, capsys):
    file_path = tmp_path/"todo.json"
    
    sys.argv = ["todo.py", "--file", str(file_path), "add","task1"]
    main()
    
    sys.argv = ["todo.py", "--file", str(file_path), "add", "task2"]
    main()
    
    sys.argv = ["todo.py", "--file", str(file_path), "done", "2"]
    main()
    
    sys.argv = ["todo.py", "--file", str(file_path), "list"]
    main()
    
    captured = capsys.readouterr()
    
    assert "[未完了]" in captured.out
    assert "[完了]" in captured.out
    
    
    
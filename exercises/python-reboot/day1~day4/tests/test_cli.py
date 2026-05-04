import sys
from todo import main
    
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
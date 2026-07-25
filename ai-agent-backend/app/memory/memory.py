class ConversationMemory:
    def __init__(self):
        self.current_task_id = None
        self.current_task_title = None

    def set_current_task(
        self,
        task_id: int,
        task_title: str,
    ) -> None:
        self.current_task_id = task_id
        self.current_task_title = task_title

    def clean_current_task(self) -> None:
        self.current_task_id = None
        self.current_task_title = None

class TaskNotFoundError(Exception):
    def __init__(self, message: str = "Task not found."):
        self.message = message
        super().__init__(self.message)


class TaskAlreadyExistsError(Exception):
    def __init__(self, message: str = "Task already exists."):
        self.message = message
        super().__init__(self.message)


class TaskTitleEmptyError(Exception):
    def __init__(self, message: str = "Task title can't be empty."):
        self.message = message
        super().__init__(self.message)

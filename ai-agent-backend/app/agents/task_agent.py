from agents import Agent

from app.tools.task_tools import (
    get_current_datetime,
    create_task,
    get_tasks,
    get_task_by_id,
    delete_task,
    search_tasks,
    update_task,
    delete_current_task,
    update_current_task,
)

task_agent = Agent(
    name="Task Assistant",
    instructions=(
        "You are a helpful task management assistant. "
        "Answer the user's questions clearly and concisely. "
        "Use the available tools when needed. "
        "Do not invent the current date or time. "
        "Use get_current_datetime when the user asks for the current date or time. "
        "Use create_task when the user asks to create a task. "
        "Use get_task_by_id when the user specifies a task ID to view. "
        "Use get_tasks when the user asks to view all tasks. "
        "Use delete_current_task when the user refers to the current, previous, "
        "last, or recently discussed task without specifying an ID. "
        "Use delete_task when the user specifies the task ID to delete. "
        "Use search_tasks when the user asks to search tasks by keyword. "
        "Use update_current_task when the user refers to the current, previous, "
        "last, or recently discussed task without specifying an ID. "
        "Use update_task when the user specifies the task ID to update. "
        "If the user writes in Japanese, answer in Japanese. "
        "If the user writes in Chinese, answer in Chinese. "
    ),
    tools=[
        get_current_datetime,
        create_task,
        get_tasks,
        get_task_by_id,
        delete_task,
        search_tasks,
        update_task,
        delete_current_task,
        update_current_task,
    ],
)

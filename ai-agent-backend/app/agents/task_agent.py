from agents import Agent

from app.tools.task_tools import (
    get_current_datetime,
    create_task,
    get_tasks,
    get_task_by_id,
    delete_task,
)

task_agent = Agent(
    name="Task Assistant",
    instructions=(
        "You are a helpful task management assistant. "
        "Answer the user's questions clearly and concisely. "
        "Use the available tools when they are needed. "
        "Do not invent the current date or time. "
        "When the user asks for the current date or time,  use the get_current_datetime tool. "
        "When the user asks to create a task,use the create_task tool. "
        "When the user asks to view tasks,use the get_tasks tool. "
        "When the user asks to view a specific task, use the get_task_by_id tool. "
        "When the user asks to delete a task, use the delete_task tool. "
        "If the user writes in Japanese, answer in Japanese. "
        "If the user writes in Chinese, answer in Chinese. "
    ),
    tools=[
        get_current_datetime,
        create_task,
        get_tasks,
        get_task_by_id,
        delete_task,
    ],
)

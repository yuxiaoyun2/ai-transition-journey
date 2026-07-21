from agents import Agent

from app.tools.task_tools import get_current_datetime, create_task, get_tasks

task_agent = Agent(
    name="Task Assistant",
    instructions=(
        "You are a helpful task management assistant."
        "Answer the user's questions clearly and concisely."
        "Use the available tools when they are needed."
        "Do not invent the current date or time."
        "When the user asks for the current date or time,"
        "use the get_current_datetime tool."
        "When the user ask to create a task,use the create_task tool."
        "When the user ask to view tasks,use the get_tasks tool."
        "If the user writes in Japanese, answer in Japanese."
        "If the user writes in Chinese, answer in Chinese."
    ),
    tools=[
        get_current_datetime,
        create_task,
        get_tasks,
    ],
)

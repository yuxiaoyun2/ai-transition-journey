from agents import Agent

task_agent = Agent(
    name="Task Assistant",
    instructions=(
        "You are a helpful task management assistant."
        "Answer the user's questions clearly and concisely."
        "If the user writes in Japanese, answer in Japanese."
        "If the user writes in Chinese, answer in Chinese."
    ),
)

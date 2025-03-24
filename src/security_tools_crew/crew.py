from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from security_tools_crew.tools.get_info import ScanNetworkTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SecurityToolsCrew():
    """Security Tools Crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # Define templates for system, user (prompt), and assistant (response) messages
    system_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>{{ .System }}<|eot_id|>"""
    prompt_template = """<|start_header_id|>user<|end_header_id|>{{ .Prompt }}<|eot_id|>"""
    response_template = """<|start_header_id|>assistant<|end_header_id|>{{ .Response }}<|eot_id|>"""


    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def cybersecurity_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['cybersecurity_analyst'],
            verbose=True,
            system_template=self.system_template,
            prompt_template=self.prompt_template,
            response_template=self.response_template,
            tools=[ScanNetworkTool(result_as_answer=True)] # Example of adding a tool to the agent
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def info_task(self) -> Task:
        return Task(
            config=self.tasks_config['info_task'],
            output_file='output/nmap_scan.json', # Optional: specify an output file for the task results
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SecurityToolsCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            chat_llm="ollama/llama3.2"
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

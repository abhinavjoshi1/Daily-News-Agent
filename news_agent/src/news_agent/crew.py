from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
import os
from datetime import date, timedelta

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


search_tool = SerperDevTool(
    tbs="qdr:d",      # Results from past 24 hours only
    # tbs="qdr:h6"   # Or past 6 hours for ultra-fresh news
)

@CrewBase
class NewsAgent():
    """NewsAgent crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def news_fetcher(self) -> Agent:
        return Agent(
            config=self.agents_config['news_fetcher'],
            verbose=True,
            tools=[search_tool]
        )

    @agent
    def news_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['news_analyst'],
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def fetch_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_news_task'],
        )

    @task
    def write_digest_task(self) -> Task:
        from datetime import datetime
        import pytz
        ist = pytz.timezone('Asia/Kolkata')
        today = datetime.now(ist).date()
        filename = f"digests/Digest_{today.strftime('%d_%m_%y')}.md"
        return Task(
            config=self.tasks_config['write_digest_task'],
            output_file=filename
        )
    # @task
    # def reporting_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['reporting_task'], # type: ignore[index]
    #         output_file='report.md'
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the NewsAgent crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

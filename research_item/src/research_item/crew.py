from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

from tools.reddit_tavily_search import RedditTavilySearchTool
from tools.tavily_search_tool import TavilySearchTool

from dotenv import load_dotenv

load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ResearchItem():
	"""ResearchItem crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	@agent
	def serper_comparison(self) -> Agent:
		return Agent(
			config=self.agents_config["researcher"],
			tools=[SerperDevTool()]
		)
	
	@agent
	def website_scrape(self) -> Agent:
		return Agent(
			config=self.agents_config['researcher'],
			tools = [ScrapeWebsiteTool()]
		)
	
	@agent
	def tavily_comparison(self) -> Agent:
		return Agent(
			config=self.agents_config["researcher"],
			tools=[TavilySearchTool()]
		)
	
	@agent
	def reddit_search_comparison(self) -> Agent:
		return Agent(
			config=self.agents_config["researcher"],
			tools=[RedditTavilySearchTool()]
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task

	@task
	def serper_comparison_task(self) -> Task:
		return Task(
			config=self.tasks_config["serper_comparison_task"],
			output_file="steps/serper_comparison_task.md"
		)
	
	@task
	def website_scrape_task(self) -> Task:
		return Task(
			config=self.tasks_config['website_scrape_task'],
			output_file="steps/website_scrape_task.md"
		)
	
	@task
	def tavily_comparison_task(self) -> Task:
		return Task(
			config=self.tasks_config["tavily_comparison_task"],
			output_file="steps/tavily_comparison_task.md"
		)

	@task
	def reddit_search_comparison_task(self) -> Task:
		return Task(
			config=self.tasks_config["reddit_search_comparison_task"],
			output_file="steps/reddit_search_comparison_task.md"
		)

	@task
	def final_comparison_report_task(self) -> Task:
		return Task(
			config=self.tasks_config["final_comparison_report_task"],
			output_file="report.md"
        )

	@crew
	def crew(self) -> Crew:
		"""Creates the ResearchItem crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

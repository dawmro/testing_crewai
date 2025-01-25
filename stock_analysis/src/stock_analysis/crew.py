from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from tools.calculator_tool import CalculatorTool
from tools.sec_tools import SEC10KTool, SEC10QTool

from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool, TXTSearchTool

from dotenv import load_dotenv
load_dotenv()

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class StockAnalysis():
	"""StockAnalysis crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def financial_agent(self) -> Agent:
		return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool("AMZN"),
                SEC10KTool("AMZN"),
            ]
        )

	@agent
	def research_analyst_agent(self) -> Agent:
		return Agent(
            config=self.agents_config['research_analyst'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                SEC10QTool("AMZN"),
                SEC10KTool("AMZN"),
            ]
        )
	
	@agent
	def financial_analyst_agent(self) -> Agent:
		return Agent(
            config=self.agents_config['financial_analyst'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
                SEC10QTool(),
                SEC10KTool(),
            ]
        )
	
	@agent
	def investment_advisor_agent(self) -> Agent:
		return Agent(
            config=self.agents_config['investment_advisor'],
            verbose=True,
            tools=[
                ScrapeWebsiteTool(),
                WebsiteSearchTool(),
                CalculatorTool(),
            ]
        )

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def financial_analysis(self) -> Task: 
		return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_agent(),
        )

	@task
	def research(self) -> Task:
		return Task(
            config=self.tasks_config['research'],
            agent=self.research_analyst_agent(),
        )
	
	@task
	def financial_analysis(self) -> Task: 
		return Task(
            config=self.tasks_config['financial_analysis'],
            agent=self.financial_analyst_agent(),
        )
	
	@task
	def filings_analysis(self) -> Task:
		return Task(
            config=self.tasks_config['filings_analysis'],
            agent=self.financial_analyst_agent(),
        )
	
	@task
	def recommend(self) -> Task:
		return Task(
            config=self.tasks_config['recommend'],
            agent=self.investment_advisor_agent(),
        )

	@crew
	def crew(self) -> Crew:
		"""Creates the StockAnalysis crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)

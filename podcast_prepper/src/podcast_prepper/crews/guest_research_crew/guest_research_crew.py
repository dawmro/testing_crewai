from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.exa_tool import ExaGuestResearchTool



@CrewBase
class GuestResearchCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def senior_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_researcher"],
            respect_context_window=True,
            max_iter=2,
            verbose=True,
            tools=[ExaGuestResearchTool()],
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            human_input=True,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            output_log_file="log_guest_research_crew.txt",
            verbose=True,
        )
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task



@CrewBase
class QuestionsResearchCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def senior_journalist(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_journalist"],
            respect_context_window=True,
            max_iter=2,
            verbose=True,
        )

    @task
    def journalism_task(self) -> Task:
        return Task(
            config=self.tasks_config["journalism_task"],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            output_log_file="log_questions_research_crew.txt",
            verbose=True,
        )
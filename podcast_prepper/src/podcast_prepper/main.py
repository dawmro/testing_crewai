#!/usr/bin/env python
import agentops
import asyncio
import os
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from crews.guest_research_crew.guest_research_crew import GuestResearchCrew
from crews.questions_research_crew.questions_research_crew import QuestionsResearchCrew
from rich.console import Console
from rich.prompt import Prompt

from dotenv import load_dotenv

load_dotenv()

output_formatter = Console()


class PodcastPrepperState(BaseModel):
    user_input: str = ""
    crewai_output: str = ""
    token_usage: str = ""


class PodcastPrepperFlow(Flow[PodcastPrepperState]):
    @start()
    def say_hello(self):
        output_formatter.print(
            "[#66FF66]\n🤖 CrewAI: Hi! Who is your next guest? Give me his or her name and surname, and I'll do the rest.[/#66FF66]"
        )

    @listen(say_hello)
    def get_guest_name(self):
        user_input = Prompt.ask("\n🧑 You")

        self.state.user_input = user_input

        if user_input.lower() in ["quit", "exit", "q"]:
            output_formatter.print("\n[#66FF66]🤖 CrewAI: Have a nice day![/#66FF66]\n")

            raise SystemExit

    @listen(get_guest_name)
    def get_information_about_guest(self):
        crewai_output = (
            GuestResearchCrew()
            .crew()
            .kickoff(
                inputs={
                    "guest": self.state.user_input,
                }
            )
        )

        self.state.crewai_output = crewai_output.raw
        self.state.token_usage = crewai_output.token_usage

        output_formatter.print(f"[#66FF66]🤖 CrewAI: \n{crewai_output.raw}[/#66FF66]")

    @listen(get_information_about_guest)
    def save_information_about_guest_and_token_usage(self):
        formatted_user_input = self.state.user_input.lower().replace(" ", "_")

        with open(f"{formatted_user_input}_report.md", "w") as file:
            file.write(self.state.crewai_output)

        token_usage_str = str(self.state.token_usage)

        with open("log_token_usage.txt", "w") as file:
            file.write("Guest Research Crew\n\n")
            file.write(token_usage_str)

    @listen(save_information_about_guest_and_token_usage)
    def get_questions_for_guest(self):
        crewai_output = (
            QuestionsResearchCrew()
            .crew()
            .kickoff(
                inputs={
                    "guest_information": self.state.crewai_output,
                }
            )
        )

        self.state.crewai_output = crewai_output.raw
        self.state.token_usage = crewai_output.token_usage

        output_formatter.print(f"[#66FF66]🤖 CrewAI: \n{crewai_output.raw}[/#66FF66]")

    @listen(get_questions_for_guest)
    def save_questions_for_guest_and_token_usage(self):
        formatted_user_input = self.state.user_input.lower().replace(" ", "_")

        with open(f"{formatted_user_input}_report.md", "a") as file:
            file.write("\n\n---\n\n")
            file.write(self.state.crewai_output)

        token_usage_str = str(self.state.token_usage)

        with open("log_token_usage.txt", "a") as file:
            file.write("\n\nQuestions Research Crew\n\n")
            file.write(token_usage_str)

    @listen(save_questions_for_guest_and_token_usage)
    def say_goodbye(self):
        formatted_user_input = self.state.user_input.lower().replace(" ", "_")

        output_formatter.print(
            f"[#66FF66]\n🤖 CrewAI: I've prepared a report about {self.state.user_input}. You can find it in the file [bold cyan]{formatted_user_input}_report.md[/bold cyan]. Have a nice day![/#66FF66]\n"
        )




def kickoff():
    session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))

    podcast_prepper_flow = PodcastPrepperFlow()
    podcast_prepper_flow.plot()
    podcast_prepper_flow.kickoff()

    session.end_session()




if __name__ == "__main__":
    kickoff()
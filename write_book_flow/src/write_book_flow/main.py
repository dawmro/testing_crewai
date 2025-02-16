#!/usr/bin/env python
import asyncio
import agentops
import os
from typing import List
from datetime import datetime

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from crews.write_book_chapter_crew.write_book_chapter_crew import (
    WriteBookChapterCrew,
)
from src.write_book_flow.models.types import Chapter, ChapterOutline

from crews.outline_book_crew.outline_crew import OutlineCrew

from dotenv import load_dotenv

load_dotenv()

date = datetime.now().strftime('%Y-%m-%d')

class BookState(BaseModel):
    title: str = f"The Current State of Growing Algae for Fuel in {date}"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = (
        f"Exploring the latest trends in Growing Algae for Fuel in different industries as of {date}"
    )
    goal: str = f"""
        The goal of this book is to provide a comprehensive overview of the current state of Growing Algae for Fuel in {date}.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge Growing Algae for Fuel technologies
        and prepare them for upcoming innovations in the field.
    """


class BookFlow(Flow[BookState]):
    initial_state = BookState

    @start()
    def generate_book_outline(self):
        print("Kickoff the Book Outline Crew")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "goal": self.state.goal})
        )

        chapters = output["chapters"]
        print("Chapters:", chapters)

        self.state.book_outline = chapters
        return chapters

    @listen(generate_book_outline)
    async def write_chapters(self):
        print("Writing Book Chapters")
        tasks = []

        async def write_single_chapter(chapter_outline):
            output = (
                WriteBookChapterCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": chapter_outline.title,
                        "chapter_description": chapter_outline.description,
                        "book_outline": [
                            chapter_outline.model_dump_json()
                            for chapter_outline in self.state.book_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter

        for chapter_outline in self.state.book_outline:
            print(f"Writing Chapter: {chapter_outline.title}")
            print(f"Description: {chapter_outline.description}")
            # Schedule each chapter writing task
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        # Await all chapter writing tasks concurrently
        chapters = await asyncio.gather(*tasks)
        print("Newly generated chapters:", chapters)
        self.state.book.extend(chapters)

        print("Book Chapters", self.state.book)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        print("Joining and Saving Book Chapters")
        # Combine all chapters into a single markdown string
        book_content = ""

        for chapter in self.state.book:
            # Add the chapter title as an H1 heading
            book_content += f"# {chapter.title}\n\n"
            # Add the chapter content
            book_content += f"{chapter.content}\n\n"

        # The title of the book from self.state.title
        book_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        filename = f"./{book_title.replace(' ', '_')}.md"

        # Save the combined content into the file
        with open(filename, "w", encoding="utf-8") as file:
            file.write(book_content)

        print(f"Book saved as {filename}")
        return book_content


def kickoff():
    session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"), skip_auto_end_session=True)
    book_flow = BookFlow()
    book_flow.kickoff()

def plot():
    book_flow = BookFlow()
    book_flow.plot()


if __name__ == "__main__":
    kickoff()
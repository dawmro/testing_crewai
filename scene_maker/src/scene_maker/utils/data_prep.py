import os 
import re
from .file_utils import read_file, write_file, read_json_file
from .logging_utils import showTime



def get_projects(PROJECTS_DIR, RESULTS_DIR):    
    print(f"{showTime()}")
    # Get current working directory
    CWD = os.getcwd()
    # list each project in PROJECTS_DIR
    project_names_mixed = [ f.name for f in os.scandir(PROJECTS_DIR) if f.is_dir() ]
    
    # sort project directiories by name
    project_names = []
    try:
        project_names_mixed.sort(key=lambda f: int(re.sub(r'\D', '', f)))
    except:
        pass
    for project_name_mixed in project_names_mixed:
        existing_result_path = os.path.join(RESULTS_DIR, project_name_mixed, "script.md")
        if not os.path.exists(existing_result_path):
            project_names.append(project_name_mixed)

    print(project_names)
    return project_names


def create_inputs_array(projects_list, PROJECTS_DIR, SYNOPIS_PATH):
    inputs_array = []
    for project_name in projects_list:
        project_path = os.path.join(PROJECTS_DIR, project_name)
        story_path = os.path.join(project_path, "story.txt")
        if os.path.exists(story_path):
            inputs_array.append({
                'synopis': read_file(SYNOPIS_PATH),
                'story_text': read_file(story_path),
                'project_name': project_name
            })
            print(f"OK: No story.txt file added for: {project_name}")
        else:
            print(f"Warning: No story.txt file found in project: {project_name}")

    return inputs_array


def extract_summary_and_narrations(data):
    summary = data['summary']
    narrations = [scene['narration'] for scene in data['scenes']]
    return summary, narrations


def extract_narrations(data):
    narrations = [scene['narration'] for scene in data['scenes']]
    return narrations


def create_recap(results_list, RESULTS_DIR):
    for result_name in results_list:
        result_path = os.path.join(RESULTS_DIR, result_name)
        script_path = os.path.join(result_path, "script.md")
        if os.path.exists(script_path):
            recap_list = []
            data = read_json_file(script_path)
            # summary, narrations = extract_summary_and_narrations(data)
            narrations = extract_narrations(data)
            recap_list.append(result_name + ".")
            # recap_list.append(summary)
            for i, narration in enumerate(narrations, start=1):
                recap_list.append(narration)

            recap_path = os.path.join(result_path, "story.txt")
            recap = '\n\n'.join(recap_list)
            status = write_file(recap, recap_path)
            if status:
                print(f"File {recap_path} written successfully")
            else:
                print(f"Error writing file {recap_path}")
            print(f"OK: Created recap for: {result_name}\n")
        else:
            print(f"Warning: No script.md file found in project: {result_name}\n")

        

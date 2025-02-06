import os 
import re
from .file_utils import read_file
from .logging_utils import showTime



def get_projects(PROJECTS_DIR):    
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
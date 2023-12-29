from pathlib import Path
import json

with open(
    'init_data/data_to_export_all_notes.json', encoding="utf8"
) as initialization_file:
    initialization_data = json.load(initialization_file)

# Reading notes' data from note.xml
notes_data = Path().cwd() / initialization_data["boyeu_notes_folder"] / "data"
with open((notes_data / 'notes.xml'), encoding='UTF-8') as notes_database_file:
    notes_database = notes_database_file.readlines()
all_known_notebook_lines = [
    line for line in notes_database if '&quot;,&quot;noteName&quot;:&quot;' in line
]

note_names_start_position_token = '&quot;,&quot;noteName&quot;:&quot;'
note_names_end_position_token = '&quot;,&quot;notebg&quot;'
all_notes_names_list = [
    line[
        (
            line.find(note_names_start_position_token)
            + len(note_names_start_position_token)
        ) : line.find(note_names_end_position_token)
    ]
    for line in all_known_notebook_lines
]

initialization_data['notes_names'] = all_notes_names_list
with open('init_data/data_for_export.json', encoding="utf8", mode='w') as export_file:
    json.dump(initialization_data, export_file, indent=4, ensure_ascii=False)

print(
    f"All notes' names are written to {Path('init_data/data_for_export.json').resolve()}"
)

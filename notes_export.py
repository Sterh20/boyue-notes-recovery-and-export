from pathlib import Path
import json
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import img2pdf

# CLI arguments parsing
parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--notes_names', default='', help='Names of the notes to export, separated by a comma and space')
cli_arguments = vars(parser.parse_args())

# convert parsed notes' names to general format
notes_names_from_cli = cli_arguments['notes_names'].split(', ')

with open('init_data/data_for_export.json', encoding="utf8") as initialization_file:
    initialization_data = json.load(initialization_file)
# Add to notes from init file notes from CLI
if notes_names_from_cli != parser.get_default('notes_names').split(', '):
    initialization_data['notes_names'] += notes_names_from_cli

# Reading notes' data from note.xml
notes_data = Path().cwd() / initialization_data["boyeu_notes_folder"] / "data"
with open((notes_data / 'notes.xml'), encoding='UTF-8') as notes_database_file:
    notes_database = notes_database_file.readlines()
all_known_notebook_lines = [
    line for line in notes_database if '&quot;,&quot;noteName&quot;:&quot;' in line
]

notes_ids_by_notes_names = {
    line[
        line.find('&quot;,&quot;noteName&quot;:&quot;')
        + len("&quot;,&quot;noteName&quot;:&quot;") : line.find(
            "&quot;,&quot;notebg&quot;"
        )
    ]: line[
        line.find('&quot;noteId&quot;:&quot;noteid-')
        + len('&quot;noteId&quot;:&quot;noteid-') : line.find(
            '&quot;,&quot;noteName&quot;:&quot;'
        )
    ]
    for line in all_known_notebook_lines
}

notes_ids_by_notes_names = {}
notes_pages_id_by_notes_ids = {}
for line in all_known_notebook_lines:
    note_names_start_position_in_the_line = line.find(
        '&quot;,&quot;noteName&quot;:&quot;'
    ) + len('&quot;,&quot;noteName&quot;:&quot;')
    note_names_end_position_in_the_line = line.find('&quot;,&quot;notebg&quot;')
    note_name = line[
        note_names_start_position_in_the_line:note_names_end_position_in_the_line
    ]
    note_id_start_position_in_the_line = line.find(
        '&quot;noteId&quot;:&quot;noteid-'
    ) + len('&quot;noteId&quot;:&quot;noteid-')
    note_id_end_position_in_the_line = line.find('&quot;,&quot;noteName&quot;:&quot;')
    note_id = line[note_id_start_position_in_the_line:note_id_end_position_in_the_line]
    notes_ids_by_notes_names[note_name] = note_id
    page_id_list_start_position_in_the_line = line.find(
        '&quot;pageIds&quot;:[&quot;'
    ) + len('&quot;pageIds&quot;:[&quot;')
    page_id_list_end_position_in_the_line = line.find('&quot;]}</string>')
    page_ids = line[
        page_id_list_start_position_in_the_line:page_id_list_end_position_in_the_line
    ].split('&quot;,&quot;')
    notes_pages_id_by_notes_ids[note_id] = [
        page_id.strip('pageid-') for page_id in page_ids
    ]

# check if their are notes in the input list that are not in the notes.xml
invalid_notes_names = set(initialization_data['notes_names']) - set(
    notes_ids_by_notes_names
)
if invalid_notes_names:
    print("The following input notes' names are not present in notes.xml:")
    print(*invalid_notes_names, sep='\n')
    print("Check for notes' names validity")
    # handle the situation with invalid notes' names
    while True:
        user_input = input('Continue? (y/n)')
        if user_input.lower() == 'y':
            for invalid_key in invalid_notes_names:
                initialization_data['notes_names'].remove(invalid_key)
            break
        elif user_input.lower() == 'n':
            exit()
        else:
            print('You entered: "' + str(user_input) + '"', 'instead of y or n')

# set boyue's page dpi (default is 96 dpi)
dpix = dpiy = 72
layout_fun = img2pdf.get_fixed_dpi_layout_fun((dpix, dpiy))
# Turn off annoying messages about alpha chanel
logger = logging.getLogger('img2pdf')
logger.disabled = True

for note_name in initialization_data['notes_names']:
    path_to_output_file = Path().cwd() / 'export' / f'Note-{note_name}.pdf'
    with open(path_to_output_file, mode='wb') as pdf_file_for_export:
        file_list_to_export = [
            (
                notes_data
                / f'noteid-{notes_ids_by_notes_names[note_name]}-pageid-{page_id}.png'
            )
            for page_id in notes_pages_id_by_notes_ids[
                notes_ids_by_notes_names[note_name]
            ]
        ]
        pdf_file_for_export.write(
            img2pdf.convert(file_list_to_export, layout_fun=layout_fun)
        )
        print(f'Note "{note_name}" is exported to {path_to_output_file}')
logger.disabled = False

from pathlib import Path
import json

with open('init_data/data_for_recovery.json', encoding='utf8') as initialization_file:
    initialization_data = json.load(initialization_file)

notes_data = Path().cwd() / initialization_data['boyeu_notes_folder'] / 'data'

note_pages = {}
for note_id in initialization_data['note_ids']:
    png_files = notes_data.glob(f'noteid-{note_id}*.png')
    note_pages[note_id] = [
        png.name for png in png_files if not png.stem.endswith('note')
    ]

with open((notes_data / 'notes.xml'), encoding='UTF-8') as notes_database_file:
    notes_database = notes_database_file.readlines()

all_known_notebook_lines = [
    line for line in notes_database if '&quot;,&quot;noteName&quot;:&quot;' in line
]

all_known_notebook_names = [
    line[
        line.find('&quot;,&quot;noteName&quot;:&quot;')
        + len('&quot;,&quot;noteName&quot;:&quot;') : line.find(
            '&quot;,&quot;notebg&quot;'
        )
    ]
    for line in all_known_notebook_lines
]

FAKE_EDIT_DATE = 1703486477983

note_pages['1698500249858'][0][note_pages['1698500249858'][0].find('-pageid-') + 1 : -4]

recovered_xml_lines = []
current_edit_data = FAKE_EDIT_DATE
for note_id, notes_pages in note_pages.items():
    current_pages_xml_list = ''
    for note_page_file_name in notes_pages:
        current_pages_xml_list += '&quot;'
        current_page_id = note_page_file_name[
            note_page_file_name.find('-pageid-') + 1 : -4
        ]
        current_pages_xml_list += current_page_id + '&quot;,'
    current_pages_xml_list = current_pages_xml_list[:-1]
    current_edit_data += 1
    recovered_xml_lines += [
        '\t<string name="noteid-'
        + note_id
        + '">{&quot;category&quot;:0,&quot;createDate&quot;:1604595761039,&quot;editDate&quot;:'
        + str(current_edit_data)
        + ',&quot;noteId&quot;:&quot;noteid-'
        + note_id
        + '&quot;,&quot;noteName&quot;:&quot;'
        + initialization_data["note_ids"][note_id]
        + '&quot;,&quot;notebg&quot;:0,&quot;notebgName&quot;:&quot;White paper&quot;,&quot;pageIds&quot;:['
        + current_pages_xml_list
        + ']}</string>'
    ]

with (Path().cwd() / 'output/recovered_xml_lines.txt').open(
    mode='w', encoding='UTF-8'
) as recovered_xml_lines_file:
    print(*recovered_xml_lines, sep='\n', file=recovered_xml_lines_file)

print(
    f"Data for notes' recovery is written to {Path('output/recovered_xml_lines.txt').resolve()}"
)

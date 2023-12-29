# Boyue Notes Recovery and Export

[![GitHub stars](https://img.shields.io/github/stars/Sterh20/boyue-notes-recovery-and-export.svg?style=social&label=Stars)](https://github.com/Sterh20/boyue-notes-recovery-and-export/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Sterh20/boyue-notes-recovery-and-export.svg?style=social&label=Forks)](https://github.com/Sterh20/boyue-notes-recovery-and-export/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/Sterh20/boyue-notes-recovery-and-export.svg?style=social&label=Watchers)](https://github.com/Sterh20/boyue-notes-recovery-and-export/watchers)
[![GitHub followers](https://img.shields.io/github/followers/Sterh20.svg?style=social&label=Followers)](https://github.com/Sterh20/?tab=followers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat)
[![Boyue](https://img.shields.io/badge/Boyue-8A2BE2)](https://www.facebook.com/BoyueLikebook/)

This repository contains three Python scripts for working with Boyue Notepad app data. The scripts are designed to assist in recovering missing lines from the `notes.xml` file, exporting notes PNG pages to PDF based on their names in the Notes app, and creating an input list of all notes in `notes.xml` for exporting.

## Scripts

1. [**notes_recovery.py**](notes_recovery.py)
   - **Purpose**: Recover missing lines from the `notes.xml` file.
   - **Motivation**: One day, the Notepad app decided to delete more notes than I asked for.
      <details>
       <summary>Detailed story</summary>

       I needed to delete 3 notes with 100 pages each. For the first time, I tried the "Batch Management" option in the Notepad menu. After hitting the delete button on my Likebook Alita, everything froze. I figured since the same happens when I manually delete large notes, it is normal. I left my tablet to do its job and forgot about it. An hour passed, and I started to worry. I tried to quit the operation but failed or quit with an error (I don't remember). I rebooted my tablet, but at this point, some of my old notes were deleted.

       At least it looked like so. I decided to inspect the contents of the notes folder in the root directory of the device on my computer. After some time, I found out that those notes that I had no intention to delete were still physically present, but the records that connect note ids with note name, page ids, and so on in `notes.xml` were deleted. So to solve this issue, I only needed to know note ids and their page ids. This info is in page's PNG and BOYUENOTE file names. I didn't check, but I guess the pages' ids are in the order of pages' creation. So to automate the gathering of page ids and proper record creation, I created this script.

      </details>

   - **Usage**: The script reads information from `init_data/data_for_recovery.json` and reconstructs missing lines from the `notes.xml` file, saving the result to `output/recovered_xml_lines.txt`. Then you need to copy the contents of `recovered_xml_lines.txt` to the end of `notes.xml` and save it. Copy modified `notes.xml` to some directory on the device manually using **<u>the device's file manager</u>**, **otherwise you will not get the desired results**. Reboot the tablet, and the lost notes should appear in the interface.
      <details>
       <summary>How to create <code>data_for_recovery.json</code>?</summary>

       To create `data_for_recovery.json`, you need notes' ids and notes' names. The easiest way to gather all missing notes' ids is to find a record in `notes.xml` that starts with `<string name="AllNote"`. In this record, you will find all note ids that are(?) and were(?) on the tablet. By searching ids in the file names of PNG files and inspecting them, you should find the missing notes' ids. After that, you should create `data_for_recovery.json` file with pairs of notes' ids and notes' names (you should recall the names of the notes or assign new ones) like this:

       ```json
       {
        "note_ids": {
          "1698500249858": "NoteName1",
          "1648706478981": "NoteName2",
          "1645719193695": "Notepad-2"
       },
       "boyeu_notes_folder": "input_data/notes"
       }
       ```

      </details>

2. [**notes_export.py**](notes_export.py)
   - **Purpose**: Export PNG notes to PDF by their names.
   - **Motivation**: When converting large notes (40 and more pages long) to PDF, the Notepad app crashes. The only other working (sometimes) option is to convert to HTML, which is not the preferable way to store this kind of data.
   - **Usage**: The script takes note names as command-line arguments (`-n` or `--notes_names`) and/or note names from [`data_for_export.json`](init_data/data_for_export.json) and then converts the corresponding PNG files to a PDF. The output PDF files are saved in the `export` folder.

3. [**create_export_json_for_all_notes.py**](create_export_json_for_all_notes.py)
   - **Purpose**: Create an input list of all valid notes in `notes.xml` for `notes_export.py`.
   - **Usage**: The script reads information from `init_data/data_to_export_all_notes.json` and extracts all note names from `notes.xml`, saving the result to `init_data/data_for_export.json`.

## Instructions

### Prerequisites

Before running the scripts, ensure that you have the following:

- Boyue Notepad application data, with PNG files:
  
  <details>
  
  <summary>How to properly get Notepad app data:</summary>
  
  Using any third party file manager (like [FX File Explorer](https://play.google.com/store/apps/details?id=nextapp.fx) or [Material Files](https://play.google.com/store/apps/details?id=me.zhanghai.android.files)) create zip file of `notes` folder in the root of the device.
  
  If you copy notes folder directly PNG files will not be copied.

  </details>

- `init_data` folder containing necessary JSON files (`data_for_recovery.json`, `data_to_export_all_notes.json`, and `data_for_export.json`).
- Python environment with required `img2pdf` dependency.
- To use all scripts you should have a file structure that looks like this:

   ```bash
   │   .gitignore
   │   create_export_json_for_all_notes.py
   │   LICENSE.txt
   │   notes_export.py
   │   notes_recovery.py
   │   README.MD
   │   requirements.txt
   │
   ├───export
   │
   ├───init_data
   │       data_for_export.json
   │       data_for_recovery.json
   │       data_to_export_all_notes.json
   │
   ├───input_data
   │   │
   │   └───notes
   │       ├───data
   │       │
   │       └───template
   │
   └───output
   ```

### Usage

1. Clone the repository:

   ```powershell
   git clone "https://github.com/Sterh20/boyue-notes-recovery-and-export"
   cd boyue-notes-recovery-and-export
   ```

2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Put the notes folder from the device into the `init_data` folder.
4. Run the desired script:

   ```powershell
   python notes_recovery.py
   ```

   ```powershell
   python notes_export.py -n "NoteName1, NoteName2, NoteName3"
   ```

   ```powershell
   python create_export_json_for_all_notes.py
   ```

## Important Notes

> [!WARNING]  
>
> - Ensure that the folder structure and file paths in the initialization JSON files are accurate.
> - Backup your Boyue Notepad data before using these scripts to avoid data loss.
> - The scripts have been tested with the Boyue Likebook Alita running BYRead-V2.3.3-2020041718 firmware. It should probably work on any Boyue device, but if it does not, please report it in an issue.

## License

This project is licensed under the [MIT License](LICENSE.txt). Feel free to customize and use the scripts according to your needs. If you encounter any issues or have suggestions, please open an [issue](https://github.com/Sterh20/boyue-notes-recovery-and-export/issues).

import os
import sys
import json
import shutil

class SortDownloads():

    def __init__(self) -> None:
        pass

    def check_directory(self):
        # Check if windows of
        if sys.platform != "win32":
            print("Can only run this script on Windows OS. Sorry bro.")
            sys.exit()

        # Change the working dict one back to be in the Downloads folder
        try:
            os.chdir(os.path.expanduser('~') + "\\Downloads")
        except FileNotFoundError:
            print("It appears that I could not find a 'Downloads' folder on your OS? Please add one to your user.")
            sys.exit()

    def check_duplicates(self, list):
        newlist = [] # empty list to hold unique elements from the list
        duplist = [] # empty list to hold the duplicate elements from the list
        for i in list:
            if i not in newlist:
                newlist.append(i)
            else:
                duplist.append(i) # this method catches the first 
        return duplist

    def listify_dict(self, dict):
        folders = []
        extensions = []
        for key,values in dict.items():
            folders.append(key)

            for value in values:
                extensions.append(value.lower())
        return folders, extensions


    def load_config(self):
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)

                folders, extensions = self.listify_dict(config)

                # Check for duplicates
                duplist = self.check_duplicates(extensions)


                print(f'Please address the following duplicates:\n {duplist}\n If you ignore my warning, I will just start making assumptions :)') if len(duplist) != 0 else print("Successfully loaded config without duplicates")
        except FileNotFoundError:
            print("Could not find your config file. Please add your config file")
            sys.exit()

        # Add more folders to the whielist
        folders.append("downloads_organizer")
        folders.append("OtherFolders")
        folders.append("Misc")
        return folders, extensions, config

    def organize(self, folders):
        files_in_downloads = os.listdir()

        for file in files_in_downloads:
            if not os.path.isdir(file):
                current_extension = file.split(".")[-1]
                file_to_organise = ".".join(file.split(".")[:-1])
                self.move_file(file_to_organise, current_extension)
            else:
                if not os.path.exists("OtherFolders"):
                    os.mkdir("OtherFolders")
                if file not in folders:
                    try:
                        shutil.move(file, f'OtherFolders//{file}')
                    except:
                        print(f'Could not move {file} to OtherFolders//{file}')

    def move_file(self, file, current_extension):
        matched_folders = [k for k, v in config.items() if current_extension.upper() in [v.upper() for v in v]]

        if len(matched_folders) != 0:
            # Assume the first
            matched_folder = matched_folders[0]

            # Make a folder if it doesn't already exist
            if not os.path.exists(matched_folder):
                os.mkdir(matched_folder)

            # Move the file
            try:
                shutil.move(f'{file}.{current_extension}', f'{matched_folder}//{file}.{current_extension}')
            except:
                print(f'Could not move {file}.{current_extension} to {matched_folder}//{file}.{current_extension}')
        else:
            print(f'Can move extension: {current_extension}. Adding to Misc')
            if not os.path.exists("Misc"):
                os.mkdir("Misc")
            try:
                if len(file) != 0:
                    shutil.move(f'{file}.{current_extension}', f'Misc//{file}.{current_extension}')
                else:
                    # No extension file
                    shutil.move(f'{current_extension}', f'Misc//{current_extension}')
            except:
                print(f'Could not move {file}.{current_extension} to Misc//{file}.{current_extension}')

        
# Start the main
if __name__ == "__main__":
    sd = SortDownloads()
    folders, extensions, config = sd.load_config()
    sd.check_directory()
    sd.organize(folders)
import time
import shutil
import os
import tkinter as tk
from tkinter import messagebox
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from collections import deque
import openpyxl
import threading


class NewFileHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.file_queue = deque()
        self.processing_flag = False
        self.processing_thread = threading.Thread(target=self.process_files)
        self.processing_thread.daemon = True  # Daemonize the thread
        self.processing_thread.start()

        self.pwd = os.getcwd()
        # self.pwd = os.path.dirname(__file__)

    def on_created(self, event):
        if event.is_directory:
            return
        self.file_queue.append(event.src_path)
        print(f'New file detected and queued: {event.src_path}')
        self.processing_flag = True

    def process_files(self):
        while True:
            if self.file_queue:
                file_path = self.file_queue.popleft()
                print(f'Processing file: {file_path}')
                self.create_backup(file_path)
                headflag = self.trigger_script(file_path)
                if headflag != True:
                    os.remove(file_path)


            if not self.file_queue and self.processing_flag:
                self.processing_flag = False
                self.notify_completion()

    def create_backup(self, file_path):
        backup_folder = os.path.join(self.pwd, "Backup")
        # backup_folder = os.path.join(self.pwd, "Test Data", "Backup")
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        file_name = os.path.basename(file_path)
        backup_path = os.path.join(backup_folder, file_name)
        shutil.copy2(file_path, backup_path)
        print(f'Backup created for {file_path} at {backup_path}')

    def trigger_script(self, file_path):
        print(f'Triggering script for the new file: {file_path}')
        # file_name = os.path.basename(file_path)

        
        upcFilePath = ""
        # upcFolderPath = os.path.join(self.pwd, "Test Data", "UPC")
        upcFolderPath = 'G:\\ftproot\\labelftp\\CouponUPCRemoval\\UPC'

        for entry in os.listdir(upcFolderPath):
            full_path = os.path.join(upcFolderPath, entry)
            if os.path.isfile(full_path):
                extension = os.path.splitext(full_path)[1]
                if extension == ".xlsx":
                    upcFilePath = full_path

        if not upcFilePath:
            # print(f"Error: Does not exist any 'xlsx' file in folder 'UPC'.")
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", "Does not exist any 'xlsx' file in folder 'UPC', Please verify....")
            root.destroy()
            return
        

        arrUPC = []
        workbook = openpyxl.load_workbook(upcFilePath)
        for eachSheet in workbook.worksheets:
            if eachSheet.sheet_state == "visible":
                # sheet = workbook.worksheets[i]
                for column in eachSheet.iter_cols():
                    column_name = column[0].value
                    if column_name == "UPC":
                        for i, cell in enumerate(column):
                            if i != 0:
                                row = cell.row
                                if eachSheet.row_dimensions[row].hidden:
                                    continue
                                upcstr = str(cell.value)
                                upcstr = upcstr.replace("-", "")
                                if upcstr and upcstr != 'None' :
                                    # print(type(upcstr))
                                    arrUPC.append(upcstr)



        tagFilePath = file_path
        if not os.path.exists(tagFilePath):
            print(f"Error: {tagFilePath} does not exist.")
            return

        with open(tagFilePath, 'r+') as sfile:
            data = sfile.readlines()
            sfile.seek(0)
            sfile.truncate()

        headflag = False
        sfile = open(tagFilePath, 'w')
        for line in data:
            start = 45  # upc 45 - 57 (13 digits)
            end = 58
            headval = line[116:118]  
            for exlUPC in arrUPC:
                # print(exlUPC)
                index = line.find(exlUPC, start, end)
                if index > 0:
                    break
            if index == -1:
                if headval != '00':
                    headflag = True
                sfile.write(line)             
        return headflag

    def notify_completion(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Process complete", "All files have been completed successfully..")
        root.destroy()

def monitor_folder(path_to_watch):
    observer = Observer()
    event_handler = NewFileHandler()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()
    print(f'Started monitoring folder: {path_to_watch}')

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
        print('Stopped monitoring.')

    observer.join()


if __name__ == "__main__":
    pwd = os.getcwd()
    # pwd = os.path.dirname(__file__)
    folder_to_monitor = os.path.join(pwd, "Tag")
    # folder_to_monitor = os.path.join(pwd,"Test Data", "Tag")


    if not os.path.exists(folder_to_monitor):
        print(f"Error: {folder_to_monitor} does not exist.")
    else:
        monitor_folder(folder_to_monitor)
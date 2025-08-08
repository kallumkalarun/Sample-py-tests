import time
import shutil
import os
import tkinter as tk
from tkinter import messagebox
import openpyxl


def upcremovalProcess(upcFilepath, tagFolderpath):

    arrUPC = []
    workbook = openpyxl.load_workbook(upcFilepath)
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

    tagFileCount = 0
    for tagfile in os.listdir(tagFolderpath):
        orgtagfile_Path = os.path.join(tagFolderpath, tagfile)
        # orgtagfull_name = os.path.basename(orgtagfile_Path)
        orgtagbase_name = os.path.splitext(tagfile)[0]
        extension = os.path.splitext(tagfile)[1]

        if not extension.lower() in [".xls", ".xlsx", ".xlsm", ".xlsb", ".csv", ".pdf", ".jpg", ".png", ".doc", ".docx", ".docm", ".bmp", ".msg", ".ppt", ".pptx", ".pptm"]:
            tagFileCount = tagFileCount + 1
            bkptagfile_name = orgtagbase_name + " - Copy" + extension

            bkptagfile_Path = os.path.join(tagFolderpath, bkptagfile_name)
            shutil.copy2(orgtagfile_Path, bkptagfile_Path)


            with open(orgtagfile_Path, 'r+') as sfile:
                data = sfile.readlines()
                sfile.seek(0)
                sfile.truncate()

            headflag = False
            sfile = open(orgtagfile_Path, 'w')
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
     
            if headflag != True:
                os.remove(orgtagfile_Path)    
                
    return tagFileCount








#     tagFilePath = file_path
#     if not os.path.exists(tagFilePath):
#         print(f"Error: {tagFilePath} does not exist.")
#         return

#     with open(tagFilePath, 'r+') as sfile:
#         data = sfile.readlines()
#         sfile.seek(0)
#         sfile.truncate()

#     headflag = False
#     sfile = open(tagFilePath, 'w')
#     for line in data:
#         start = 45  # upc 45 - 57 (13 digits)
#         end = 58
#         headval = line[116:118]  
#         for exlUPC in arrUPC:
#             # print(exlUPC)
#             index = line.find(exlUPC, start, end)
#             if index > 0:
#                 break
#         if index == -1:
#             if headval != '00':
#                 headflag = True
#             sfile.write(line)             
#     return headflag

# # #--------------


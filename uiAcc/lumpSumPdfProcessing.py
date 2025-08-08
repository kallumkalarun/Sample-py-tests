import os
import sys
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
import tkinter as tk
from tkinter import messagebox
from PySide6.QtWidgets import QApplication, QMessageBox

def splitPdf(SourcePdfPath):
    # SourcePdfPath = os.path.join(SourcePath, "SourcePdf")
    SourcePath = os.path.dirname(SourcePdfPath)

    output_dir = os.path.join(SourcePath, "Split Pdfs")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    files_in_dir = os.listdir(output_dir)
    if files_in_dir:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "There are files available in the 'Split Pdfs' folder, Please delete and rerun.")
        root.destroy()
        return 

    sPdfFilePath = SourcePdfPath

    # sPdfFilePath = ""
    # for entry in os.listdir(SourcePdfPath):
    #     full_path = os.path.join(SourcePdfPath, entry)
    #     if os.path.isfile(full_path):
    #         extension = os.path.splitext(full_path)[1]
    #         if extension == ".pdf":
    #             sPdfFilePath = full_path

    # if not sPdfFilePath:
    #     root = tk.Tk()
    #     root.withdraw()
    #     messagebox.showerror("Error", "Does not exist any 'pdf' file in 'SourcePdf' folder, Please verify....")
    #     root.destroy()
    #     return   

    try:
        # os.makedirs(output_dir, exist_ok=True)
        reader = PdfReader(sPdfFilePath)
        num_pages = len(reader.pages)

        for i in range(num_pages):
            base_name = "page -"
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            output_filename = os.path.join(output_dir, f"{base_name} {i+1}.pdf")
            with open(output_filename, "wb") as outfile:
                writer.write(outfile)
            print(f"Saved: {output_filename}")

            newFileName = getFileNameFromPdf(output_filename)

            newOutput_filename = os.path.join(output_dir, f"{newFileName}.pdf")

            # Rename the temporary file to the final filename
            os.rename(output_filename, newOutput_filename)
            print(f"Renamed to: {newOutput_filename}")

            
        print(f"\nSuccessfully split '{os.path.basename(sPdfFilePath)}' into {num_pages} pages in '{output_dir}'.")
        return num_pages

    except FileNotFoundError:
        print(f"Error: PDF file not found at '{SourcePdfPath}'")
    except Exception as e:
        print(f"An error occurred: {e}")

def getFileNameFromPdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            InvoiceNumber = "0000000"
            AccountNumber = "0000000"
            SupplierName = "NO SUPPLIER"
            tempSName = ""
            invNo_fg = False
            accNo_fg = False
            sName_fg = False
            for line in text.split('\n'):
                if "Invoice Number" in line:
                    parts = line.split("Invoice Number")
                    if len(parts) > 1:
                        InvoiceNumber =  parts[1].strip()
                        invNo_fg = True

                if "Account Number" in line:
                    parts = line.split("Account Number")
                    if len(parts) > 1:
                        AccountNumber =  parts[1].strip()
                        accNo_fg = True

                if "Authorized By" in line:
                    SupplierName = tempSName
                    sName_fg = True
                
                if accNo_fg and sName_fg and invNo_fg:
                    newOutput_filename = f"{InvoiceNumber} - {SupplierName} - {AccountNumber}"
                    return newOutput_filename

                tempSName = line

        newOutput_filename = f"{InvoiceNumber} - {SupplierName} - {AccountNumber}"
        return newOutput_filename
    except Exception as e:
        print(f"Error extracting info from pdfs: {e}")
        return None



# if __name__ == "__main__":
#     sourcePath = os.getcwd()
#     splitPdf(sourcePath)




import sys
import os
from PySide6.QtWidgets import  QApplication, QMainWindow, QMenuBar, QMenu, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QPushButton, QFileDialog, QLineEdit, QMessageBox, QSizePolicy
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
import uiautoremovalUPC

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = app 
        # self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("GE Non Banner")

        self.tab_widget = QTabWidget()
        self.excel_path_label = None 
        self.folder_path_label = None 


        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.label = QLabel("Welcome! GE Non-Banner Team Tasks.", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; color: #154360; background-color: #a9cce3; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.label)
        self.setCentralWidget(self.central_widget)


        #Menubar and menus
        menuBar = self.menuBar()

        # accMenu =menuBar.addMenu("Accounting")
        # lsMenu = accMenu.addAction("Lump Sum")
        # lsMenu.triggered.connect(self.show_accounting_options)

        dicpMenu = menuBar.addMenu("DI / CP")
        ruMenu = dicpMenu.addAction("Remove UPC")
        ruMenu.triggered.connect(self.show_rumenu_options)

        # tvMenu = dicpMenu.addAction("Tag Verification")
        # tvMenu.triggered.connect(self.show_tagveri_options)

        clMenu = menuBar.addAction("Close Tab")
        clMenu.triggered.connect(self._clear_tabs)

        qtMenu = menuBar.addAction("Quit App")
        qtMenu.triggered.connect(self.quit_app)



        self.setMenuBar(menuBar)
        # self.showMaximized()
        # Set the default width and height
        default_width = 950
        default_height = 620
        self.resize(default_width, default_height)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)   

    def _clear_tabs(self):
        if self.tab_widget:
            """Closes all existing tabs in the tab widget."""
            for i in reversed(range(self.tab_widget.count())):
                self.tab_widget.removeTab(0)

    def show_rumenu_options(self):
        self._clear_tabs()
        # Create a new tab for remove upc operations
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setSpacing(15)


        self.tHeader_label = QLabel("Remove UPC Process", self)
        self.tHeader_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tHeader_label.setFixedHeight(30) # Set fixed height for label
        self.tHeader_label.setFixedWidth(750) # Set fixed width for label
        self.tHeader_label.setStyleSheet("font-size: 18px; color: #154360; background-color: #a9cce3; font-weight: bold; padding: 5px;")
        tHeader_layout = QHBoxLayout()
        tHeader_layout.addWidget(self.tHeader_label)
        tab_layout.addLayout(tHeader_layout)


        # --- New Browse Excel File Button ---
        self.excel_path_label = QLabel("No Excel file selected") # Create this label in your UI
        browse_button_excel = QPushButton("Select UPC List")
        browse_button_excel.clicked.connect(self._browse_excel)
        browse_button_excel.setFixedHeight(30)
        browse_button_excel.setFixedWidth(120) # Adjusted width for "Browse Excel"
        browse_button_excel.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px;")  
        browse_button_excel.setStyleSheet("QPushButton {background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px; } QPushButton:hover {background-color: #005682; border-color: #005682; }")
     

        # --- New Browse Folder Button ---
        self.folder_path_label = QLabel("No Tag folder selected") # Create this label in your UI
        browse_button_folder = QPushButton("Select Tag Folder")
        browse_button_folder.clicked.connect(self._browse_folder)
        browse_button_folder.setFixedHeight(30)
        browse_button_folder.setFixedWidth(120) # Adjusted width for "Select Folder"
        browse_button_folder.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px;")  
        browse_button_folder.setStyleSheet("QPushButton {background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px; } QPushButton:hover {background-color: #005682; border-color: #005682; }")


        # Label to display the Excel path
        self.excel_path_label = QLineEdit()
        self.excel_path_label.setReadOnly(True)
        self.excel_path_label.setFixedHeight(30) # Set fixed height for label
        self.excel_path_label.setFixedWidth(750) # Set fixed width for label
        self.excel_path_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #00008B; background-color: #fdfefe; padding-left: 5px;")

        # Layout to hold the browse button and the Excel path label
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(browse_button_excel)
        browse_layout.addWidget(self.excel_path_label)
        tab_layout.addLayout(browse_layout)


        # Label to display the Folder path
        self.folder_path_label = QLineEdit()
        self.folder_path_label.setReadOnly(True)
        self.folder_path_label.setFixedHeight(30) # Set fixed height for label
        self.folder_path_label.setFixedWidth(750) # Set fixed width for label
        self.folder_path_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #00008B; background-color: #fdfefe; padding-left: 5px;")

        # Layout to hold the browse button and the Excel path label
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(browse_button_folder)
        browse_layout.addWidget(self.folder_path_label)
        tab_layout.addLayout(browse_layout)



        # Submit button
        submit_button = QPushButton("SUBMIT")
        submit_button.clicked.connect(self._removingUPC)
        submit_button.setFixedWidth(150)
        submit_button.setFixedHeight(35)
        submit_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px;")
        submit_button.setStyleSheet("QPushButton {background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px; } QPushButton:hover {background-color: #005682; border-color: #005682; }"  # Darker shade on hover
        )


        button_layout = QHBoxLayout()
        button_layout.addWidget(submit_button)
        tab_layout.addLayout(button_layout)


        # 2. Change default background color of Tab
        tab.setStyleSheet(
            "background-color: #a9cce3;" 
        )
        tab.setStyleSheet(
            "QWidget {"
            "    background-color: #d4e6f1; }"
            "QTabWidget::tab-bar {"
            "    alignment: center; }"
            "QTabBar::tab {"
            "    background-color: #E0FFFF; color: black; font-size: 12px; font-weight: bold;"
            "    padding: 8px 20px; border-top-left-radius: 5px; border-top-right-radius: 5px;"
            "    border: 1px solid #E0FFFF; }"
            "QTabBar::tab:selected {"
            "    background-color: #a93226; color: black; border-bottom: 2px solid #a93226; }"
            "QTabBar::tab:hover {"
            "    background-color: #ADD8E6; border-color: #ADD8E6; }"  # Light blue on hover
        )


        tab.setLayout(tab_layout)
        self.tab_widget.addTab(tab, "Remove UPC")
        self.tab_widget.setCurrentWidget(tab)


    def show_tagveri_options(self):
        self._clear_tabs()
        # Create a new tab for Tag Verification operations
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        # label = QLabel("Tag Verification:\n- Tag Verification in batch file...")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # tab_layout.addWidget(label)
        tab.setLayout(tab_layout)
        self.tab_widget.addTab(tab, "Tag Verification")
        self.tab_widget.setCurrentWidget(tab)

    def quit_app(self):
        self.app.quit()


    def _browse_excel(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select Excel File",
            "",  # Start in the current directory or last visited
            "Excel Files (*.xlsx *.xls);;All Files (*)"
        )
        if file_path:
            self.excel_path_label.setText(file_path)


    def _browse_folder(self):
        file_dialog = QFileDialog()
        folder_path = file_dialog.getExistingDirectory(
            self,
            "Select Tag Folder",
            "" 
        )
        if folder_path:
            self.folder_path_label.setText(folder_path)



    def _removingUPC(self):
        upcFilepath = self.excel_path_label.text()
        tagFolderpath = self.folder_path_label.text()

        if upcFilepath:
            if os.path.isfile(upcFilepath):
                extension = os.path.splitext(upcFilepath)[1]
                if not extension.lower() in [".xls", ".xlsx"]:
                    QMessageBox.warning(self,"Warning !", "Please select UPC list as '.xls' or '.xlsx' file format to continue...!", QMessageBox.Ok)
                else:

                    if tagFolderpath:
                        if os.path.isdir(tagFolderpath):
                            if any(os.path.isfile(os.path.join(tagFolderpath, f)) for f in os.listdir(tagFolderpath)):

                                tagFileCount = uiautoremovalUPC.upcremovalProcess(upcFilepath, tagFolderpath)

                                if tagFileCount>0:
                                    QMessageBox.information(self,"Result", f"Sucessfully verified and removed upc from {tagFileCount} Tag File(s) and its ready to upload.", QMessageBox.Ok)
                                else:
                                    QMessageBox.information(self,"Result", f"There is no appropriate Tag file available in Tag Folder to remove UPC", QMessageBox.Ok)

                            else:
                                # No files in the directory (it might be empty or contain only subdirectories)
                                QMessageBox.warning(self, "Warning !", f"No files found in the selected Tag folder, Please revise", QMessageBox.Ok)

                    else:
                        QMessageBox.warning(self,"Warning !", "Please select a Tag file Folder to continue...!", QMessageBox.Ok)
        else:
            # print("No PDF file selected.")
            QMessageBox.warning(self,"Warning !", "Please select UPC list file to continue...!", QMessageBox.Ok)







    def update_main_window(self, message):
            self.label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # mainWindow.showMaximized()
    mainWindow.show()
    sys.exit(app.exec())


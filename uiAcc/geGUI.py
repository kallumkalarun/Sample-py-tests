
import sys
import os
from PySide6.QtWidgets import  QApplication, QMainWindow, QMenuBar, QMenu, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTabWidget, QPushButton, QFileDialog, QLineEdit, QMessageBox, QSizePolicy
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor, QFont
import lumpSumPdfProcessing

def do_nothing():
    print("Menu item clicked")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app = app 
        # self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("GE Non Banner")

        self.tab_widget = QTabWidget()
        self.pdf_path_label = None # Make sure this is initialized

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)        

        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        self.label = QLabel("Welcome! GE Non-Banner Team Tasks.", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; color: #154360; background-color: #a9cce3; font-weight: bold; padding: 5px;")
        self.layout.addWidget(self.label)
        self.setCentralWidget(self.central_widget)


        #Menubar and menus
        menuBar = self.menuBar()

        accMenu =menuBar.addMenu("Accounting")
        lsMenu = accMenu.addAction("Lump Sum")
        lsMenu.triggered.connect(self.show_accounting_options)

        # dicpMenu = menuBar.addMenu("DI / CP")
        # ruMenu = dicpMenu.addAction("Remove UPC")
        # ruMenu.triggered.connect(self.show_rumenu_options)

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

    def show_accounting_options(self):
        self._clear_tabs()
        # Create a new tab for accounting operations
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        tab_layout.setSpacing(15)




        # Browse button
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self._browse_pdf)
        browse_button.setFixedHeight(30)  # Set fixed height for Browse button
        browse_button.setFixedWidth(120)
        browse_button.setStyleSheet("background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px;")  
        browse_button.setStyleSheet("QPushButton {background-color: #008CBA; color: white; font-size: 14px; font-weight: bold; border: 2px solid #008CBA; border-radius: 5px; } QPushButton:hover {background-color: #005682; border-color: #005682; }"  # Darker shade on hover
        )

        # Label to display the PDF path
        self.pdf_path_label = QLineEdit()
        self.pdf_path_label.setReadOnly(True)
        self.pdf_path_label.setFixedHeight(30) # Set fixed height for label
        self.pdf_path_label.setFixedWidth(750) # Set fixed width for label
        self.pdf_path_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #00008B; background-color: #fdfefe; padding-left: 5px;")

        # Layout to hold the browse button and the PDF path label
        browse_layout = QHBoxLayout()
        browse_layout.addWidget(browse_button)
        browse_layout.addWidget(self.pdf_path_label)
        tab_layout.addLayout(browse_layout)


        # Submit button
        submit_button = QPushButton("SUBMIT")
        submit_button.clicked.connect(self._process_pdf)
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
        self.tab_widget.addTab(tab, "Lump Sum")
        self.tab_widget.setCurrentWidget(tab)


    def show_rumenu_options(self):
        self._clear_tabs()
        # Create a new tab for Remove UPC operations
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        # label = QLabel("Remove UPC:\n- Remove UPC from Tag file...")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # tab_layout.addWidget(label)
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


    def _browse_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Select PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.pdf_path_label.setText(file_path)



    def _process_pdf(self):
        pdf_path = self.pdf_path_label.text()
        if pdf_path:
            # print(f"Processing PDF file: {pdf_path}")
            if os.path.isfile(pdf_path):
                extension = os.path.splitext(pdf_path)[1]
                if not extension == ".pdf":
                    QMessageBox.warning(self,"Warning !", "Please select a 'PDF' file to continue...!", QMessageBox.Ok)
                else:
                    # print("Call lumpSumProcess here with pdf_path as parameter")
                    num_pages = lumpSumPdfProcessing.splitPdf(pdf_path)
                    if num_pages:
                        QMessageBox.information(self,"Result", f"Sucessfully split the selected file in to '{num_pages}' number of pages.", QMessageBox.Ok)
        else:
            # print("No PDF file selected.")
            QMessageBox.warning(self,"Warning !", "Please select appropriate 'PDF' file to continue...!", QMessageBox.Ok)


    def update_main_window(self, message):
            self.label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    # mainWindow.showMaximized()
    mainWindow.show()
    sys.exit(app.exec())


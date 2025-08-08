from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

def split_pdf(main_window):  # Receive the main window instance
    """
    This function performs the PDF splitting and interacts with the main window.
    """
    dialog = QDialog()
    layout = QVBoxLayout(dialog)
    label = QLabel("Splitting PDF...", dialog)
    layout.addWidget(label)
    close_button = QPushButton("Close", dialog)
    layout.addWidget(close_button)

    def on_close_button_clicked():
        # Update the main window's label
        main_window.update_main_window("PDF splitting complete!")
        dialog.close()

    close_button.clicked.connect(on_close_button_clicked)
    dialog.exec()  # Use dialog.exec() to show the dialog
    # No return value is needed.  The dialog updates the main window directly.
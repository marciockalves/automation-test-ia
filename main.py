import sys
from PySide6.QtWidgets import QApplication
from src.application_board import ApplicationBoard

def main():
    app = QApplication(sys.argv)
    
    # Estilo visual (CSS/QSS)
    app.setStyleSheet("""
        QMainWindow { background-color: #1e1e1e; }
        QTreeView { background-color: #252526; color: #cccccc; border: none; padding: 5px; }
        QTextEdit { background-color: #1e1e1e; color: #d4d4d4; border: none; padding: 10px; }
        QPushButton { 
            background-color: #37373d; 
            color: white; 
            border: 1px solid #454545; 
            border-radius: 4px; 
            margin-bottom: 5px;
        }
        QPushButton:hover { background-color: #454545; }
        QSplitter::handle { background-color: #2d2d2d; width: 2px; }
    """)

    window = ApplicationBoard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
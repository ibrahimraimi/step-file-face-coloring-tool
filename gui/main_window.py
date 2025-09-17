"""
Main GUI window for STEP File Face Coloring Tool
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QComboBox, QGroupBox, QTextEdit, QProgressBar,
                             QMessageBox, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

from core.step_processor import StepProcessor


class ProcessingThread(QThread):
    """Thread for processing STEP files to avoid GUI freezing"""
    
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, input_path, output_path, orientation_criteria, coloring_criteria):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.orientation_criteria = orientation_criteria
        self.coloring_criteria = coloring_criteria
        self.processor = StepProcessor()
    
    def run(self):
        try:
            self.status.emit("Loading STEP file...")
            self.progress.emit(20)
            
            self.status.emit("Processing orientation...")
            self.progress.emit(40)
            
            self.status.emit("Applying face colors...")
            self.progress.emit(60)
            
            self.status.emit("Saving colored STEP file...")
            self.progress.emit(80)
            
            # Process the file
            success = self.processor.process_file(
                self.input_path, 
                self.output_path, 
                self.orientation_criteria, 
                self.coloring_criteria
            )
            
            self.progress.emit(100)
            self.status.emit("Processing complete!")
            
            if success:
                self.finished.emit(True, f"Successfully created: {os.path.basename(self.output_path)}")
            else:
                self.finished.emit(False, "Processing failed")
                
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.input_file_path = None
        self.output_file_path = None
        self.processing_thread = None
        
        self.init_ui()
        self.setup_styles()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("STEP File Face Coloring Tool")
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("STEP File Face Coloring Tool")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # File selection section
        file_group = self.create_file_selection_group()
        main_layout.addWidget(file_group)
        
        # Settings section
        settings_group = self.create_settings_group()
        main_layout.addWidget(settings_group)
        
        # Processing section
        processing_group = self.create_processing_group()
        main_layout.addWidget(processing_group)
        
        # Status section
        status_group = self.create_status_group()
        main_layout.addWidget(status_group)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()
    
    def create_file_selection_group(self):
        """Create file selection group"""
        group = QGroupBox("File Selection")
        layout = QVBoxLayout(group)
        
        # Input file selection
        input_layout = QHBoxLayout()
        self.input_file_label = QLabel("No file selected")
        self.input_file_label.setStyleSheet("border: 1px solid #ccc; padding: 8px; background-color: #f9f9f9;")
        input_layout.addWidget(self.input_file_label, 1)
        
        self.select_file_btn = QPushButton("Select File")
        self.select_file_btn.clicked.connect(self.select_input_file)
        input_layout.addWidget(self.select_file_btn)
        
        layout.addLayout(input_layout)
        
        # File info
        self.file_info_label = QLabel("")
        self.file_info_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.file_info_label)
        
        return group
    
    def create_settings_group(self):
        """Create settings group"""
        group = QGroupBox("Processing Settings")
        layout = QGridLayout(group)
        
        # Orientation settings
        layout.addWidget(QLabel("Orientation:"), 0, 0)
        self.orientation_combo = QComboBox()
        self.orientation_combo.addItems(["Auto", "Manual", "Principal Axes"])
        layout.addWidget(self.orientation_combo, 0, 1)
        
        # Coloring settings
        layout.addWidget(QLabel("Coloring Method:"), 1, 0)
        self.coloring_combo = QComboBox()
        self.coloring_combo.addItems(["Random Colors", "Gradient", "Custom Palette"])
        layout.addWidget(self.coloring_combo, 1, 1)
        
        # Color count
        layout.addWidget(QLabel("Number of Colors:"), 2, 0)
        self.color_count_combo = QComboBox()
        self.color_count_combo.addItems(["5", "10", "15", "20"])
        self.color_count_combo.setCurrentText("10")
        layout.addWidget(self.color_count_combo, 2, 1)
        
        return group
    
    def create_processing_group(self):
        """Create processing group"""
        group = QGroupBox("Processing")
        layout = QVBoxLayout(group)
        
        # Process button
        self.process_btn = QPushButton("Process File")
        self.process_btn.setMinimumHeight(40)
        self.process_btn.clicked.connect(self.process_file)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return group
    
    def create_status_group(self):
        """Create status group"""
        group = QGroupBox("Status")
        layout = QVBoxLayout(group)
        
        # Status text
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(100)
        self.status_text.setReadOnly(True)
        self.status_text.append("Ready to process STEP files...")
        layout.addWidget(self.status_text)
        
        return group
    
    def setup_styles(self):
        """Setup application styles"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px;
                text-align: center;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QComboBox {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
        """)
    
    def select_input_file(self):
        """Select input STEP file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select STEP File",
            "",
            "STEP Files (*.stp *.step);;All Files (*)"
        )
        
        if file_path:
            self.input_file_path = file_path
            filename = os.path.basename(file_path)
            self.input_file_label.setText(filename)
            
            # Generate output filename
            base_name = os.path.splitext(filename)[0]
            output_dir = os.path.dirname(file_path)
            self.output_file_path = os.path.join(output_dir, f"{base_name}_colored.step")
            
            # Update file info
            file_size = os.path.getsize(file_path)
            self.file_info_label.setText(f"File size: {file_size:,} bytes")
            
            # Enable process button
            self.process_btn.setEnabled(True)
            
            self.status_text.append(f"Selected file: {filename}")
    
    def process_file(self):
        """Process the selected STEP file"""
        if not self.input_file_path:
            QMessageBox.warning(self, "Warning", "Please select a STEP file first.")
            return
        
        # Disable process button and show progress
        self.process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Get settings
        orientation_criteria = self.orientation_combo.currentText().lower().replace(" ", "_")
        coloring_criteria = {
            "method": self.coloring_combo.currentText().lower().replace(" ", "_"),
            "count": int(self.color_count_combo.currentText())
        }
        
        # Start processing thread
        self.processing_thread = ProcessingThread(
            self.input_file_path,
            self.output_file_path,
            orientation_criteria,
            coloring_criteria
        )
        
        self.processing_thread.progress.connect(self.progress_bar.setValue)
        self.processing_thread.status.connect(self.update_status)
        self.processing_thread.finished.connect(self.processing_finished)
        
        self.processing_thread.start()
    
    def update_status(self, message):
        """Update status text"""
        self.status_text.append(message)
        self.status_text.ensureCursorVisible()
    
    def processing_finished(self, success, message):
        """Handle processing completion"""
        self.progress_bar.setVisible(False)
        self.process_btn.setEnabled(True)
        
        if success:
            self.status_text.append(f"✓ {message}")
            QMessageBox.information(self, "Success", message)
        else:
            self.status_text.append(f"✗ {message}")
            QMessageBox.critical(self, "Error", message)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("STEP File Face Coloring Tool")
    app.setApplicationVersion("1.0")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

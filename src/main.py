from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QSpinBox, QRadioButton, QSlider, QCheckBox,
    QTextEdit, QPushButton, QMessageBox,
    QVBoxLayout, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
import sys
import csv
import json
import xml.etree.ElementTree as ET
from datetime import datetime

class VolleyballRegistration(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Volleyball Registration Form")
        self.resize(800, 600)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # Titel
        title = QLabel("Volleyball Registration Form")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

        # Name
        main_layout.addWidget(QLabel("Participant Name"))

        name_layout = QHBoxLayout()

        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("First")

        self.last_name = QLineEdit()
        self.last_name.setPlaceholderText("Last")

        name_layout.addWidget(self.first_name)
        name_layout.addWidget(self.last_name)

        main_layout.addLayout(name_layout)

        # Alter
        main_layout.addWidget(QLabel("Age"))

        self.age = QSpinBox()
        self.age.setRange(0, 120)

        main_layout.addWidget(self.age)

        # Mittlerer Bereich
        middle_layout = QHBoxLayout()

        # Linke Seite
        left_layout = QVBoxLayout()

        gender_label = QLabel("Gender:")
        left_layout.addWidget(gender_label)

        self.male = QRadioButton("Male")
        self.female = QRadioButton("Female")

        left_layout.addWidget(self.male)
        left_layout.addWidget(self.female)

        left_layout.addSpacing(20)

        satisfaction_label = QLabel("Satisfaction (0-10):")
        left_layout.addWidget(satisfaction_label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 10)

        left_layout.addWidget(self.slider)

        left_layout.addSpacing(20)

        self.agree = QCheckBox("I agree to the terms and conditions.")
        left_layout.addWidget(self.agree)

        # Rechte Seite
        right_layout = QVBoxLayout()

        notes_label = QLabel("Notes:")
        right_layout.addWidget(notes_label)

        self.notes = QTextEdit()
        right_layout.addWidget(self.notes)

        middle_layout.addLayout(left_layout)
        middle_layout.addLayout(right_layout)

        main_layout.addLayout(middle_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.save_button = QPushButton("Save/Register")
        self.save_button.clicked.connect(self.register)

        self.save_csv_button = QPushButton("Save as CSV")
        self.save_csv_button.clicked.connect(lambda: self.save_data("csv"))

        self.save_json_button = QPushButton("Save as JSON")
        self.save_json_button.clicked.connect(lambda: self.save_data("json"))

        self.save_xml_button = QPushButton("Save as XML")
        self.save_xml_button.clicked.connect(lambda: self.save_data("xml"))

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.save_csv_button)
        button_layout.addWidget(self.save_json_button)
        button_layout.addWidget(self.save_xml_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_gender(self):
        if self.male.isChecked():
            return "Male"
        if self.female.isChecked():
            return "Female"
        return "Not Selected"

    def collect_data(self):
        return {
            "first_name": self.first_name.text(),
            "last_name": self.last_name.text(),
            "age": self.age.value(),
            "gender": self.get_gender(),
            "satisfaction": self.slider.value(),
            "agreement": self.agree.isChecked(),
            "notes": self.notes.toPlainText(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def register(self):
        data = self.collect_data()
        message = (
            f"Name: {data['first_name']} {data['last_name']}\n"
            f"Age: {data['age']}\n"
            f"Gender: {data['gender']}\n"
            f"Satisfaction: {data['satisfaction']}\n"
            f"Agreement: {data['agreement']}\n"
            f"Notes: {data['notes']}\n"
            f"Timestamp: {data['timestamp']}"
        )

        QMessageBox.information(
            self,
            "Registration Saved",
            message
        )

    def save_data(self, format_type):
        data = self.collect_data()

        # Dateinamen vorschlagen
        default_filename = f"volleyball_registration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Dateiauswahl-Dialog öffnen
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Data",
            default_filename,
            f"{format_type.upper()} Files (*.{format_type})"
        )

        if not file_path:
            return  # Abbruch, wenn kein Dateipfad ausgewählt

        try:
            if format_type == "csv":
                self.save_as_csv(data, file_path)
            elif format_type == "json":
                self.save_as_json(data, file_path)
            elif format_type == "xml":
                self.save_as_xml(data, file_path)

            QMessageBox.information(
                self,
                "Success",
                f"Data saved successfully as {format_type.upper()}!"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save data: {str(e)}"
            )

    def save_as_csv(self, data, file_path):
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data.keys())
            writer.writerow(data.values())

    def save_as_json(self, data, file_path):
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def save_as_xml(self, data, file_path):
        root = ET.Element("Registration")
        for key, value in data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)

        tree = ET.ElementTree(root)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VolleyballRegistration()
    window.show()
    sys.exit(app.exec())

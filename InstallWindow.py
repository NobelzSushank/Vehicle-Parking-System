from PyQt5.QtWidgets import QVBoxLayout, QLabel, QLabel, QPushButton, QWidget, QLineEdit
from LoginWindow import LoginScreen
import json
from DatabaseOperation import DBOperation

class InstallWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Install Vehichle Parking System")
        self.resize(350, 300)

        layout = QVBoxLayout()
        label_db_name = QLabel("Database Name: ")
        label_db_username = QLabel("Database Userame: ")
        label_db_password = QLabel("Database Password: ")
        label_admin_username = QLabel("Admin Username: ")
        label_admin_password = QLabel("Admin Password: ")
        label_no_of_two_seater = QLabel("No. Of Two Wheeler Space: ")
        label_no_of_four_seater = QLabel("No. Of Four Wheeler Space: ")

        self.input_db_name = QLineEdit()
        self.input_db_name.setText("py_vehicle_parking")
        self.input_db_username = QLineEdit()
        self.input_db_username.setText("vehicle_user")
        self.input_db_password = QLineEdit()
        self.input_db_password.setText("vehicle_password")
        self.input_admin_username = QLineEdit()
        self.input_admin_password = QLineEdit()
        self.input_no_of_two_seater = QLineEdit()
        self.input_no_of_four_seater = QLineEdit()

        buttonSave = QPushButton("save config")

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color:red")

        layout.addWidget(label_db_name)
        layout.addWidget(self.input_db_name)
        layout.addWidget(label_db_username)
        layout.addWidget(self.input_db_username)
        layout.addWidget(label_db_password)
        layout.addWidget(self.input_db_password)
        layout.addWidget(label_admin_username)
        layout.addWidget(self.input_admin_username)
        layout.addWidget(label_admin_password)
        layout.addWidget(self.input_admin_password)
        layout.addWidget(label_no_of_two_seater)
        layout.addWidget(self.input_no_of_two_seater)
        layout.addWidget(label_no_of_four_seater)
        layout.addWidget(self.input_no_of_four_seater)

        layout.addWidget(buttonSave)

        layout.addWidget(self.error_label)

        buttonSave.clicked.connect(self.showStepInfo)

        self.setLayout(layout)


    def showStepInfo(self):
        if self.input_db_name.text() == "":
            self.error_label.setText("Please Enter DB Name")
            return

        if self.input_db_username.text() == "":
            self.error_label.setText("Please Enter DB Username")
            return

        if self.input_db_password.text() == "":
            self.error_label.setText("Please Enter DB Password")
            return

        if self.input_admin_username.text() == "":
            self.error_label.setText("Please Enter Admin Username")
            return

        if self.input_admin_password.text() == "":
            self.error_label.setText("Please Enter Admin Password")
            return

        if self.input_no_of_two_seater.text() == "":
            self.error_label.setText("Please Enter Two Wheeler Space")
            return

        if self.input_no_of_four_seater.text() == "":
            self.error_label.setText("Please Enter Four Wheeler Space")
            return

        data = {
            "username": self.input_db_username.text(),
            "database": self.input_db_name.text(),
            "password": self.input_db_password.text(),
        }
        file = open("./config.json", "w")
        file.write(json.dumps(data))
        file.close()

        dbOperation = DBOperation()
        dbOperation.createTables()
        dbOperation.insertAdmin(
            self.input_admin_username.text(),
            self.input_admin_password.text()
        )
        dbOperation.insertOneTimeData(
            int(self.input_no_of_two_seater.text()),
            int(self.input_no_of_four_seater.text())
        )

        self.close()
        self.login = LoginScreen()
        self.login.showLoginScreen()
        print("Save step")
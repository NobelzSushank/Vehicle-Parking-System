import sys
import os
from InstallWindow import InstallWindow
from LoginWindow import LoginScreen
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

class MainScreen():
    def showSplashScreen(self):
        print("Showing Splash screen")
        self.pix=QPixmap("python_vehicle.jpg")
        self.splash=QSplashScreen(self.pix, Qt.WindowStaysOnTopHint)
        self.splash.show()

def showSetupWindow():
    mainScreen.splash.close()
    installWindow.show()

def showLoginWindow():
    mainScreen.splash.close()
    login.showLoginScreen()


app = QApplication(sys.argv)
login = LoginScreen()
mainScreen = MainScreen()
mainScreen.showSplashScreen()
installWindow = InstallWindow()

if os.path.exists("./config.json"):
    QTimer.singleShot(3000, showLoginWindow)
else:
    QTimer.singleShot(3000, showSetupWindow)

sys.exit(app.exec())
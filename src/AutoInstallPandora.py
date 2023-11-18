import os.path
import sys
import subprocess
import shutil

from PySide2.QtCore import QStandardPaths
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel
from PySide2 import QtCore

#pandora facilities
from UserInterfacesPandora import qdarkstyle
from Pandora_Maya_Integration import Pandora_Maya_Integration
from PandoraSettings import PandoraSettings
from PandoraCore import PandoraCore

class PandoraInstallerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UIW Pandora Auto Installer 0.0.1")

        #Widgets
        self.maya_path_hint = QLabel("Maya Document Path should be C:\\Users\\your_user_name\\Documents\\maya\\maya_version")
        self.maya_path_label = QLabel("Maya Document Path: ")
        self.maya_path_field = QLineEdit()
        self.load_path_button = QPushButton("...")
        self.install_button = QPushButton("Install")

        #layout
        self.layout = QVBoxLayout(self)
        self.path_layout = QHBoxLayout(self)

        self.layout.addWidget(self.maya_path_hint)

        self.layout.addLayout(self.path_layout)
        self.path_layout.addWidget(self.maya_path_label)
        self.path_layout.addWidget(self.maya_path_field)
        self.path_layout.addWidget(self.load_path_button)

        self.layout.addWidget(self.install_button)


        #deault values:
        self.documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        self.maya_path = self.documents_path + "/maya/2024"
        self.maya_path_field.setText(self.maya_path)

        #functionality
        self.load_path_button.clicked.connect(self.pick_maya_path)
        self.install_button.clicked.connect(self.install)


        #style
        self.resize(600, 100)
        self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=True))



    def pick_maya_path(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog

        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            self.documents_path = directory
            self.maya_path_field.setText(directory)

    def install(self):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.abspath(exec_dir))
        pandora_installer_dir = os.path.join(project_dir, "vendor\\Pandora")
        os.chdir(pandora_installer_dir)
        pandora_installer_name = "Pandora_Setup.bat"
        pandora_installer_path = os.path.join(pandora_installer_dir, pandora_installer_name)


        dependency_dir = os.path.join(project_dir, "vendor\\PandoraDependency")
        dependency_names = ['Python37', 'PythonLibs']
        for dependency_name in dependency_names:
            dependency_path = os.path.join(dependency_dir, dependency_name)

            destination = os.path.join(pandora_installer_dir, "Pandora\\"+dependency_name)
            if not os.path.exists(destination):
                shutil.copytree(dependency_path, destination)


        #subprocess.run([pandora_installer_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(pandora_installer_dir)
        #init pandora core
        core = PandoraCore()
        self.installPandora(core)
        #setup maya integration
        core_working_dir = os.path.join(pandora_installer_dir, 'Pandora\\Scripts')
        os.chdir(core_working_dir)

        for i in core.unloadedAppPlugins:
            if i.pluginName == "Maya":
                i.writeMayaFiles(self.maya_path)

    #TODO: win32 load issue with quite install.
    def installPandora(self, core):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.abspath(exec_dir))
        installer_working_dir = os.path.join(project_dir, "vendor\\Pandora\\Pandora")
        os.chdir(installer_working_dir)

        from PandoraInstaller import PandoraInstaller
        installer = PandoraInstaller(core)
        installer.install()

if __name__ == "__main__":
    app = QApplication([])
    widget = PandoraInstallerWidget()
    widget.show()
    app.exec_()


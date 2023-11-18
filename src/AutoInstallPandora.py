#setup lib path
import os, shutil, sys, platform

if sys.version[0] == "3":
    pVersion = 3
    pyLibs = "Python37"
else:
    pVersion = 2
    pyLibs = "Python27"

root_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

script_path = os.path.abspath(os.path.dirname(__file__))
if script_path not in sys.path:
    sys.path.append(script_path)

sys.path.insert(0, os.path.join(root_path, "dependency\\PythonLibs", pyLibs))
sys.path.insert(0, os.path.join(root_path, "dependency\\PythonLibs", pyLibs, "win32"))
sys.path.insert(0, os.path.join(root_path, "dependency\\PythonLibs", pyLibs, "win32", "lib"))
sys.path.insert(0, os.path.join(root_path, "dependency\\PythonLibs", pyLibs, "PySide"))

sys.path.insert(0, os.path.join(root_path, "vendor\\Pandora\\Pandora\\Scripts", "UserInterfacesPandora"))
sys.path.insert(0, os.path.join(root_path, "vendor\\Pandora\\Pandora\\Scripts"))

os.environ['PATH'] = os.path.join(root_path, "dependency\\PythonLibs", pyLibs, "pywin32_system32") + os.pathsep + os.environ['PATH']

#importing modules
import os.path
import sys
import shutil

from PySide2.QtCore import QStandardPaths
from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel

#pandora facilities
from UserInterfacesPandora import qdarkstyle
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
    qApp = QApplication()
    qApp.setStyleSheet(qdarkstyle.load_stylesheet(pyside=True))

    widget = PandoraInstallerWidget()
    widget.show()

    sys.exit(qApp.exec_())

# setup lib path
import os
import shutil
import sys

def init_sys_path():
    py_libs = "Python37"
    vendor_dir_name = 'vendor'
    pandora_dir_name = 'Pandora'
    pandora_scrip_relative_dir = 'Pandora\\Scripts'

    working_dir = os.path.abspath(os.path.dirname(os.path.dirname('__file__')))

    src_dir = os.path.join(working_dir, "src")

    if src_dir not in sys.path:
        sys.path.append(src_dir)

    root_dir = os.path.abspath(os.path.dirname(src_dir))
    dependency_path = os.path.join(root_dir, vendor_dir_name, 'pythonEnv')
    pandora_script_dir = os.path.join(root_dir, vendor_dir_name, pandora_dir_name, pandora_scrip_relative_dir)


    #add lib paths
    sys.path.insert(0, pandora_script_dir)

    lib_dir = os.path.join(dependency_path, "PythonLibs", py_libs)
    sys.path.insert(0, lib_dir)

    win32_lib_root_dir = os.path.join(dependency_path, "PythonLibs", py_libs, "win32")
    sys.path.insert(0, win32_lib_root_dir)

    win32_lib_dir = os.path.join(dependency_path, "PythonLibs", py_libs, "win32", "lib")
    sys.path.insert(0, win32_lib_dir)

    pyside_lib_dir = os.path.join(dependency_path, "PythonLibs", py_libs, "PySide")
    sys.path.insert(0, pyside_lib_dir)

    pandora_interface_lib_dir = os.path.join(pandora_script_dir, "UserInterfacesPandora")
    sys.path.insert(0, pandora_interface_lib_dir)

    os.environ['PATH'] = os.path.join(dependency_path, "PythonLibs", py_libs, "pywin32_system32") + os.pathsep + os.environ['PATH']

    #log out path info:
    #sys.stdout = open('output.log', 'w')
    print(f"src_dir: {src_dir}")
    print(f"root_dir: {root_dir}")
    print(f"dependency_path: {dependency_path}")
    print(f"pandora_script_dir: {pandora_script_dir}")
    print(f"lib_dir: {lib_dir}")
    print(f"win32_lib_root_dir: {win32_lib_root_dir}")
    print(f"win32_lib_dir: {win32_lib_dir}")
    print(f"pyside_lib_dir: {pyside_lib_dir}")
    print(f"pandora_interface_lib_dir: {pandora_interface_lib_dir}")
    #sys.stdout.close()

#needed for python interactive interpreter to load modules properly.
init_sys_path()

#Pyside
from PySide2.QtCore import QStandardPaths
from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel

# pandora facilities
from UserInterfacesPandora import qdarkstyle
from PandoraCore import PandoraCore


class PandoraInstallerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UIW Pandora Auto Installer 0.0.1")

        # Widgets
        self.maya_path_hint = QLabel(
            "Maya Document Path should be C:\\Users\\your_user_name\\Documents\\maya\\maya_version")
        self.maya_path_label = QLabel("Maya Document Path: ")
        self.maya_path_field = QLineEdit()
        self.load_path_button = QPushButton("...")
        self.install_button = QPushButton("Install")

        # layout
        self.layout = QVBoxLayout(self)
        self.path_layout = QHBoxLayout(self)

        self.layout.addWidget(self.maya_path_hint)

        self.layout.addLayout(self.path_layout)
        self.path_layout.addWidget(self.maya_path_label)
        self.path_layout.addWidget(self.maya_path_field)
        self.path_layout.addWidget(self.load_path_button)

        self.layout.addWidget(self.install_button)

        # deault values:
        self.documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        self.maya_path = self.documents_path + "/maya/2024"
        self.maya_path_field.setText(self.maya_path)

        # functionality
        self.load_path_button.clicked.connect(self.pick_maya_path)
        self.install_button.clicked.connect(self.install)

        # style
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

        dependency_dir = os.path.join(project_dir, "vendor\\PythonEnv")
        dependency_names = ['Python37', 'PythonLibs']
        for dependency_name in dependency_names:
            dependency_path = os.path.join(dependency_dir, dependency_name)

            destination = os.path.join(pandora_installer_dir, "Pandora\\" + dependency_name)
            if not os.path.exists(destination):
                shutil.copytree(dependency_path, destination)

        # subprocess.run([pandora_installer_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.chdir(pandora_installer_dir)
        # init pandora core
        core = PandoraCore()
        self.installPandora(core)
        # setup maya integration
        core_working_dir = os.path.join(pandora_installer_dir, 'Pandora\\Scripts')
        os.chdir(core_working_dir)

        for i in core.unloadedAppPlugins:
            if i.pluginName == "Maya":
                i.writeMayaFiles(self.maya_path)

    # TODO: win32 load issue with quite install.
    def installPandora(self, core):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.abspath(exec_dir))
        installer_working_dir = os.path.join(project_dir, "vendor\\Pandora\\Pandora")
        os.chdir(installer_working_dir)

        from PandoraInstaller import PandoraInstaller
        installer = PandoraInstaller(core)
        installer.install()


qApp = QApplication()
qApp.setStyleSheet(qdarkstyle.load_stylesheet(pyside=True))

widget = PandoraInstallerWidget()
widget.show()

sys.exit(qApp.exec_())

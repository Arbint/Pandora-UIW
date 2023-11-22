# setup lib path
import json
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

    # add lib paths
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

    # log out path info:
    # sys.stdout = open('output.log', 'w')
    print(f"src_dir: {src_dir}")
    print(f"root_dir: {root_dir}")
    print(f"dependency_path: {dependency_path}")
    print(f"pandora_script_dir: {pandora_script_dir}")
    print(f"lib_dir: {lib_dir}")
    print(f"win32_lib_root_dir: {win32_lib_root_dir}")
    print(f"win32_lib_dir: {win32_lib_dir}")
    print(f"pyside_lib_dir: {pyside_lib_dir}")
    print(f"pandora_interface_lib_dir: {pandora_interface_lib_dir}")  # sys.stdout.close()


# needed for python interactive interpreter to load modules properly.
init_sys_path()

# Pyside
from PySide2.QtCore import QStandardPaths
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLineEdit, QLabel, QFrame

# pandora facilities
from UserInterfacesPandora import qdarkstyle
from PandoraCore import PandoraCore


class PandoraInstallerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UIW Pandora Auto Installer 0.0.1")

        # Widgets
        self.maya_path_hint = QLabel("Maya Document Path should be C:\\Users\\your_user_name\\Documents\\maya\\maya_version")
        self.maya_path_label = QLabel("Maya Document Path: ")
        self.maya_path_field = QLineEdit()
        self.load_path_button = QPushButton("...")

        self.net_path_hint = QLabel("Net Location should be a net location all render slaves can access (example: \\\\AD-406\\render_server\\)")
        self.net_path_label = QLabel("Net Location: ")
        self.net_path_field = QLineEdit()
        self.net_path_button = QPushButton("...")

        self.local_repo_path_hint = QLabel("Local repository need to be unique for every render slave(can be a net location, faster if local)")
        self.local_repo_path_label = QLabel("Local Repository: ")
        self.local_repo_path_field = QLineEdit()
        self.local_repo_path_button = QPushButton("...")

        self.install_button = QPushButton("Install")
        self.setup_slave_button = QPushButton("Start Slave")
        self.open_settings_button = QPushButton("Pandora Settings")
        # layout
        self.layout = QVBoxLayout(self)
        frame = QFrame(self)
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(frame)
        self.maya_path_layout = QHBoxLayout(self)

        self.layout.addWidget(self.maya_path_hint)

        self.layout.addLayout(self.maya_path_layout)
        self.maya_path_layout.addWidget(self.maya_path_label)
        self.maya_path_layout.addWidget(self.maya_path_field)
        self.maya_path_layout.addWidget(self.load_path_button)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(frame)
        self.layout.addWidget(self.net_path_hint)

        self.net_path_layout = QHBoxLayout(self)
        self.layout.addLayout(self.net_path_layout)
        self.net_path_layout.addWidget(self.net_path_label)
        self.net_path_layout.addWidget(self.net_path_field)
        self.net_path_layout.addWidget(self.net_path_button)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(frame)
        self.layout.addWidget(self.local_repo_path_hint)

        self.local_repo_path_layout = QHBoxLayout(self)
        self.layout.addLayout(self.local_repo_path_layout)
        self.local_repo_path_layout.addWidget(self.local_repo_path_label)
        self.local_repo_path_layout.addWidget(self.local_repo_path_field)
        self.local_repo_path_layout.addWidget(self.local_repo_path_button)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.HLine)
        frame.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(frame)
        self.layout.addWidget(self.install_button)
        self.layout.addWidget(self.setup_slave_button)
        self.layout.addWidget(self.open_settings_button)

        # deault values:
        self.documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        self.maya_path = self.documents_path + "/maya/2024"
        self.maya_path_field.setText(self.maya_path)

        # functionality
        self.load_path_button.clicked.connect(self.pick_maya_path)
        self.install_button.clicked.connect(self.install)
        self.net_path_button.clicked.connect(self.pick_net_path)
        self.local_repo_path_button.clicked.connect(self.pick_local_repo_path)
        self.setup_slave_button.clicked.connect(self.toggle_slave)
        self.open_settings_button.clicked.connect(self.open_pandora_settings)

        # style
        self.resize(600, 100)
        self.setStyleSheet(qdarkstyle.load_stylesheet(pyside=True))

        self.config_file_name = "config.json"
        self.load_config()

    def load_config(self):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(exec_dir, self.config_file_name)

        with open(config_file_path, "r") as config_file:
            config_data = json.load(config_file)
            self.local_repo_path_field.setText(config_data["localRepository"])
            self.net_path_field.setText(config_data["netLocation"])

    def save_settings(self):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        config_file_path = os.path.join(exec_dir, self.config_file_name)
        config = {
            "netLocation": self.net_path_field.text(),
            "localRepository": self.local_repo_path_field.text()
        }
        config_json = json.dumps(config, indent=4)

        with open(config_file_path, "w") as config_file:
            config_file.write(config_json)

    def pick_local_repo_path(self):
        self.pick_path_for_field(self.local_repo_path_field)

    def pick_net_path(self):
        self.pick_path_for_field(self.net_path_field)

    def toggle_slave(self):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.abspath(exec_dir))
        pandora_slave_path = os.path.join(project_dir, "vendor\\Pandora\\Pandora\\Python37\\Pandora Slave.exe")
        pandora_slave_file_path = os.path.join(project_dir, "vendor\\Pandora\\Pandora\\Scripts\\PandoraSlave.py")

        import subprocess
        subprocess.Popen([pandora_slave_path, pandora_slave_file_path])

    def open_pandora_settings(self):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.abspath(exec_dir))
        pandora_settings_path = os.path.join(project_dir, "vendor\\Pandora\\Pandora\\Python37\\Pandora Settings.exe")
        pandora_settings_file_path = os.path.join(project_dir, "vendor\\Pandora\\Pandora\\Scripts\\PandoraSettings.py")

        import subprocess
        subprocess.Popen([pandora_settings_path, pandora_settings_file_path])

    def pick_maya_path(self):
        self.documents_path = self.pick_path_for_field(self.maya_path_field)

    def pick_path_for_field(self, field: QLineEdit):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog

        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            field.setText(directory)
            return directory

        return ""

    def install(self):
        exec_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(os.path.abspath(exec_dir))
        pandora_installer_dir = os.path.join(project_dir, "vendor\\Pandora")

        dependency_dir = os.path.join(project_dir, "vendor\\PythonEnv")
        dependency_names = ['Python37', 'PythonLibs']
        for dependency_name in dependency_names:
            dependency_path = os.path.join(dependency_dir, dependency_name)

            destination = os.path.join(pandora_installer_dir, "Pandora\\" + dependency_name)
            if not os.path.exists(destination):
                shutil.copytree(dependency_path, destination)

        os.chdir(pandora_installer_dir)
        # init pandora core
        core = PandoraCore()
        self.installPandora(core)
        # setup maya integration
        self.setupMayaPlugins(core)
        self.setupLocalPath(core)
        self.setupRootPath(core)
        self.save_settings()
    def setupLocalPath(self, core: PandoraCore):
        configureData = []

        repPath = self.local_repo_path_field.text().replace("/", "\\")
        if repPath != "" and not repPath.endswith("\\"):
            repPath += "\\"
        configureData.append(["globals", "repositoryPath", repPath])
        core.setConfig(data=configureData)

    def setupRootPath(self, core: PandoraCore):
        configureData = []

        rootPath = self.net_path_field.text().replace("/", "\\")
        if rootPath != "" and not rootPath.endswith("\\"):
            rootPath += "\\"
        configureData.append(["globals", "rootPath", rootPath])
        core.setConfig(data=configureData)

    def setupMayaPlugins(self, core: PandoraCore):
        for i in core.unloadedAppPlugins:
            if i.pluginName == "Maya":
                i.writeMayaFiles(self.maya_path)

    def installPandora(self, core):
        # exec_dir = os.path.dirname(os.path.abspath(__file__))
        # project_dir = os.path.dirname(os.path.abspath(exec_dir))
        # installer_working_dir = os.path.join(project_dir, "vendor\\Pandora\\Pandora")
        # os.chdir(installer_working_dir)

        from PandoraInstaller import PandoraInstaller
        installer = PandoraInstaller(core)
        installer.install()


qApp = QApplication()
qApp.setStyleSheet(qdarkstyle.load_stylesheet(pyside=True))

#icon setup
exec_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.abspath(exec_dir))
icon_path =project_dir + "\\assets\\icon.ico"
handlerIcon = QIcon(icon_path)
qApp.setWindowIcon(handlerIcon)

widget = PandoraInstallerWidget()
widget.show()

sys.exit(qApp.exec_())
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PandoraSlaveAssignment.ui'
#
# Created: Fri Jun 08 15:38:10 2018
#      by: pyside2-uic @pyside_tools_VERSION@ running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets


class Ui_dlg_SlaveAssignment(object):
    def setupUi(self, dlg_SlaveAssignment):
        dlg_SlaveAssignment.setObjectName("dlg_SlaveAssignment")
        dlg_SlaveAssignment.resize(375, 382)
        self.gridLayout = QtWidgets.QGridLayout(dlg_SlaveAssignment)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_2 = QtWidgets.QWidget(dlg_SlaveAssignment)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rb_all = QtWidgets.QRadioButton(self.widget_2)
        self.rb_all.setChecked(True)
        self.rb_all.setObjectName("rb_all")
        self.verticalLayout_2.addWidget(self.rb_all)
        self.rb_group = QtWidgets.QRadioButton(self.widget_2)
        self.rb_group.setObjectName("rb_group")
        self.verticalLayout_2.addWidget(self.rb_group)
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.w_slaveGroups = QtWidgets.QWidget(self.widget_3)
        self.w_slaveGroups.setObjectName("w_slaveGroups")
        self.horizontalLayout.addWidget(self.w_slaveGroups)
        self.verticalLayout_2.addWidget(self.widget_3)
        self.rb_custom = QtWidgets.QRadioButton(self.widget_2)
        self.rb_custom.setObjectName("rb_custom")
        self.verticalLayout_2.addWidget(self.rb_custom)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_2.addItem(spacerItem1)
        self.gridLayout.addWidget(self.widget_2, 0, 0, 2, 1)
        self.widget = QtWidgets.QWidget(dlg_SlaveAssignment)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rb_include = QtWidgets.QRadioButton(self.widget_4)
        self.rb_include.setChecked(True)
        self.rb_include.setObjectName("rb_include")
        self.horizontalLayout_2.addWidget(self.rb_include)
        self.rb_exclude = QtWidgets.QRadioButton(self.widget_4)
        self.rb_exclude.setObjectName("rb_exclude")
        self.horizontalLayout_2.addWidget(self.rb_exclude)
        self.verticalLayout.addWidget(self.widget_4)
        self.lw_slaves = QtWidgets.QListWidget(self.widget)
        self.lw_slaves.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lw_slaves.setObjectName("lw_slaves")
        self.verticalLayout.addWidget(self.lw_slaves)
        self.gridLayout.addWidget(self.widget, 0, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(dlg_SlaveAssignment)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 2, 1, 1)

        self.retranslateUi(dlg_SlaveAssignment)
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("accepted()"), dlg_SlaveAssignment.accept
        )
        QtCore.QObject.connect(
            self.buttonBox, QtCore.SIGNAL("rejected()"), dlg_SlaveAssignment.reject
        )
        QtCore.QMetaObject.connectSlotsByName(dlg_SlaveAssignment)

    def retranslateUi(self, dlg_SlaveAssignment):
        dlg_SlaveAssignment.setWindowTitle(
            QtWidgets.QApplication.translate(
                "dlg_SlaveAssignment", "Slave assigment", None, -1
            )
        )
        self.rb_all.setText(
            QtWidgets.QApplication.translate("dlg_SlaveAssignment", "All", None, -1)
        )
        self.rb_group.setText(
            QtWidgets.QApplication.translate("dlg_SlaveAssignment", "By group", None, -1)
        )
        self.rb_custom.setText(
            QtWidgets.QApplication.translate("dlg_SlaveAssignment", "Custom", None, -1)
        )
        self.rb_include.setText(
            QtWidgets.QApplication.translate("dlg_SlaveAssignment", "Include", None, -1)
        )
        self.rb_exclude.setText(
            QtWidgets.QApplication.translate("dlg_SlaveAssignment", "Exclude", None, -1)
        )

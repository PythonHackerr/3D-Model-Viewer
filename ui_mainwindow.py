# -*- coding: utf-8 -*-

##############################################################################
# Form generated from reading UI file 'GKOM1.ui'
##
# Created by: Qt User Interface Compiler version 6.6.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
##############################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject,
                            QRect, QSize, QTimer)
from PySide6.QtGui import (QAction)
from PySide6.QtWidgets import (QCheckBox, QGridLayout, QHBoxLayout,
                               QLabel, QListView, QMainWindow, QMenu,
                               QMenuBar, QPushButton, QSizePolicy, QSpacerItem,
                               QStatusBar, QWidget, QSpinBox, QVBoxLayout)
from engine import QGLControllerWidget
import loader


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.checkboxes = []
        self.scene_objects = []
        self.scene_objects_data = []
        timer = QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.openGLWidget.update)
        timer.start()

    def load_file(self, scene=None) -> None:
        """
        Load object from file
        """
        if isinstance(scene, str):
            self.scene_objects = loader.open_file(scene)
        else:
            self.scene_objects = loader.open_file_ask()
        self.scene_objects_data = [o["data"] for o in self.scene_objects]
        self.update_checkboxes()
        loader.load_mesh(self.scene_objects_data, self.openGLWidget)
        self.updateStatusBar()

    def updateStatusBar(self) -> None:
        """
        Update model data shown in labels.
        """
        vertices = self.openGLWidget.getVerticesNumber()
        faces = self.openGLWidget.getFacesNumber()
        edges = self.openGLWidget.getEdgesNumber()
        uv = self.openGLWidget.getUVCoordinatesNumber()
        self.modelDataLabel.setText("Vertices: %i\nFaces: %i\nEdges: %i\nUV coordinates: %i"
                                    % (vertices, faces, edges, uv))

    def update_checkboxes(self) -> None:
        """
        Remove existing checkboxes and set new ones.
        """
        for c in self.checkboxes:
            c.setParent(None)
        self.checkboxes = []
        for i, o in enumerate(self.scene_objects):
            self.checkboxes.append(QCheckBox(self.objectHierarchyWidget))
            self.checkboxes[-1].setObjectName(o["name"])
            self.checkboxes[-1].setText(
                QCoreApplication.translate("MainWindow", o["name"], None))
            self.checkboxes[-1].setChecked(True)
            self.checkboxes[-1].stateChanged.connect(self.update_scene)
            self.gridLayout_2.addWidget(self.checkboxes[-1], i, 1, 1, 1)
        self.gridLayout_2.addItem(self.verticalSpacer, i+1, 1, 1, 1)

    def update_camera(self) -> None:
        """
        Update camera position to coordinates set in spinboxes.
        """
        position = [
            self.CameraXPos.value(),
            self.CameraYPos.value(),
            self.CameraZPos.value()
        ]

        self.openGLWidget.setCamera(position)

    def update_scene(self) -> None:
        """
        Reload object into openGL widget. Shows only models chosen in checkboxes.
        """
        self.scene_objects_data = []
        for o in zip(self.scene_objects, self.checkboxes):
            if o[1].isChecked():
                self.scene_objects_data.append(o[0]["data"])
        loader.load_mesh(self.scene_objects_data, self.openGLWidget)
        self.updateStatusBar()

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(998, 703)
        self.actionOpen_file = QAction(MainWindow)
        self.actionOpen_file.setObjectName(u"actionOpen_file")
        self.actionOpen_file.triggered.connect(self.load_file)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.objectHierarchyWidget = QWidget(self.centralwidget)
        self.objectHierarchyWidget.setObjectName(u"objectHierarchyWidget")
        self.gridLayout_2 = QGridLayout(self.objectHierarchyWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontalLayout_4.addWidget(self.objectHierarchyWidget)

        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.openGLWidget = QGLControllerWidget(self.widget)
        self.openGLWidget.setGeometry(100, 30, 700, 500)

        self.verticalLayout.addWidget(self.openGLWidget)

        self.cameraCoordsWidget = QWidget(self.widget)
        self.cameraCoordsWidget.setObjectName(u"cameraCoordsWidget")
        self.gridLayout_5 = QGridLayout(self.cameraCoordsWidget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.CameraXPos = QSpinBox(self.cameraCoordsWidget)
        self.CameraXPos.setObjectName(u"CameraXPos")
        self.CameraXPos.setMinimum(-999999)
        self.CameraXPos.setMaximum(999999)
        self.CameraXPos.valueChanged.connect(self.update_camera)

        self.gridLayout_5.addWidget(self.CameraXPos, 2, 0, 1, 1)

        self.CameraYPos = QSpinBox(self.cameraCoordsWidget)
        self.CameraYPos.setObjectName(u"CameraYPos")
        self.CameraYPos.setMinimum(-999999)
        self.CameraYPos.setMaximum(999999)
        self.CameraYPos.valueChanged.connect(self.update_camera)

        self.gridLayout_5.addWidget(self.CameraYPos, 2, 1, 1, 1)

        self.CameraZPos = QSpinBox(self.cameraCoordsWidget)
        self.CameraZPos.setObjectName(u"CameraZPos")
        self.CameraZPos.setMinimum(-999999)
        self.CameraZPos.setMaximum(999999)
        self.CameraZPos.valueChanged.connect(self.update_camera)

        self.gridLayout_5.addWidget(self.CameraZPos, 2, 2, 1, 1)

        self.cameraYlabel = QLabel(self.cameraCoordsWidget)
        self.cameraYlabel.setObjectName(u"cameraYlabel")

        self.gridLayout_5.addWidget(self.cameraYlabel, 0, 1, 1, 1)

        self.cameraZlabel = QLabel(self.cameraCoordsWidget)
        self.cameraZlabel.setObjectName(u"cameraZlabel")

        self.gridLayout_5.addWidget(self.cameraZlabel, 0, 2, 1, 1)

        self.cameraXlabel = QLabel(self.cameraCoordsWidget)
        self.cameraXlabel.setObjectName(u"cameraXlabel")

        self.gridLayout_5.addWidget(self.cameraXlabel, 0, 0, 1, 1)

        self.cameraLRlaber = QLabel(self.cameraCoordsWidget)
        self.cameraLRlaber.setObjectName(u"cameraLRlaber")

        self.gridLayout_5.addWidget(self.cameraLRlaber, 0, 3, 1, 1)

        self.verticalLayout.addWidget(self.cameraCoordsWidget)

        self.verticalLayout.setStretch(0, 6)

        self.horizontalLayout_4.addWidget(self.widget)

        self.toolsWidget = QWidget(self.centralwidget)
        self.toolsWidget.setObjectName(u"toolsWidget")
        self.toolsWidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_4 = QGridLayout(self.toolsWidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.lightsWidget = QWidget(self.toolsWidget)
        self.lightsWidget.setObjectName(u"lightsWidget")
        self.lightsWidget.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_3 = QGridLayout(self.lightsWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lightsListView = QListView(self.lightsWidget)
        self.lightsListView.setObjectName(u"lightsListView")

        self.gridLayout_3.addWidget(self.lightsListView, 2, 0, 1, 1)

        self.addNewLight = QPushButton(self.lightsWidget)
        self.addNewLight.setObjectName(u"addNewLight")

        self.gridLayout_3.addWidget(self.addNewLight, 1, 0, 1, 1)

        self.titleLabel = QLabel(self.lightsWidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.gridLayout_3.addWidget(self.titleLabel, 0, 0, 1, 1)

        self.editLightWidget = QWidget(self.lightsWidget)
        self.editLightWidget.setObjectName(u"editLightWidget")

        self.gridLayout_3.addWidget(self.editLightWidget, 3, 0, 1, 1)

        self.gridLayout_4.addWidget(self.lightsWidget, 2, 0, 1, 1)

        self.materialLabel = QLabel(self.toolsWidget)
        self.materialLabel.setObjectName(u"materialLabel")

        self.gridLayout_4.addWidget(self.materialLabel, 1, 0, 1, 1)

        self.modelDataLabel = QLabel(self.toolsWidget)
        self.modelDataLabel.setObjectName(u"modelDataLabel")

        self.gridLayout_4.addWidget(self.modelDataLabel, 3, 0, 1, 1)

        self.vectorsCheckBox = QPushButton(self.toolsWidget)
        self.vectorsCheckBox.setObjectName(u"vectorsCheckBox")
        self.vectorsCheckBox.clicked.connect(self.openGLWidget.showVectors)

        self.gridLayout_4.addWidget(self.vectorsCheckBox, 4, 0, 1, 1)

        self.wireframeCheckBox = QCheckBox(self.toolsWidget)
        self.wireframeCheckBox.setObjectName(u"wireframeCheckBox")
        self.wireframeCheckBox.stateChanged.connect(self.openGLWidget.set_showWireFrame)

        self.gridLayout_4.addWidget(self.wireframeCheckBox, 5, 0, 1, 1)

        self.wireframeCheckBox1 = QCheckBox(self.toolsWidget)
        self.wireframeCheckBox1.setObjectName(u"wireframeCheckBox1")
        self.wireframeCheckBox1.stateChanged.connect(self.openGLWidget.set_ambient)

        self.gridLayout_4.addWidget(self.wireframeCheckBox1, 6, 0, 1, 1)

        self.horizontalLayout_4.addWidget(self.toolsWidget)

        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 4)
        self.horizontalLayout_4.setStretch(2, 1)

        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.statusBarLabel = QLabel("")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 998, 21))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.addWidget(self.statusBarLabel)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionOpen_file)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen_file.setText(QCoreApplication.translate("MainWindow", u"Open file", None))
        self.cameraYlabel.setText(QCoreApplication.translate("MainWindow", u"Camera Y", None))
        self.cameraZlabel.setText(QCoreApplication.translate("MainWindow", u"Camera Z", None))
        self.cameraXlabel.setText(QCoreApplication.translate("MainWindow", u"Camera X", None))
        self.addNewLight.setText(QCoreApplication.translate("MainWindow", u"Add new", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Lights", None))
        self.vectorsCheckBox.setText(QCoreApplication.translate("MainWindow", u"Show vectors", None))
        self.wireframeCheckBox.setText(QCoreApplication.translate("MainWindow", u"Show wireframe", None))
        self.wireframeCheckBox1.setText(QCoreApplication.translate("MainWindow", u"Light", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
    # retranslateUi

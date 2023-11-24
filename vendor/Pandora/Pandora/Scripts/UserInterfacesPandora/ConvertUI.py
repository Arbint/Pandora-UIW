import sys, pprint


fname = "RenderHandler"
fname = "PandoraSettings"
fname = "PandoraSubmitter"
# fname = "PandoraSlaveAssignment"
# fname = "PandoraInstaller"


pyside = 0

if pyside in [0, 1]:
    from pysideuic import compileUi

    pyfile = open(fname + "_ui.py", "w")
    compileUi(fname + ".ui", pyfile, False, 4, False)

if pyside in [0, 2]:
    from pyside2uic import compileUi as compileUi2

    pyfile = open(fname + "_ui_ps2.py", "w")
    compileUi2(fname + ".ui", pyfile, False, 4, False)

pyfile.close()

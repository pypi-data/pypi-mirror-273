from pathlib import Path
from magicgui import widgets
from ...gui.gui_components import (
    check_file_availability,
)


def show_io_win(dtype="APS_tomo"):
    if dtype == "APS_tomo":
        vals = widgets.request_values(
            name={
                "annotation": Path,
                "label": "pick a tomo file",
                "options": {"mode": "r", "filter": "tomo data file (*.h5)"},
            },
            title="pick a tomo file from 3D XANES data series",
        )
        return vals


def mk_aps_cfg(fn_tplt, cfg, dtype="APS 3D XANES"):
    if dtype == "APS 3D XANES":
        tem = (
            cfg["io_data_structure_tomo"]["tomo_raw_fn_template"]
            .replace("{0}", fn_tplt)
            .replace("{1}", "{0}")
        )
        cfg["io_data_structure_tomo"]["tomo_raw_fn_template"] = tem
        cfg["io_data_structure_xanes3D"]["tomo_raw_fn_template"] = tem
        cfg["io_data_structure_xanes3D"]["xanes3D_recon_dir_template"] = "recon_" + str(
            Path(tem).stem
        )
        cfg["io_data_structure_xanes3D"]["xanes3D_recon_fn_template"] = (
            "recon_" + str(Path(tem).stem) + "_{1}.tiff"
        )
    elif dtype == "APS 2D XANES":
        # APS 2D XANES data files are saved in the same manner as APS 3D XANES; the naming schemes
        # in both 2D XANES and 3D XANES are same
        tem = (
            cfg["io_data_structure_xanes2D"]["xanes2D_raw_fn_template"]
            .replace("{0}", fn_tplt)
            .replace("{1}", "{0}")
        )
        cfg["io_data_structure_xanes2D"]["xanes2D_raw_fn_template"] = tem
    return cfg


# from magicgui.widgets import request_values

# vals = request_values(
#     age=int,
#     name={"annotation": str, "label": "Enter your name:"},
#     title="Hi, who are you?",
# )
# print(repr(vals))


# from magicgui import widgets


# class extra_io_win(widgets.MainWindow):
#     def __init__(self, parent, dtype):
#         super().__init__()
#         self.parent_obj = parent
#         self.dtype = dtype

#         label = widgets.Label(value="extra data info")
#         self.sel_file = widgets.FileEdit(
#             mode="r",
#             filter="dxchange tomo file (*.h5)",
#             name="xanes file",
#         )
#         self.close = widgets.PushButton(text="confirm")
#         self.sel_file.changed.connect(self._sel_file)
#         self.close.changed.connect(self._close)

#         self.widgets = [label, self.sel_file, self.close]
#         self.show(run=True)

#     def _sel_file(self):
#         pass
#         # app = QtWidgets.QApplication([])
#         # file_dialog = QtWidgets.QFileDialog(
#         #     caption="pick a tomo file",
#         #     directory=self.parent._io_win_dir,
#         #     filter="APS tomo data file (*.h5)",
#         # )
#         # if file_dialog.exec_():
#         #     self.parent.selected_file = file_dialog.selectedFiles()[0]
#         #     print(f"Selected file: {self.parent.selected_file}")
#         # app.exec_()

#     def _close(self):
#         self.close()


# import sys
# from PyQt5.QtWidgets import (
#     QApplication,
#     QWidget,
#     QVBoxLayout,
#     QHBoxLayout,
#     QMainWindow,
#     QLabel,
#     QLineEdit,
#     QFileDialog,
#     QPushButton,
# )


# class extra_io_win(QMainWindow):
#     def __init__(self, parent, dtype):
#         super().__init__()
#         self.parent_obj = parent
#         self.dtype = dtype

#         # app = QApplication(sys.argv)
#         self.setWindowTitle("extra data info")

#         central_widget = QWidget()

#         layout = QVBoxLayout()
#         label = QLabel(text="pick a tomo file")

#         self.file_dialog = QWidget()
#         fd_layout = QHBoxLayout()
#         self.path = QLineEdit("")
#         self.open_butt = QPushButton(text="pick a tomo file")
#         fd_layout.addWidget(self.path)
#         fd_layout.addWidget(self.open_butt)
#         self.file_dialog.setLayout(fd_layout)

#         # self.sel_file = QFileDialog(
#         #     caption="pick a tomo file",
#         #     directory=self.parent_obj._io_win_dir,
#         #     filter="dxchange tomo file (*.h5)",
#         # )
#         self.close_butt = QPushButton(text="confirm")
#         layout.addWidget(label)
#         layout.addWidget(self.file_dialog)
#         layout.addWidget(self.close_butt)

#         central_widget.setLayout(layout)

#         self.setCentralWidget(central_widget)

#         self.open_butt.clicked.connect(self._sel_file)
#         self.close_butt.clicked.connect(self._close)

#         self.show()
#         # sys.exit(app.exec_())

#     def _sel_file(self):
#         pass
#         # app = QtWidgets.QApplication([])
#         # file_dialog = QtWidgets.QFileDialog(
#         #     caption="pick a tomo file",
#         #     directory=self.parent._io_win_dir,
#         #     filter="APS tomo data file (*.h5)",
#         # )
#         # if file_dialog.exec_():
#         #     self.parent.selected_file = file_dialog.selectedFiles()[0]
#         #     print(f"Selected file: {self.parent.selected_file}")
#         # app.exec_()

#     def _close(self):
#         self.close()

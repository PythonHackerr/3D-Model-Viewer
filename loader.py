from PySide6 import QtWidgets
import trimesh


def open_file_ask() -> list[dict[str]]:
    file_name = QtWidgets.QFileDialog.getOpenFileName(
        None,
        'Open file',
        '',
        "Mesh files (*.obj *.stl *.ply *.off *.om)")
    if not file_name[0]:
        return
    return open_file(file_name[0])


def open_file(file_name) -> list[dict[str]]:
    return get_data(file_name)


def load_mesh(obj_list: list[dict[str]], opengl_obj: object) -> None:
    """
    Load data from list of objects and setup on openGL widget.
    """
    l_list = []
    for i in obj_list:
        mesh = trimesh.load(file_obj=trimesh.util.wrap_as_stream(i),
                            file_type='obj')
        l_list.append(trimesh.load(mesh))
    opengl_obj.set_mesh(l_list)


def get_data(fname: str) -> list[dict[str]]:
    """
    Read data from .obj file and separate objects.
    """
    obj_list = []
    counter = 0
    subtractor = 0
    curr_obj_name = ""
    with open(fname, 'r') as f:
        line = f.readline()
        s = ""
        while line:
            if line[0] == "#":
                line = f.readline()
                continue
            fline = line.split(" ")
            if fline[0] == "o":
                if s != "":
                    obj_list.append({"name": curr_obj_name, "data": s})
                    s = ""
                    subtractor = counter
                curr_obj_name = fline[1]
            elif fline[0] == "f":
                s += "f "
                for face in fline[1:]:
                    vs = face.split("/")
                    for _, v in enumerate(vs):
                        s += str(int(v) - subtractor)
                        if _ != len(vs) - 1:
                            s += "/"
                        else:
                            s += " "
                s += "\n"
            else:
                if fline[0] == "v":
                    counter += 1
                s += line
            line = f.readline()
        obj_list.append({"name": curr_obj_name, "data": s})
    return obj_list

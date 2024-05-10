from PySide6.QtGui import QImage
from PySide6.QtOpenGLWidgets import QOpenGLWidget
import OpenGL.GL as gl
import numpy as np
from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram
import shaders
import trimesh
import math
DIFFUSE_TEXTURE_PATH = "assets/textures/wood2.jpg"
SPECULAR_TEXTURE_PATH = "assets/textures/wood.jpg"


def load_texture(image: QImage) -> None:
    if image.isNull():
        print("Error: Image not loaded successfully")
        return

    image = image.convertToFormat(QImage.Format_RGBA8888)
    image_data = image.bits().tobytes()

    gl.glEnable(gl.GL_TEXTURE_2D)
    texture_obj = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture_obj)
    gl.glTexImage2D(
        gl.GL_TEXTURE_2D,
        0,
        gl.GL_RGBA,
        image.width(),
        image.height(),
        0,
        gl.GL_RGBA,
        gl.GL_UNSIGNED_BYTE,
        image_data
    )

    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                       gl.GL_NEAREST)
    gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                       gl.GL_NEAREST)

    return texture_obj


class QGLControllerWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(QGLControllerWidget, self).__init__(parent)
        self.shader = None
        self.indices = None
        self.vertices = None
        self.mesh = None
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.diffuse_texture_obj = None
        self.specular_texture_obj = None
        self.wireframeMode = False
        self.ambient = False
        self.uniqueVerticesNumber = 0
        self.facesNumber = 0
        self.edgesNumber = 0
        self.uvCoordinatesNumber = 0
        self.cameraPosition = [0.1, 0.1, 0]

        self.light_direction = [1.0, 1.0, 1.0]
        self.light_color = [1.0, 1.0, 1.0]
        self.ambient_strength = 0.0

    def set_ambient(self, state) -> None:
        self.ambient = (state == 2)
        self.update()

    def initializeGL(self) -> None:
        gl.glClearColor(0, 0, 0, 1)
        gl.glEnable(gl.GL_DEPTH_TEST)

        self.initShaders()
        self.load_textures()

    def initShaders(self) -> None:
        # Initialize shaders for rendering
        self.shader = QOpenGLShaderProgram()
        self.shader.addShaderFromSourceCode(
            QOpenGLShader.Vertex, shaders.vertex_shader)
        self.shader.addShaderFromSourceCode(
            QOpenGLShader.Fragment, shaders.fragment_shader)
        self.shader.link()

    def load_textures(self) -> None:
        diffuse_image = QImage(DIFFUSE_TEXTURE_PATH)
        self.diffuse_texture_obj = load_texture(diffuse_image)

        specular_image = QImage(SPECULAR_TEXTURE_PATH)
        self.specular_texture_obj = load_texture(specular_image)

    def set_mesh(self, mesh_list: list[trimesh.Trimesh]) -> None:
        # Merge list of all models in scene
        if len(mesh_list) > 0:
            merged__meshes = trimesh.util.concatenate(mesh_list)
        else:
            merged__meshes = trimesh.Trimesh()

        self.mesh = merged__meshes.copy()
        self.originalMesh = merged__meshes.copy()
        self.setCamera()
        self.initObject(self.mesh)
        self.update()

        merged__meshes.merge_vertices(merge_tex=True, merge_norm=True)
        self.uniqueVerticesNumber = len(merged__meshes.vertices)
        self.facesNumber = len(merged__meshes.faces)
        self.edgesNumber = len(merged__meshes.edges)
        if hasattr(merged__meshes.visual, "uv"):
            self.uvCoordinatesNumber = len(merged__meshes.visual.uv)
        else:
            self.uvCoordinatesNumber = 0

    def initObject(self, mesh: trimesh.Trimesh) -> None:
        # Extract vertices and faces (indices) from the mesh
        self.vertices = np.array(
            mesh.vertices, dtype=np.float32)
        self.indices = np.array(
            mesh.faces.flatten(), dtype=np.uint32)

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        # Vertex buffer
        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, gl.GL_STATIC_DRAW)

        # Element buffer
        self.ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, gl.GL_STATIC_DRAW)

        # Position attribute
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * gl.sizeof(gl.GLfloat), gl.ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        # Texture coordinate attribute
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 2 * gl.sizeof(gl.GLfloat), gl.ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def setupMeshBuffers(self) -> None:
        if self.mesh is None:
            return

        vertices = np.array(self.mesh.vertices, dtype=np.float32)
        faces = np.array(self.mesh.faces, dtype=np.uint32).flatten()

        self.vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(self.vao)

        self.vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes,
                        vertices, gl.GL_STATIC_DRAW)

        self.ebo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, faces.nbytes,
                        faces, gl.GL_STATIC_DRAW)

        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE,
                                 3 * gl.sizeof(gl.GLfloat),
                                 gl.ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(0)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def resizeGL(self, width: int, height: int) -> None:
        gl.glViewport(0, 0, width, height)

    def paintGL(self) -> None:
        if self.mesh is None:
            return

        if self.wireframeMode:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        else:
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        self.ambient_strength = 0.7 if self.ambient else 0.0

        self.initObject(self.mesh)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        self.shader.bind()

        gl.glUniform3fv(gl.glGetUniformLocation(self.shader.programId(), "light_direction"), 1, self.light_direction)
        gl.glUniform3fv(gl.glGetUniformLocation(self.shader.programId(), "light_color"), 1, self.light_color)
        gl.glUniform3fv(gl.glGetUniformLocation(self.shader.programId(), "ambient_strength"), 1, self.ambient_strength)

        gl.glUniform1i(gl.glGetUniformLocation(self.shader.programId(), "diffuseTexture"), 0)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.diffuse_texture_obj)

        gl.glUniform1i(gl.glGetUniformLocation(self.shader.programId(), "specularTexture"), 1)
        gl.glActiveTexture(gl.GL_TEXTURE1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.specular_texture_obj)

        gl.glBindVertexArray(self.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, len(self.indices), gl.GL_UNSIGNED_INT, None)
        gl.glBindVertexArray(0)

        self.shader.release()

    def set_showWireFrame(self, state) -> None:
        self.wireframeMode = (state == 2)
        self.update()

    def setCamera(self, position=None):
        if position is not None:
            self.cameraPosition = position
            self.cameraPosition[0] /= 100
            self.cameraPosition[1] /= 100
            self.cameraPosition[2] /= 100

        if self.mesh is None or self.originalMesh is None:
            return

        self.mesh = self.originalMesh.copy()

        proximity = 1 + math.sqrt(self.cameraPosition[0] ** 2 + self.cameraPosition[1] ** 2 + self.cameraPosition[2] ** 2)

        try:
            xangle = -math.asin(self.cameraPosition[1] / proximity)
        except ZeroDivisionError:
            xangle = 0

        try:
            yangle = math.asin(self.cameraPosition[0] / math.sqrt(self.cameraPosition[0] ** 2 + self.cameraPosition[2] ** 2)) # self.cameraPosition[2])
        except:

            yangle = 0

        # rotate
        self.mesh.apply_transform([
            [math.cos(yangle), 0, math.sin(yangle), 0],
            [0, 1, 0, 0],
            [-math.sin(yangle), 0, math.cos(yangle), 0],
            [0, 0, 0, 1]])
        self.mesh.apply_transform([
            [1, 0, 0, 0],
            [0, math.cos(xangle), -math.sin(xangle), 0],
            [0, math.sin(xangle), math.cos(xangle), 0],
            [0, 0, 0, 1]])

        # move and resize
        self.mesh.apply_transform([
            [1/proximity, 0, 0, 0],
            [0, 1/proximity, 0, 0],
            [0, 0, 1/proximity, 0],
            [0, 0, 0, 1]])

    def showVectors(self) -> None:
        if self.mesh is None:
            return
        vec = np.column_stack((self.mesh.triangles_center, self.mesh.triangles_center + (self.mesh.face_normals * self.mesh.scale * .05)))
        path = trimesh.load_path(vec.reshape((-1, 2, 3)))
        trimesh.Scene([self.mesh, path]).show(smooth=False)

    def getVerticesNumber(self) -> int:
        return self.uniqueVerticesNumber

    def getFacesNumber(self) -> int:
        return self.facesNumber

    def getEdgesNumber(self) -> int:
        return self.edgesNumber

    def getUVCoordinatesNumber(self) -> int:
        return self.uvCoordinatesNumber

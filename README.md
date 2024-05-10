# 3D Model Viewer

### Installing libraries
`pip3 install -r requirements.txt`

### Starting the program
`python3 main.py`

### Reading the model
Go to Menu > Open file and select the appropriate file from the directory. Example models can be found in assets/models/

## About 3D Model Viewer

As part of the project, a program should be created that will enable viewing 3D models and their properties. For this purpose, you need to implement: 
1. support for various types of input files with the 3D model: obj, alembic 
2. Phong shading 
3. interpretation of material properties: diffuse, specular 
4. support for diffuse, specular textures
5. support for point lights - ability to add new ones, edit light properties
6. possibility of displaying data about the model: (a) number of vertices, faces, edges, uv coordinates (b) visualization of normal vectors (c) visualization of the model in the form of a wireframe All properties should be displayed in the same OK no.
7. ability to see individual parts of the object, i.e. if the object consists of several models, we can see its hierarchy and show/hide part of this hierarchy.
8. perspective camera - ability to move around the stage and rotate
9. model validation - the lack of specific properties, e.g. UV coordinates, should result in an error

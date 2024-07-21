# import numpy
from stl import mesh
# from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
from matplotlib import pyplot
# from stl.mesh import Mesh

class RenderObject:
    def __init__(self):
        pass

    def import_object(self, objPath):

        figure = pyplot.figure()
        axes = figure.add_subplot(projection='3d')

        # Load the STL files and add the vectors to the plot
        your_mesh = mesh.Mesh.from_file(objPath)

        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

        # auto scale
        scale = your_mesh.points.flatten()

        axes.auto_scale_xyz(scale, scale, scale)
        # axes.view_init(0, 0)  # from the side
        # axes.view_init(90, 0) # from top or bottom
        axes.view_init(0, 90) # from front or back
        pyplot.grid(False)
        pyplot.axis('off')
        pyplot.savefig("render.png")
        # Show the plot to the screen
        # pyplot.show()

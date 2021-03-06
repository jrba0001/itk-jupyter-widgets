"""Viewer class

Visualization of an image.

In the future, will add optional segmentation mesh overlay.
"""

import ipywidgets as widgets
from traitlets import Unicode
import numpy as np
import itk
from .trait_types import ITKImage, itkimage_serialization
HAVE_VTK = False
try:
    import vtk
    HAVE_VTK = True
except ImportError:
    pass

@widgets.register
class Viewer(widgets.DOMWidget):
    _view_name = Unicode('ViewerView').tag(sync=True)
    _model_name = Unicode('ViewerModel').tag(sync=True)
    _view_module = Unicode('itk-jupyter-widgets').tag(sync=True)
    _model_module = Unicode('itk-jupyter-widgets').tag(sync=True)
    _view_module_version = Unicode('^0.2.1').tag(sync=True)
    _model_module_version = Unicode('^0.2.1').tag(sync=True)
    image = ITKImage(default_value=None, allow_none=True).tag(sync=True, **itkimage_serialization)

def view(image):
    viewer = Viewer()
    if isinstance(image, np.ndarray):
        image_from_array = itk.GetImageViewFromArray(image)
        viewer.image = image_from_array
    elif HAVE_VTK and isinstance(image, vtk.vtkImageData):
        from vtk.util import numpy_support as vtk_numpy_support
        array = vtk_numpy_support.vtk_to_numpy(image.GetPointData().GetScalars())
        array.shape = tuple(image.GetDimensions())[::-1]
        image_from_array = itk.GetImageViewFromArray(array)
        image_from_array.SetSpacing(image.GetSpacing())
        image_from_array.SetOrigin(image.GetOrigin())
        viewer.image = image_from_array
    else:
        viewer.image = image
    return viewer

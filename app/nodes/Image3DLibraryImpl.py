####################################################################################################
#                                                                                                  #
#  Informations :                                                                                  #
#      This code is part of the project VolumeRendering                                            #
#                                                                                                  #
#  Contacts :                                                                                      #
#      couet.julien@gmail.com                                                                      #
#      benyoub.anis@gmail.com                                                                      #
#                                                                                                  #
####################################################################################################


import FabricEngine.SceneGraph
from FabricEngine.SceneGraph.Nodes.Images.BaseImageImpl import BaseImage
   

class Image3DLibrary(BaseImage):
  """A class to manage 3D images"""   
   
  def __init__(self, scene, format = 'Volume', **kwargs):
    super(Image3DLibrary, self).__init__(scene, format=format, **kwargs)

    self.getDGNode().addMember("dirty", 'Boolean', True)
    self.getDGNode().addMember("path", 'String', '')

    self.bindDGOperator(self.getDGNode().bindings,
      name='createTextureFromImage', 
      fileName=FabricEngine.SceneGraph.buildAbsolutePath('Image3DLibrary.kl'), 
      layout=[
        'self.path',
        'self.dirty',
        'self.image'],
      mainThreadOnly=True)

    # self.bindDGOperator(self.getDGNode().bindings,
    #   name='createTextureTest', 
    #   fileName=FabricEngine.SceneGraph.buildAbsolutePath('Image3DLibrary.kl'), 
    #   layout=[
    #     'self.dirty',
    #     'self.image'],
    #   mainThreadOnly=True)
 
  def evaluate(self):
    self.getDGNode().evaluate()

  def setImage(self, path):
    self.getDGNode().setData('path', path)
    self.getDGNode().setData('dirty', True)


Image3DLibrary.registerNodeClass('Image3DLibrary')
 
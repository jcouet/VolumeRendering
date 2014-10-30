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
   

class VolumeTextureLibrary(BaseImage):
  """A class to display meshes"""   
   
  def __init__(self, scene, format = 'Volume', **kwargs):
    super(VolumeTextureLibrary, self).__init__(scene, format=format, **kwargs)

    self.getDGNode().addMember("dirty", 'Boolean', True)
    self.getDGNode().addMember("path", 'String', '')

    self.bindDGOperator(self.getDGNode().bindings,
      name='createTextureFromImage', 
      fileName=FabricEngine.SceneGraph.buildAbsolutePath('VolumeTextureLibrary.kl'), 
      layout=[
        'self.path',
        'self.dirty',
        'self.image'],
      mainThreadOnly=True)

    # self.bindDGOperator(self.getDGNode().bindings,
    #   name='createTextureTest', 
    #   fileName=FabricEngine.SceneGraph.buildAbsolutePath('VolumeTextureLibrary.kl'), 
    #   layout=[
    #     'self.dirty',
    #     'self.image'],
    #   mainThreadOnly=True)
 
  def evaluate(self):
    self.getDGNode().evaluate()

  def setImage(self, path):
    self.getDGNode().setData('path', path)
    self.getDGNode().setData('dirty', True)


VolumeTextureLibrary.registerNodeClass('VolumeTextureLibrary')
 
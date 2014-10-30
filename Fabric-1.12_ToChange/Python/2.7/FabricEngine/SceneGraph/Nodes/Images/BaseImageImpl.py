
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

import FabricEngine.SceneGraph
from FabricEngine.SceneGraph.Nodes.SceneGraphNodeImpl import SceneGraphNode
from FabricEngine.SceneGraph.RT.Math.ColorImpl import Color

IMAGE2D_depthFlag = 1
IMAGE2D_mipmapFlag = 2
IMAGE2D_repeatFlag = 4

class BaseImage(SceneGraphNode):
  """The base class for all image nodes"""
  
  @classmethod
  def getNodeColor(cls):
    """Returns the color to use for the UI elements for this node"""
    return Color(191, 88, 255)

  def __init__(self, scene, format = 'RGBA', mipmaps = True, glRepeat= True, createRenderParamOperators = True, **kwargs):
    
    # ensure that base class is never instantiated
    if self.__class__.__name__ == 'BaseImage':
      raise FabricEngine.SceneGraph.SceneGraphException('You cannot instantiate the BaseImage node directly.')

    scene.loadExtension('Images')

    # call the baseclass constructor
    super(BaseImage, self).__init__(scene, **kwargs)

    self.__format = format
    
    # create DG node
    defaultImage = None
    if self.__format == 'RGB':
      defaultImage = scene.getFabricClient().RT.types.Image2DRGB.create()
    elif self.__format == 'RGBA':
      defaultImage = scene.getFabricClient().RT.types.Image2DRGBA.create()
    elif self.__format == 'Color':
      defaultImage = scene.getFabricClient().RT.types.Image2DColor.create()
    elif self.__format == 'Scalar':
      defaultImage = scene.getFabricClient().RT.types.Image2DScalar.create()
      
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
    elif self.__format == 'Volume':
      defaultImage = scene.getFabricClient().RT.types.Image2DVolume.create()

    if mipmaps:
      defaultImage.flags = defaultImage.flags | IMAGE2D_mipmapFlag
    if glRepeat:
      defaultImage.flags = defaultImage.flags | IMAGE2D_repeatFlag
    if self.__format == 'Scalar': # TODO: this is arbitrary; make this explicit
      defaultImage.flags = defaultImage.flags | IMAGE2D_depthFlag

    dgnode = self.constructDGNode()
    dgnode.addMember('image', 'Image2D' + self.__format)
    dgnode.setValue('image', 0, defaultImage)

    self.bindDGOperator(dgnode.bindings,
      name = 'initImages'+self.__format, 
      fileName = FabricEngine.SceneGraph.buildAbsolutePath('BaseImage.kl'), 
      preProcessorDefinitions = { 'PIXELFORMAT': self.__format }, 
      layout = [
        'self.image<>'
      ],
      mainThreadOnly = True
      )

    renderParams = self.constructDGNode('RenderParams')
    renderParams.setDependency('imageData', dgnode)
    renderParams.addMember('renderParamValues', 'RenderParamValues')

    if createRenderParamOperators:
      self.bindDGOperator(renderParams.bindings,
        name = 'matchCount', 
        sourceCode = 'operator matchCount(in Container parentContainer, io Container selfContainer) { \
          selfContainer.resize( parentContainer.size() ); \
        }', 
        layout = [
          'imageData', 
          'self'
        ])
    
      self.bindDGOperator(renderParams.bindings,
        name = 'loadImageRenderParams'+self.__format, 
        fileName = FabricEngine.SceneGraph.buildAbsolutePath('BaseImage.kl'), 
        preProcessorDefinitions = { 'PIXELFORMAT': self.__format }, 
        layout = [
          'imageData.image<>',
          'self.renderParamValues<>'
        ],
        mainThreadOnly = True
        )

  def getFormat(self):
    return self.__format

  def getImageNodeAndMember(self):
    return {'DGNode':self.getRenderParamsDGNode(), 'member':'renderParamValues'}
    

    

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

from FabricEngine.SceneGraph.PySide import *
from FabricEngine.SceneGraph.Nodes.Images import *
from FabricEngine.SceneGraph.Nodes.Rendering import *
from FabricEngine.SceneGraph.Nodes.Primitives import *
from FabricEngine.SceneGraph.Nodes.Manipulation import * 
from FabricEngine.SceneGraph.Nodes.Importers.OBJImporterImpl import *
from FabricEngine.SceneGraph.PySide.SceneGraphApplicationImpl import SceneGraphApplication
 
from nodes.VolumeTextureLibraryImpl import VolumeTextureLibrary


class VolumeRenderingApp(SceneGraphApplication):
 
  def __init__(self):
    FileLocationManager.addSearchLocation('realtime', [FabricEngine.SceneGraph.buildAbsolutePath( './rendering')])
    
    super(VolumeRenderingApp, self).__init__(
      guarded=False,
      basicRenderPasses=True,
      menuNames=['File'], 
      setupEditorProfiler=False)

    self.constructApplication()
    self.constructionCompleted()
 
 
# 1. Application construction
  def constructApplication(self):
    self.setWindowTitle('VolumeRendering')
    self.setupViewports(useBackgroundTexture=False)
    self.setupSunlight()

    self.setupSelection() 
    self.setupGrid()
    self.setupCamera(
      cameraPosition=Vec3(0, 0, -20),
      cameraTarget=Vec3(0.0, 0.0, 0.0),
      setupCameraLight=True)

    self.scene=self.getScene()
    self.context_id=self.scene.getFabricContextID()
    
    self.constructSceneGraph()
    self.constructScene()

 
  def constructSceneGraph(self):
    path=FabricEngine.SceneGraph.buildAbsolutePath('../data/0001.jpg')

    self.volumeTextureLibrary=VolumeTextureLibrary(self.scene)
    self.volumeTextureLibrary.setImage(path)

    self.texture2DLibrary=Image2DLibrary(self.scene)
    self.texture2DLibrary.addImage(name='texture2D', filePath=path)
    

  def constructScene(self):
    volumeRenderingMaterial=Material(
      self.scene, 
      xmlFile='VolumeRenderingMaterial',
      volumeTexture=self.volumeTextureLibrary)

    GeometryInstance(
      self.scene, 
      geometry=PolygonMeshCuboid(self.scene, length=4, width=4, height=4),
      transform=Transform(self.scene, globalXfo=Xfo(sc=Vec3(2, 2, 2))),
      material=volumeRenderingMaterial)

  
    texturedSurfaceMaterial=Material(
      self.scene, 
      xmlFile='TexturedSurfaceMaterial')

    texturedSurfaceMaterial.addPreset(
      name='texture2D', 
      diffuseTexture=(self.texture2DLibrary, 0))

    GeometryInstance(
      self.scene, 
      geometry=PolygonMeshCuboid(self.scene, length=4, width=4, height=4),
      transform=Transform(self.scene, globalXfo=Xfo(tr=Vec3(10,0,0), sc=Vec3(2, 2, 2))),
      material=texturedSurfaceMaterial,
      materialPreset='texture2D')
 
 
if __name__ == "__main__":
  app=VolumeRenderingApp()
  app.exec_()

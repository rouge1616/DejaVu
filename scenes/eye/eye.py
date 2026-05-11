import Sofa
import Sofa.Core
import Sofa.Gui
import os
from PIL import Image


#./runSofa eye.py && python merge_w_background.py


class ScreenshotController(Sofa.Core.Controller):
    def __init__(self, root, output_dir="../screenshots", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.output_dir = output_dir
        self.frame_count = 0
      

        # Load overlay once during initialization
        #background_path = "data/eye-transp.png"
        #self.background_img = Image.open(background_path).convert("RGBA")
        #self.size = self.background_img.size

        #print(f"[INIT] Loaded overlay: {background_path} | Size: {self.size}")


    def onAnimateEndEvent(self, event):
        # Save the screenshot
        simulation_path = os.path.join(self.output_dir, f"frame_{self.frame_count:04d}.png")
        #merged_path = os.path.join(self.output_dir, f"merged_{self.frame_count:04d}.png")
        
        Sofa.Gui.GUIManager.SaveScreenshot(simulation_path)
        print(f"[SCREENSHOT] Saved: {simulation_path}")
        
        #simulation_img = Image.open(simulation_path).convert("RGBA")
        #simulation_img = simulation_img.resize(self.size, Image.Resampling.NEAREST)
        #simulation_img.paste(self.background_img, (0, 0), self.background_img)
        #simulation_img.save(merged_path)

        #print(f"[MERGED] Saved merged image: {merged_path}")

        self.frame_count += 1




def createScene(rootNode):

    # Root Node setup
    rootNode.gravity = [0, 0, 0]
    rootNode.dt = 0.02
    rootNode.name = "root"
    rootNode.addObject("ViewerSetting", resolution=[1200, 880])

    # Use this if you want to add the background. It will slow down the simultion
    rootNode.addObject(ScreenshotController(rootNode))

    # Background and viewer settings
    rootNode.addObject('BackgroundSetting', image='data/eye-diffuse.png')
    rootNode.addObject('ViewerSetting', resolution=[1200, 880])

    # Visual style and camera
    rootNode.addObject('VisualStyle', displayFlags='showVisualModels hideBehaviorModels hideCollisionModels hideMappings hideForceFields hideWireframe')
    rootNode.addObject('InteractiveCamera', name='camera')

    # Sclera Node
    scleraNode = rootNode.addChild('Sclera')
    scleraNode.activated = True

    # Topology Node
    topologyNode = scleraNode.addChild('Topology')
    inputB = topologyNode.addObject('MeshVTKLoader', name='inputB', filename='data/mesh/Sclera.vtk')
    hexaTop = topologyNode.addObject('MeshTopology', name='HexaTop', src=inputB.getLinkPath())
    container = topologyNode.addObject('TetrahedronSetTopologyContainer', name='Container', position=hexaTop.getLinkPath() + '.position')
    topologyNode.addObject('TetrahedronSetTopologyModifier', name='Modifier')
    topologyNode.addObject('Hexa2TetraTopologicalMapping', input=hexaTop.getLinkPath(), output=container.getLinkPath(), swapping=True)

    # Physics Node
    physicsNode = scleraNode.addChild('Physics')
    physicsNode.addObject('EulerImplicitSolver', vdamping=2)
    physicsNode.addObject('CGLinearSolver', iterations=20, tolerance=1e-5, threshold=1e-5)

    # Container and DOFs
    physicsNode.addObject('TetrahedronSetTopologyContainer', name='HexaContainer', src=container.getLinkPath())
    dofs = physicsNode.addObject('MechanicalObject', template='Vec3d', name='DOFs')
    physicsNode.addObject('TetrahedronFEMForceField', name='FEM', youngModulus=25000, poissonRatio=0.45)
    physicsNode.addObject('UniformMass', name='mass', totalMass=7.0)

    # BoxROIs for muscles and constraints
    musclesROI = physicsNode.addObject('BoxROI', name='Muscles', box=[-12, -6, -1, -8, 3, 6,
                                                                       11, -6, -1, 15, 3, 6,
                                                                       -3, 7, -1, 6, 13, 6,
                                                                       -3, -16, -1, 6, -10, 6],
                                       drawBoxes=False, drawSize=3)

    muscleBackROI = physicsNode.addObject('BoxROI', name='Muscleback', box=[-2, -3, -11, 2, 3, -7])

    # RestShapeSpringsForceField
    physicsNode.addObject('RestShapeSpringsForceField', name='MuscleRSFF',
                          stiffness=2e4,
                          angularStiffness=1e3,
                          external_rest_shape=dofs.getLinkPath(),
                          external_points=musclesROI.getLinkPath() + '.indices',
                          points=musclesROI.getLinkPath() + '.indices',
                          drawSpring=True)

    # PartialFixedConstraint
    physicsNode.addObject('PartialFixedConstraint', template='Vec3d',
                          indices=muscleBackROI.getLinkPath() + '.indices',
                          drawSize=0,
                          fixedDirections=[1, 1, 1])

    # Visual node
    visualNode = physicsNode.addChild('Visual')

    # Cornea visual
    corneaNode = visualNode.addChild('cornea')
    corneaNode.activated = True
    corneaNode.addObject('OglModel', name='VisualModel', fileMesh='data/objects/cornea_uv_clean.obj',
                         useNormals=True, putOnlyTexCoords=True)
    corneaNode.addObject('OglShader', vertFilename='shaders/shaderLibrary.glsl',
                         fragFilename='shaders/shaderLibrary.glsl')
    corneaNode.addObject('OglTexture', id='DiffuseMap', textureFilename='data/eye-diffuse-smudge.png',
                         textureUnit=1, repeat=True, generateMipmaps=False)
    corneaNode.addObject('OglShaderDefineMacro', id='DiffuseMap_Present')
    corneaNode.addObject('OglFloat3Variable', id='LightPosition', value=[0, 0, 500])
    corneaNode.addObject('OglFloat3Variable', id='LightColor', value=[1, 1, 1])
    corneaNode.addObject('OglFloat3Variable', id='DiffuseColor', value=[1, 1, 1])
    corneaNode.addObject('OglFloat3Variable', id='AmbientColor', value=[0.2, 0.2, 0.2])
    corneaNode.addObject('OglFloat3Variable', id='SpecularColor', value=[1, 1, 1])
    corneaNode.addObject('OglFloatVariable', name='SpecularRoughness', value=0.04)
    corneaNode.addObject('OglFloatVariable', name='SpecularReflectance', value=0.04)
    corneaNode.addObject('BarycentricMapping')

    # Sclera visual
    scleraVisualNode = visualNode.addChild('Sclera')
    scleraVisualNode.activated = False
    scleraVisualNode.addObject('OglModel', name='VisualModel', fileMesh='data/objects/r_sclera_uv.obj')
    scleraVisualNode.addObject('BarycentricMapping')

    # Conjunctiva visual
    conjunctivaNode = visualNode.addChild('Conjunctiva')
    conjunctivaNode.activated = True
    conjunctivaNode.addObject('OglModel', name='Visual',
                              filename='data/objects/r_conjunctiva_uv.obj',
                              putOnlyTexCoords=True,
                              texturename='data/eye-diffuse-smudge.png',
                              material="MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 0 255 255 255 1 Emissive 0 1 1 1 1 Shininess 1 45")
    conjunctivaNode.addObject('BarycentricMapping')

    # Trocars nodes
    trocar_configs = [
        ('Trocars1', [(10, 2, 5.7), (0, 30, 0)]),
        ('Trocars2', [(8, -4, 7.2), (0, 30, 0)]),
        ('Trocars3', [(-8, 2, 5.5), (0, -25, 0)]),
        ('Trocars4', [(-6, -4, 6.5), (0, -40, 0)]),
    ]

    for trocar_name, (translation, rotation) in trocar_configs:
        trocarNode = visualNode.addChild(trocar_name)

        p1 = trocarNode.addChild(f'{trocar_name}p1')
        p1.activated = True
        p1.addObject('OglModel', name='Visual', filename='data/trocars/trocar_part1.obj',
                     translation=translation, rotation=rotation)
        p1.addObject('BarycentricMapping')

        p2 = trocarNode.addChild(f'{trocar_name}p2')
        p2.activated = True
        p2.addObject('OglModel', name='Visual', filename='data/trocars/trocar_part2.obj',
                     translation=translation, rotation=rotation)
        p2.addObject('BarycentricMapping')


def main():
    root = Sofa.Core.Node("root")
    createScene(root)

if __name__ == '__main__':
    main()

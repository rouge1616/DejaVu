import Sofa
import Sofa.Core

def createScene(rootNode):
    rootNode.gravity = [0, 0, 0]
    rootNode.dt = 0.005
    rootNode.animate = False

    rootNode.addObject('ViewerSetting', resolution=[960, 540])
    #rootNode.addObject('BackgroundSetting', image='data/liver.png')
    rootNode.addObject('VisualStyle', displayFlags='showCollisionModels hideForceFields hideBehaviorModels')
    rootNode.addObject('DefaultAnimationLoop')

    liver = rootNode.addChild('LIVER')
    liver.addObject('EulerImplicitSolver')
    liver.addObject('CGLinearSolver', iterations=200, tolerance=1e-9, threshold=1e-9)

    liver.addObject('SparseGridTopology', name='volume', fileTopology='data/parenchyma_001.obj', n=[16, 16, 16])
    liver.addObject('MechanicalObject', name='DOFs', template='Vec3d')
    liver.addObject('UniformMass', totalMass=3)
    liver.addObject('TetrahedronFEMForceField', name='Corot', youngModulus=800, poissonRatio=0.45, method='large', rayleighStiffness=0.5)

    liver.addObject('BoxROI', name='ROI1', box=[-0.10, 0, -0.20, 0.06, 0.05, 0.01], drawBoxes=False)
    liver.addObject('FixedConstraint', template='Vec3d', indices='@ROI1.indices', drawSize=0)

    liver.addObject('BoxROI', name='ROI2', box=[0, -0.10, -0.10, 0.16, 0.05, -0.05], drawBoxes=False)
    liver.addObject('FixedConstraint', template='Vec3d', indices='@ROI2.indices', drawSize=0)

    liver.addObject('BoxROI', name='ROI3', box=[0, -0.02, -0.05, 0.16, 0.02, -0.02], drawBoxes=False)
    liver.addObject('FixedConstraint', template='Vec3d', indices='@ROI3.indices', drawSize=0)

    liver.addObject('BoxROI', name='ROI4', box=[0.08, -0.04, 0.05, 0.10, -0.02, 0.07], drawBoxes=False)
    liver.addObject('LinearForceField',
                    points='@ROI4.indices',
                    forces="0 0 1 0 0.5 -1 0 0 2 0 -1 0 0 0 0",
                    force=0.2,
                    times="0 1 2 3 4",
                    arrowSizeCoef=0)

    # Liver Visual
    visLiver = liver.addChild('LiverVisual')
    visLiver.activated = True
    visLiver.addObject('OglModel',
                       name='Visual',
                       filename='data/parenchyma_uv.obj',
                       scale3d=[0.01, 0.01, 0.01],
                       putOnlyTexCoords=True,
                       texturename='data/liver.png',
                       material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 0 255 255 255 1 Emissive 1 255 255 255 1 Shininess 1 45')
    visLiver.addObject('BarycentricMapping')

    # Square
    square = liver.addChild('Square')
    square.activated = True
    square.addObject('OglModel',
                     name='Visual',
                     filename='data/square_2594_triangles.obj',
                     scale3d=[0.0354, 0.02, 0.02],
                     rotation=[10, -25, 163],
                     translation=[0.235, 0.005, -0.13],
                     putOnlyTexCoords=True,
                     texturename='data/liver.png',
                     material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 0 255 255 255 1 Emissive 1 255 255 255 1 Shininess 1 45')

    # Tool body
    body = liver.addChild('VisualToolBody')
    body.activated = True
    body.addObject('OglModel',
                   name='VM',
                   fileMesh='data/dv_tool/body_uv.obj',
                   scale3d=[0.002, 0.002, 0.002],
                   rotation=[180, 0, 90],
                   translation=[0.09, -0.03, 0.085],
                   putOnlyTexCoords=True,
                   texturename='data/dv_tool/instru.png',
                   material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 0 255 255 255 1 Emissive 0 1 1 1 1 Shininess 1 45')
    body.addObject('BarycentricMapping')

    # Tool Clasper 1
    clasper1 = liver.addChild('VisualToolClasper1')
    clasper1.activated = True
    clasper1.addObject('OglModel',
                       name='VM',
                       fileMesh='data/dv_tool/clasper1_uv.obj',
                       scale3d=[0.002, 0.002, 0.002],
                       rotation=[180, 0, 90],
                       translation=[0.09, -0.03, 0.085],
                       putOnlyTexCoords=True,
                       texturename='data/dv_tool/instru_clasper.png',
                       material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 0 255 255 255 1 Emissive 0 1 1 1 1 Shininess 1 45')
    clasper1.addObject('BarycentricMapping')

    # Tool Clasper 2
    clasper2 = liver.addChild('VisualToolClasper2')
    clasper2.activated = True
    clasper2.addObject('OglModel',
                       name='VM',
                       fileMesh='data/dv_tool/clasper2_uv.obj',
                       scale3d=[0.002, 0.002, 0.002],
                       rotation=[180, 0, 90],
                       translation=[0.09, -0.03, 0.085],
                       putOnlyTexCoords=True,
                       texturename='data/dv_tool/instru_clasper.png',
                       material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 0 255 255 255 1 Emissive 0 1 1 1 1 Shininess 1 45')
    clasper2.addObject('BarycentricMapping')
    
    
    # Optional visual vessels (commented out in XML)
    """
    # HVVisual Node
    hv_visual = liver.addChild('HVVisual')
    hv_visual.activated = True
    hv_visual.addObject('VisualStyle', displayFlags='showWireframe')
    hv_visual.addObject('OglModel',
                        name='Visual',
                        filename='data/hepatic_vein.obj',
                        scale3d=[0.01, 0.01, 0.01])
    hv_visual.addObject('BarycentricMapping')

    # PVVisual Node
    pv_visual = liver.addChild('PVVisual')
    pv_visual.activated = True
    pv_visual.addObject('VisualStyle', displayFlags='showWireframe')
    pv_visual.addObject('OglModel',
                        name='Visual',
                        filename='data/portal_vein.obj',
                        scale3d=[0.01, 0.01, 0.01])
    pv_visual.addObject('BarycentricMapping')
    """    

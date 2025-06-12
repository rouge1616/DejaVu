import Sofa
import Sofa.Core

def createScene(rootNode):
    rootNode.gravity = [0, 0, 0]
    rootNode.dt = 0.01
    rootNode.animate = False

    rootNode.addObject('ViewerSetting', resolution=[950, 700])
    rootNode.addObject('BackgroundSetting')
    rootNode.addObject('VisualStyle', displayFlags='hideCollisionModels hideForceFields hideBehaviorModels')

    rootNode.addObject('DefaultAnimationLoop')
    rootNode.addObject('DefaultPipeline', verbose=0, depth=10, draw=0)
    rootNode.addObject('BruteForceBroadPhase')
    rootNode.addObject('BVHNarrowPhase')
    rootNode.addObject('MinProximityIntersection', name='Proximity', alarmDistance=0.1, contactDistance=0.1)
    rootNode.addObject('DefaultContactManager', name='Response', response='PenalityContactForceField')

    # Brain node
    brain = rootNode.addChild('Brain')
    brain.addObject('EulerImplicitSolver')
    brain.addObject('CGLinearSolver', iterations=100, tolerance=1e-9, threshold=1e-9)

    brain.addObject('SparseGridTopology', name='volume', fileTopology='data/volume_simplified.obj', n=[16, 16, 16])
    brain.addObject('MechanicalObject', name='gridDOFs', template='Vec3d')
    brain.addObject('UniformMass', totalMass=0.01)
    brain.addObject('TetrahedronFEMForceField', name='Corot', youngModulus=20, poissonRatio=0.40, method='large', rayleighStiffness=0.05)

    brain.addObject('BoxROI', name='ROI1', box=[-70, -50, -60, 50, 50, -20], drawBoxes=False)
    brain.addObject('FixedConstraint', template='Vec3d', indices='@ROI1.indices', drawSize=0)

    brain.addObject('BoxROI', name='ROI2', box=[20, -50, -50, 70, 50, 50], drawBoxes=False)
    brain.addObject('FixedConstraint', template='Vec3d', indices='@ROI2.indices', drawSize=0)

    brain.addObject('BoxROI', name='ROI3', box=[-70, 30, -60, 70, 50, 50], drawBoxes=False)
    brain.addObject('FixedConstraint', template='Vec3d', indices='@ROI3.indices', drawSize=0)

    brain.addObject('BoxROI', name='ROI4', box=[-70, -40, -60, 70, -60, 50], drawBoxes=False)
    brain.addObject('FixedConstraint', template='Vec3d', indices='@ROI4.indices', drawSize=0)

    visual = brain.addChild('Visual')
    visual.activated = True
    visual.addObject('MeshOBJLoader', name='loader', filename='data/surface_full.obj')
    visual.addObject('OglModel',
                     name='Visual',
                     src='@loader',
                     putOnlyTexCoords=True,
                     texturename='data/texture_outpaint.png',
                     material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 1 255 255 255 1 Emissive 1 255 255 255 1 Shininess 1 45')
    visual.addObject('BarycentricMapping')

    # Skull node
    skull = rootNode.addChild('Skull')
    visual_skull = skull.addChild('Visual')
    visual_skull.activated = True
    visual_skull.addObject('MeshOBJLoader',
                           name='loader',
                           filename='data/surface_skull.obj',
                           scale3d=[0.92, 0.92, 0.92],
                           translation=[-5, -2.5, 7.5])
    visual_skull.addObject('OglModel',
                           src='@loader',
                           putOnlyTexCoords=True,
                           texturename='data/texture.png',
                           material='MAT Diffuse 1 255 255 255 1 Ambient 1 255 255 255 1 Specular 1 255 255 255 1 Emissive 1 255 255 255 1 Shininess 1 45')
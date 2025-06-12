import Sofa
import Sofa.Core

def createScene(rootNode):
    rootNode.name = "root"
    rootNode.gravity = [0, 0, 0]
    rootNode.dt = 0.01
    rootNode.animate = False

    rootNode.addObject("ViewerSetting", resolution=[854, 480])
    rootNode.addObject("BackgroundSetting", image="data/uterus-inpaint.png")
    rootNode.addObject("VisualStyle", displayFlags="hideWireframe hideCollisionModels hideForceFields hideBehaviorModels")
    rootNode.addObject("DefaultAnimationLoop")

    uterus = rootNode.addChild("UTERUS")

    uterus.addObject("EulerImplicit")
    uterus.addObject("CGLinearSolver", iterations=200, tolerance=1e-9, threshold=1e-9)
    uterus.addObject("SparseGrid", name="volume", fileTopology="data/sphere_uv.obj", n=[16, 16, 16])
    uterus.addObject("MechanicalObject", template="Vec3d", name="gridDOFs")
    uterus.addObject("UniformMass", totalMass=0.03)
    uterus.addObject("TetrahedronFEMForceField", name="Corot", youngModulus=2500, poissonRatio=0.35, method="large")

    # ROIs and constraints
    uterus.addObject("BoxROI", name="ROI1", box=[1, 1, -0.2, -1, -1, -1], drawBoxes=False)
    uterus.addObject("FixedConstraint", template="Vec3d", indices="@ROI1.indices", drawSize=0)

    uterus.addObject("BoxROI", name="ROI2", box=[1, 1, 1, 0.5, -1, -1], drawBoxes=False)
    uterus.addObject("FixedConstraint", template="Vec3d", indices="@ROI2.indices", drawSize=0)

    uterus.addObject("BoxROI", name="ROI3", box=[1, -0.5, 1, -1, 0.1, -1], drawBoxes=False)
    uterus.addObject("FixedConstraint", template="Vec3d", indices="@ROI3.indices", drawSize=0)

    uterus.addObject("BoxROI", name="ROI4", box=[0.5, 0.7, 0.5, -0.5, 1.5, -0.5], drawBoxes=False)
    uterus.addObject("LinearForceField",
                     points="@ROI4.indices",
                     forces=[
                         0, -1, 0, 0, -1, 0, 0, -1, 0,
                         0, -1, 0, 0, -1, 0, 0, -1, 0,
                         0, 0, 0, 0, -1, 0, 0, -1, 0,
                         0, -1, 0, 0, -1, 0, 0, -1, 0,
                         0, -1, 0, 0, 0, 0
                     ],
                     force=5,
                     times=[0, 0.4, 0.8, 1.2, 1.6, 2, 2.4, 2.8, 3.2, 3.6, 4],
                     arrowSizeCoef=0)

    # Visual Surface Node
    vis = uterus.addChild("VisualSurface")
    vis.activated = True
    vis.addObject("OglModel", name="VisualModel", fileMesh="data/sphere_uv.obj", putOnlyTexCoords=True, updateNormals=False)
    vis.addObject("OglShader", vertFilename="shaders/shaderLibrary.glsl", fragFilename="shaders/shaderLibrary.glsl")
    vis.addObject("OglTexture", id="DiffuseMap", textureFilename="data/uterus-pot.png", textureUnit=1, repeat=True, generateMipmaps=False)
    vis.addObject("OglShaderDefineMacro", id="DiffuseMap_Present")
    vis.addObject("OglFloat3Variable", id="LightPosition", value=[-0.18, 0, 50])
    vis.addObject("OglFloat3Variable", id="LightColor", value=[0.1, 0.1, 0.1])
    vis.addObject("OglFloat3Variable", id="DiffuseColor", value=[1, 1, 1])
    vis.addObject("OglFloat3Variable", id="AmbientColor", value=[1, 1, 1])
    vis.addObject("OglFloat3Variable", id="SpecularColor", value=[1, 1, 1])
    vis.addObject("OglFloatVariable", id="SpecularRoughness", value=0.035)
    vis.addObject("OglFloatVariable", id="SpecularReflectance", value=0.04)
    vis.addObject("BarycentricMapping", name="visual-mapping", input="@../gridDOFs", output="@VisualModel")

    # Tumor Visual Node
    tum = uterus.addChild("TumVisual")
    tum.activated = True
    tum.addObject("OglModel", name="VisualModel", filename="data/tumor.obj", translation=[-8, 0.7, -1.6],
                  material="MAT Diffuse 1 0.7 0.7 0.7 1 Ambient 1 1 1 1 1 Specular 0 255 255 255 1 Emissive 0 1 1 1 1 Shininess 0 45")
    tum.addObject("BarycentricMapping", name="visual-mapping", input="@../gridDOFs", output="@VisualModel")

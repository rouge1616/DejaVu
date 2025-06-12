import Sofa

def createScene(rootNode):
    # Set root-level parameters
    rootNode.gravity = "0 0 0"
    rootNode.dt = 0.01
    rootNode.animate = 0  # equivalent to "animate=0" in XML

    # Add some global objects
    rootNode.createObject("ViewerSetting", resolution=[1000, 800])
    rootNode.createObject("BackgroundSetting", image="data/kidney-inpaint.png")
    rootNode.createObject("VisualStyle",
                          displayFlags="hideCollisionModels hideForceFields hideBehaviorModels hideWireframe")
    rootNode.createObject("DefaultAnimationLoop")

    # Create the FEM node
    fem = rootNode.createChild("FEM")
    fem.createObject("EulerImplicitSolver")
    fem.createObject("CGLinearSolver", iterations=200, tolerance=1e-9, threshold=1e-9)
    # fem.createObject("SparseGrid", name="volume", fileTopology="data/kidney_pig_surface_smooth.obj", n=[12, 8, 12])
    
    fem.createObject("MeshVTKLoader", name="meshLoader", filename="data/kidney_pig_volume.vtu")
    fem.createObject("TetrahedronSetTopologyContainer", name="Container", src="@meshLoader")
    fem.createObject("TetrahedronSetTopologyModifier", name="Modifier")
    fem.createObject("TetrahedronSetGeometryAlgorithms", name="GeomAlgo")

    fem.createObject("MechanicalObject", template="Vec3d", name="MO")
    fem.createObject("UniformMass", totalMass=1)
    fem.createObject("TetrahedronFEMForceField", name="Corot",
                     youngModulus=2000, poissonRatio=0.45, method="large")

    # ROI and constraints / forces
    fem.createObject("BoxROI", name="ROI1", box="20 40 -960 70 100 -950", drawBoxes=False)
    fem.createObject("FixedConstraint", template="Vec3d", indices="@ROI1.indices", drawSize=0)

    fem.createObject("BoxROI", name="ROI2", box="40 40 -1040 100 100 -1030", drawBoxes=False)
    fem.createObject("FixedConstraint", template="Vec3d", indices="@ROI2.indices", drawSize=0)

    fem.createObject("BoxROI", name="ROI3", box="80 80 -990 90 100 -980", drawBoxes=False)
    fem.createObject("LinearForceField",
                     points="@ROI3.indices",
                     forces="-1 0 0 1 0.5 0 -1 0.4 0.8 1 0.6 -0.8 -1 0 0",
                     force=15000,
                     times="0 0.5 1 1.5 2 2.5 3",
                     arrowSizeCoef=0)

    # -------------------------------------------------------------------------
    # Visual surface: mapping the FEM mechanical object onto a visual model
    visualSurface = fem.createChild("VisualSurface")
    visualSurface.activated = True
    visualSurface.createObject("OglModel",
                               name="VisualModel",
                               fileMesh="data/kidney_pig_surface_smooth.obj",
                               putOnlyTexCoords=True,
                               texturename="data/kidney-texture.png",
                               material=("MAT Diffuse 1 255 255 255 1 "
                                         "Ambient 1 255 255 255 1 "
                                         "Specular 0 255 255 255 1 "
                                         "Emissive 0 1 1 1 1 "
                                         "Shininess 1 45"))
    visualSurface.createObject("BarycentricMapping",
                               name="visual-mapping",
                               input="@../MO",
                               output="@VisualModel")

    # -------------------------------------------------------------------------
    # Visualize vessels
    visualVessels = fem.createChild("VisualVessels")
    visualVessels.activated = True
    visualVessels.createObject("VisualStyle", displayFlags="showWireframe")
    visualVessels.createObject("OglModel",
                               name="VisualModel",
                               fileMesh="data/kidney_pig_vessels_smooth.obj",
                               color=[0.2, 0.2, 0.8, 0.35])
    visualVessels.createObject("BarycentricMapping",
                               name="visual-mapping",
                               input="@../MO",
                               output="@VisualModel")

    # -------------------------------------------------------------------------
    # Visualize the tool body
    visualToolBody = fem.createChild("VisualToolBody")
    visualToolBody.activated = True
    visualToolBody.createObject("VisualStyle", displayFlags="hideWireframe")
    visualToolBody.createObject("OglModel",
                                name="VisualModel",
                                fileMesh="data/dv_tool/body_uv.obj",
                                scale3d=[1, 1, 1],
                                rotation=[90, 90, 0],
                                translation=[85, 95, -985],
                                putOnlyTexCoords=True,
                                texturename="data/dv_tool/instru.png",
                                material=("MAT Diffuse 1 255 255 255 1 "
                                          "Ambient 1 255 255 255 1 "
                                          "Specular 0 255 255 255 1 "
                                          "Emissive 0 1 1 1 1 "
                                          "Shininess 1 45"))
    visualToolBody.createObject("BarycentricMapping")

    # -------------------------------------------------------------------------
    # Visualize the tool clasper(s)
    visualToolClasper1 = fem.createChild("VisualToolClasper")
    visualToolClasper1.activated = True
    visualToolClasper1.createObject("VisualStyle", displayFlags="hideWireframe")
    visualToolClasper1.createObject("OglModel",
                                    name="VisualModel",
                                    fileMesh="data/dv_tool/clasper1_uv.obj",
                                    scale3d=[1, 1, 1],
                                    rotation=[90, 90, 0],
                                    translation=[85, 95, -985],
                                    putOnlyTexCoords=True,
                                    texturename="data/dv_tool/instru_clasper.png",
                                    material=("MAT Diffuse 1 255 255 255 1 "
                                              "Ambient 1 255 255 255 1 "
                                              "Specular 0 255 255 255 1 "
                                              "Emissive 0 1 1 1 1 "
                                              "Shininess 1 45"))
    visualToolClasper1.createObject("BarycentricMapping")

    visualToolClasper2 = fem.createChild("VisualToolClasper")
    visualToolClasper2.activated = True
    visualToolClasper2.createObject("VisualStyle", displayFlags="hideWireframe")
    visualToolClasper2.createObject("OglModel",
                                    name="VisualModel",
                                    fileMesh="data/dv_tool/clasper2_uv.obj",
                                    scale3d=[1, 1, 1],
                                    rotation=[90, 90, 0],
                                    translation=[85, 95, -985],
                                    putOnlyTexCoords=True,
                                    texturename="data/dv_tool/instru_clasper.png",
                                    material=("MAT Diffuse 1 255 255 255 1 "
                                              "Ambient 1 255 255 255 1 "
                                              "Specular 0 255 255 255 1 "
                                              "Emissive 0 1 1 1 1 "
                                              "Shininess 1 45"))
    visualToolClasper2.createObject("BarycentricMapping")
    
    return rootNode

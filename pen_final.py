#!/usr/bin/python
 
import getpass
import sys

from Transformation import *
import time

# import the python renderman library
import prman

# create an instance of the RenderMan interface
ri = prman.Ri()

filename = "scene.rib"

# beginning of RIB archive
ri.Begin(filename)


# ArchiveRecord is used to add elements to the rib stream in this case comments
# note the function is overloaded so we can concatinate output
ri.ArchiveRecord(ri.COMMENT, 'File ' +filename)
ri.ArchiveRecord(ri.COMMENT, "Created by " + getpass.getuser())
ri.ArchiveRecord(ri.COMMENT, "Creation Date: " +time.ctime(time.time()))


# FILENAME DISPLAY Type Output format
ri.Display("scene.exr", "it", "rgba")


# Specify PAL resolution 1:1 pixel Aspect ratio
ri.Format(1280,720,1)


# sampling to 720 to reduce noise, put pixel variance low for better look.
ri.Hider("raytrace",{"int incremental" :[1], "int maxsamples":720, "int minsamples":720})
ri.PixelVariance (0.01)
ri.Exposure(1,2.2)


# path tracer for final lighting and shading
ri.Integrator ("PxrDefault" , "integrator")
ri.Integrator ("PxrVCM" ,"integrator")
ri.Integrator ("PxrDirectLighting" ,"integrator")
ri.Integrator ("PxrPathTracer" ,"integrator")


# now set the projection to perspective
ri.Projection(ri.PERSPECTIVE,{ri.FOV:40})
ri.Translate(-1.5,0,5)
ri.Rotate(-20,1,0,0)


# setting depth of field
ri.DepthOfField(5.4, 0.6, 5.3 )


# now we start our world
ri.WorldBegin()

            
#-------------------------- Lights ----------------------------
""" adding about 6 lights to give a good illumination of the objet
    4 Area lights: 2 positioned at bottom left and right
                   1 near the centre
                   1 enviroment light using hdri to have a better light color

    2 Sphere lights: positioned at top left and right
"""
# Center Light
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdAreaLight", {ri.HANDLEID:"areaLight",
                                        "float exposure"  : [4.5]
                                       })
ri.Translate( 1, 2.7, 0)
ri.Sphere( 0.5, -0.5, 0.5, 360)
ri.AttributeEnd()


# Bottom right Light
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
ri.AreaLightSource("PxrStdAreaLight", {ri.HANDLEID:"areaLight",
                                       "float exposure"  : [4.5]
                                      })
ri.Translate(6,2,0)
ri.Sphere( 0.5, -0.5, 0.5, 360)
ri.AttributeEnd()


# Bottom left Light
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
ri.AreaLightSource("PxrStdAreaLight", {ri.HANDLEID:"areaLight",
                                       "float exposure"  : [4.5]
                                      })
ri.Translate(-0.7,2.7,0)
ri.Sphere( 0.5, -0.5, 0.5, 360)
ri.AttributeEnd()


# Environment Map
ri.AttributeBegin()
ri.Declare("areaLight" ,"string")
ri.AreaLightSource( "PxrStdEnvMapLight", {ri.HANDLEID:"areaLight", 
                                          "float exposure" : [0.1],
                                          "string rman__EnvMap" : ["kiara_9_dusk_1k.tx"]
                                        })
lightTx=Transformation()
lightTx.setPosition(1,0,1)
lightTx.setScale(1,1,1)
ri.ConcatTransform(lightTx.getMatrix())
ri.Geometry('envsphere')
ri.AttributeEnd()


ri.Bxdf( "PxrDisney","bxdf", { 
                              "color emitColor" : [ 1,1,1]
                             })


# Top left
ri.TransformBegin()
ri.Translate(-1.5, 5,-2)
ri.Scale(3,3,3)
ri.Geometry("spherelight")
ri.TransformEnd()


# Top right
ri.TransformBegin()
ri.Translate(5, 5,-2)
ri.Scale(3,3,3)
ri.Geometry("spherelight")
ri.TransformEnd()
#--------------------------------------------------------------------------------------------


#-------------------------------Modelling----------------------------------------------------
# modelling the pen

ri.TransformBegin()

ri.Rotate(80,0,1,0)
ri.Rotate(120,0,0,1)
ri.Rotate(-90,1,0,0)

# the cap base
ri.TransformBegin()
ri.AttributeBegin()
ri.ShadingRate(2)

# appling displacement map for the linear pattern
ri.Attribute("trace", {
                      "displacements" : [1]
                      })

ri.Attribute("displacementbound", {
                                  "sphere" : [30],
                                  "coordinatesystem" : ["shader"]
                                  })

ri.Pattern("PxrOSL", "noise", {
                              "string shader": "noise"                        
                              })

ri.Displacement("doDisplace", {
                              "reference float disp": ["noise:resultF"],
                              "float atten": [0.005]
                              })

# applying bump map for the compnay logo
ri.Pattern("PxrBump", "text", {
                              "string filename": "lamy_9.tx",
                              "float scale" : [0.1]
                              })

ri.Bxdf( "PxrDisney","bxdf", { 
                             "color baseColor" : [ 0.8, 0.2, 0.2], 
                             "reference normal bumpNormal" :["text:resultN"],
                             "float metallic" : [0.5]
                             })
                                          
ri.Translate(0,-0.5,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.22,-0.75,0.75,360)
ri.AttributeEnd()
ri.TransformEnd()


# the cap top
ri.TransformBegin()
ri.AttributeBegin()

# applying scratches
ri.Pattern("PxrBump", "scratch", {
                                  "string filename": "scratch_new.tx",
                                  "float scale" : [0.005]
                                 })

ri.Bxdf("PxrDisney", "bxdf",{
                            "color baseColor" : [ 0.8, 0.2, 0.2],
                            "reference normal bumpNormal" :["scratch:resultN"],
                            "float metallic": [1],
                            "float specular":[1]
                            })

ri.Translate(0,0.45,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.20,-0.20,0.20,360)
ri.AttributeEnd()
ri.TransformEnd()


# the holder
ri.TransformBegin()
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2], 
                              "float metallic" : [1]
                             })
ri.Translate(0.27,-0.15,0)
ri.Rotate(90,0,1,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.07,-0.8,0.8,180)
ri.AttributeEnd()
ri.TransformEnd()


# cap holder joint
ri.TransformBegin()
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2], 
                              "float metallic" : [1]
                             })
ri.Translate(0.25,0.45,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.07,-0.2,0.2,360)
ri.AttributeEnd()
ri.TransformEnd()


#the holder circle
ri.TransformBegin()
ri.Translate(0.27,-0.8,-0.12)
ri.Rotate(90,0,0,1)
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2], 
                              "float metallic" : [1]
                             })
ri.Sphere(0.06, -0.0001, 0.06, 180)
ri.AttributeEnd()
ri.TransformEnd()


# the middle rings' base
ri.TransformBegin()
ri.Translate(0,-1.5,0)
ri.AttributeBegin()

ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2], 
                              "float metallic" : [0.5]
                             })
ri.Rotate(90,1,0,0)
ri.Cylinder(0.19,-0.25,0.25,360)
ri.Translate(0,0,-0.3)

# the rings as a combination of torus and cylinder
ri.TransformBegin()
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                             "color baseColor" : [ 0.8, 0.2, 0.2], 
                             "float metallic" : [1]
                             })
for i in range(1,7,1):
  ri.Translate(0.01,0,i*0.08)
  ri.Torus(0.165,0.04,0,360,360)
  ri.Cylinder(0.202,-0.013,0.013,360)

ri.AttributeEnd()
ri.TransformEnd()

ri.AttributeEnd()
ri.TransformEnd()

# the body
ri.TransformBegin()
ri.AttributeBegin()
ri.ShadingRate(2)

# applying scratches
ri.Pattern("PxrBump", "scratchbody", {
                                      "string filename": "scratch.tx",
                                      "float scale" : [0.005]
                                     })

# appling displacement map for the linear pattern
ri.Attribute("trace", {
                      "displacements" : [1]
                      })

ri.Attribute("displacementbound", {
                                  "sphere" : [30],
                                  "coordinatesystem" : ["shader"]
                                  })

ri.Pattern("PxrOSL", "noise", {
                              "string shader": "noise"                        
                              })

ri.Displacement("doDisplace", {
                              "reference float disp": ["noise:resultF"],
                              "float atten": [0.005]
                              })

ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2],
                              "reference normal bumpNormal" :["scratchbody:resultN"], 
                              "float metallic" : [0.5]
                             })

ri.Translate(0,-3.25,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.21,-1.5,1.5,360)
ri.AttributeEnd()
ri.TransformEnd()

# the base ring
ri.TransformBegin()
ri.AttributeBegin()
ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2], 
                              "float metallic" : [0.5]
                             })
ri.Translate(0,-4.7,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.21,-0.025,0.025,360)
ri.AttributeEnd()
ri.TransformEnd()

# the base
ri.TransformBegin()
ri.AttributeBegin()

ri.Bxdf( "PxrDisney","bxdf", { 
                              "color baseColor" : [ 0.8, 0.2, 0.2], 
                              "float metallic" : [1]
                             })

ri.Translate(0,-4.9,0)
ri.Rotate(90,1,0,0)
ri.Cylinder(0.19,-0.15,0.15,360)
ri.AttributeEnd()
ri.TransformEnd()

ri.TransformEnd()

# floor with a wooden texture
ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(0,4.8,0)
ri.Pattern("PxrTexture", "wood",{ "string filename" : "wood.tx"})


ri.Bxdf( "PxrDisney","bxdf", { 
                              "reference color baseColor" : ["wood:resultRGB"], 
                             })

s=15.0
face=[-s,-5,-s, s,-5,-s,-s,-5,s, s,-5,s]
ri.Patch("bilinear",{'P':face})
ri.AttributeEnd()
ri.TransformEnd()

# wall with an rough ivy texture
ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(0,4.8,14)
ri.Rotate(90,1,0,0)

ri.Pattern("PxrTexture", "wall",{ "string filename" : "ivy.tx"})


ri.Bxdf( "PxrDisney","bxdf", { 
                              "reference color baseColor" : ["wall:resultRGB"], 
                             })
                                        
s=15.0
face=[-s,-5,-s, s,-5,-s,-s,-5,s, s,-5,s]
ri.Patch("bilinear",{'P':face})
ri.AttributeEnd()
ri.TransformEnd()
#--------------------------------------------------------------------------------------------

ri.WorldEnd()
ri.End()

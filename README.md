# Modelling and Rendering a pen in Renderman

First project using Python API for RenderManProServer.
The aim is to create a believable pen geometry and render it with proper shading and lighting.

# Repository Structure
*Images: all the .tx texture images used to create the scene
*Shaders: shaders used in the project

# Requirements
Tested on: RenderManProServer (python engine 2.7).

# Execute
*Commands for compiling shaders

  *oslc *.osl: will compile the new generation shaders.
  *shader *.sl: will compile the old .sl shaders.

*Open RenderMan visualization program it

*Execute the scene.py script by typing in the terminal:
  *./scene.py: it executes the python scripts and produces the RIB file
  *render scene.rib: it will send and start rendering the image in the previously opened it program.

# Final Output
![alt text](https://github.com/jroy1992/Renderman/blob/master/pen_Final1.png)

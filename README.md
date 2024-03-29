
A Novel Device for Detecting Objects using Artificial Intelligence and Sound Localization for the Visually Impaired

  My Project goal is to develop a system that can capture an environment using a camera, identify specific objects in the area, and output the recognized objects via sound for the visually impaired. After identifying objects, they will be read to the user using surround sound so that the user can recognize locations of the objects. The system will also be able to read any text found in the image.
  
  I evaluated my project on the following criteria. The entire system should be controlled by one joystick. The system should fit in a box with dimensions of 8’’ x 3’’ x 2’’. The system should be able to function with an on-board battery for 2 hours. The user should be able to identify the direction of objects using surround sound. The system should be able to correctly recognize 85% of objects in the environment. The system should take a maximum of 2 seconds to identify objects in the input.
  
  For the project, I used a Raspberry Pi and the respective camera, a joystick, a MCP3008 ADC, earbuds/headphones, a power switch, and a battery. I first developed the software for object recognition using python and the Yolo-tiny vision engine. I then added the camera so that I could use my own images in the detection. Additionally, a joystick was later added to allow for the user to change the mode of the device. The joystick, with the accompanying ADC, was soldered onto a PCB which connected to pins on the Raspberry Pi. A transparent plastic case was chosen to protect the components while allowing vision of them. 
  
  Utilizing Yolo-tiny for the Raspberry Pi, objects in the scene are identified clearly with bounding boxes. The sound from Yolo was enhanced using ITD to give the appearance of a directional sound source. Additionally, tesseract-ocr is able to recognize text in the scene, albeit with a delay. Optimal filters were used to reduce the runtime and to improve accuracy for the OCR. 
  
  Overall, the device is successful; it is capable of operating in the two modes, Yolo mode and OCR mode, with the user controlling the device.

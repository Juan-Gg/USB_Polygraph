# USB_Polygraph
This is a USB Polygraph, which I designed and built as a classroom project on June 2018. 
The hardware side is pretty simple, an Arduino UNO collects data from some sensors and 
sends it via serial. On the computer, a Python program takes that data and not only graphs 
it, but it also allows the user to save it, manages questions and adds question and answer 
markers to the graphs so results can later be inspected. All results are saved in .txt files.
Two sample files are provided, a questions file and an exam file. The exam file can be opened
and visualized from the Python program.

Find more information here: https://juangg-projects.blogspot.com/2019/06/usb-polygraph.html

Note:
I could not get the polygraph aplication running because pyqtgraph gave some random error when importing it, a workaorund is found here:

https://developercommunity.visualstudio.com/content/problem/1207405/fmod-after-an-update-to-windows-2004-is-causing-a.html

Installing an older version of numpy fixes it: pip install numpy==1.19.3

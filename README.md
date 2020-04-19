# Simple terminal-based PNG or JPG to PDF converter
Simple script written in Python 3.7 to turn png or jpg images to pdf. It allows the user to shrink the created pdf by using an existing installation of Ghostscript. You may need to edit "shrinkpdf.bat" to enter your installation directory of Ghostscript. It is important to keep shrinkpdf.bat in the same directory as ImageToPDF.py, as well as the .exe file included in /dist for Windows users. This executable file should run without any prerequisites.

## External libraries
- img2pdf. Go to https://pypi.org/project/img2pdf/ 
- Pillow. Go to https://pillow.readthedocs.io/en/stable/

## Aditional information
To download Ghostscript: https://www.ghostscript.com/download.html

All credits to http://dcm684.us/wp/2013/10/pdf-shrink/ for his batch script (shrinkpdf.bat)

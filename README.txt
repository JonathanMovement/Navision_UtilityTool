-- Navision Utility Tool --

This is a small application for Business Central and Microsoft Dynamics NAV where you paste a list of values, 
one per line or separated by spaces, and one click turns it into NAV filter syntax.
No more typing | and * by hand.
The app can also read the text from a screenshot.

Download the 64-bit installer from https://github.com/UB-Mannheim/tesseract/wiki, 
rename it exactly into tesseract-ocr-w64-setup.exe  
and copy-paste it into a new folder called OCR_tesseract_installer

When running the app for the first time, clicking on screenshot -> text will automatically run the tesseract installer if it's not installed.
During the installation, under "Additional language data", select Dutch (the app reads both English and Dutch)

In the possible_paths variable from NavisionApp.py (where the app looks for tesseract.exe), 
you can delete the last 2 H: paths, they are my local workstation folder layout:

possible_paths = [
             r"C:\Program Files\Tesseract-OCR\tesseract.exe",
             r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
-            r"H:\Tesseract\tesseract.exe", <-- You can delete this
-            r"H:\Oleg\Tesseract+Navision\tesseract.exe" <-- You can delete this
         ]

Run below command in the terminal before running the script:
pip install -r requirements.txt
Then start the app from inside the project folder or make the executable (paste in terminal):
pip install pyinstaller
pyinstaller --onefile --windowed --name "Navision Utility Tool" --add-data "OCR_tesseract_installer;OCR_tesseract_installer" NavisionApp.py
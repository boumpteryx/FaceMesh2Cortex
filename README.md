# FaceMesh
 
This repository enables to use the FaceMesh model to extract face landmarks around the mouth. It can also be sued to compare those extracted landmarks to those extracted by the cortex system.

![](Antoine_facemesh.png)

## Extract landmarks from a video
run `video_processing.py`
choose the video you want to process
The video will play at processing speed, not at normal speed. you may visually confirm the position of the landmarks. Absent landmarks are replaced with NaNs
if you change the code to put webcam=True, you can have it run on your webcam for fun, nothing is registered.

## compare cortex and FaceMesh
run `GUI.py`
then select the csv file with the cortex landmarks (header and data)
the select the csv file with the FaceMesh dta extracted in the previous step

Choose the landmark to use for analysis. LLx is a good choice.
Left-click on the plot to place markers for trimming. In case of a mistake, right-click to delete previous marker. Please only put two markers. When done, close the plot window. 
Another plot window with the trimmed signal will appear, just for a visual check. Close that window and then select the save file for the cortex trimmed signal and then for the facemesh trimmed signal.

It is not yet possible to align manually the signals, it is done automatically. If auto-alignment fails, please report the case where that happens.
The way the automatic alignment is made consists of taking each landmark/dimension (LLx, Uly, etc) and shifting the signals to get the maximum Pearson correlation. Since different signals have different offsets but should all share the same offsets (video start vs cortex start), the code selects the offset that comes out the most times amongst landmarks/dimensions and keeps it as the ground truth offset.
vertical resizing is done by simply fitting the mean and the standard deviation of cortex (to fit the movements in pixels of FaceMesh to the movement in cm of Cortex).

# Getting Started

## Step 1: Download and Install Anaconda
1. Go to the Anaconda website: [https://www.anaconda.com/products/individual](https://www.anaconda.com/products/individual).
2. Scroll down to the "Anaconda Individual Edition" section.
3. Select the appropriate installer for your operating system (Windows/macOS/Linux) and download it.
4. Once the download is complete, run the installer.
5. Follow the installation wizard's instructions:
   - Choose a destination folder (the default location is recommended).
   - Optionally, select "Add Anaconda to my PATH environment variable" for easier command-line access.
   - Click "Install" to begin the installation.
6. After the installation completes, close the installer.

## Step 2: Clone the FaceMesh GitHub Repository
1. Open PyCharm Community Edition.
2. On the welcome screen, select "Check out from Version Control" and choose "Git".
3. In the "Git Repository URL" field, enter the URL of the FaceMesh GitHub repository.
4. Choose a directory where you want to store the project on your local machine.
5. Click "Clone" to clone the repository.

## Step 3: Create a Virtual Environment with Python 3.7.0 Interpreter
1. After cloning the repository, PyCharm will prompt you to open the project. Click "Yes" to open it.
2. Once the project is open, go to the top menu and select "File" -> "Settings".
3. In the Settings window, navigate to "Project: FaceMesh" -> "Python Interpreter" (or similar).
4. Click on the gear icon on the right and select "Add".
5. In the "Add Python Interpreter" window, choose "Virtual Environment" -> "New Environment".
6. Select the base interpreter as Python 3.7.0 from the drop-down list.
   - If Python 3.7.0 is not listed, you may need to add it as a new interpreter in Anaconda before proceeding.
7. Choose a location for the virtual environment directory or use the default location.
8. Click "OK" to create the virtual environment.

## Step 4: Install Project Requirements from `requirements.txt`
1. In PyCharm, ensure that the FaceMesh project is open.
2. Open the terminal within PyCharm (bottom toolbar or "View" -> "Tool Windows" -> "Terminal").
3. Make sure the terminal is using the correct virtual environment by checking the prompt (it should show the virtual environment name).
4. Run the following command in the terminal to install the project's requirements:
   ```
   pip install -r requirements.txt
   ```
   This command will install all the packages listed in the `requirements.txt` file.
5. Wait for the installation to complete.

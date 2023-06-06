import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from utils import dict_match,butter_lowpass_filter, rescale, leader_offset

fps = 60
down_sample_ratio = 2

def load_explorer():
    # Create the root window
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    # Open the file explorer dialog
    file_path = filedialog.askopenfilename()
    # Check if a file was selected
    root.destroy()
    if file_path:
        return file_path
    else:
        print("No file selected.")
        return

# Cortex data
url_cortex = load_explorer()
data_cortex = pd.read_csv(url_cortex)

# FaceMesh data
url_FaceMesh = load_explorer()
data_facemesh = pd.read_csv(url_FaceMesh)

def option_selected(event=None):
    global landmark_show
    landmark_show = dropdown.get()
    root.destroy()  # Close the tkinter window after option selection

root = tk.Tk()
root.title("Select a Landmark")

landmark_show = None  # Initialize the landmark variable

# Create a dropdown menu
dropdown = tk.StringVar(root)
dropdown.set(list(dict_match.keys())[0])  # Set default value

option_menu = tk.OptionMenu(root, dropdown, *dict_match.keys())
option_menu.pack(pady=10)

# Create a button to confirm the selection
confirm_button = tk.Button(root, text="Confirm", command=option_selected)
confirm_button.pack(pady=5)

# Run the tkinter event loop
root.mainloop()

offset = leader_offset(data_facemesh, data_cortex)
print('finale offset:', offset)

llx, lly, llz = [], [], []
ulx, uly, ulz = [], [], []
lelx, lely, lelz = [], [], []
rlx, rly, rlz = [], [], []
jlx, jly, jlz = [], [], []
jrx, jry, jrz = [], [], []
save_facemesh = {'LLx': llx, 'LLy': lly, 'LLz': llz,
        'ULx': ulx, 'ULy': uly, 'ULz': ulz,
        'LeLx': lelx, 'LeLy': lely, 'LeLz': lelz,
        'RLx': rlx, 'RLy': rly, 'RLz': rlz,
        'JLx': jlx, 'JLy': jly, 'JLz': jlz,
        'JRx': jrx, 'JRy': jry, 'JRz': jrz,
        }
c_llx, c_lly, c_llz = [], [], []
c_ulx, c_uly, c_ulz = [], [], []
c_lelx, c_lely, c_lelz = [], [], []
c_rlx, c_rly, c_rlz = [], [], []
c_jlx, c_jly, c_jlz = [], [], []
c_jrx, c_jry, c_jrz = [], [], []
save_cortex = {'LowerLip_x': c_llx, 'LowerLip_y': c_lly, 'LowerLip_z': c_llz,
        'UpperLip_x': c_ulx, 'UpperLip_y': c_uly, 'UpperLip_z': c_ulz,
        'LeftLip_x': c_lelx, 'LeftLip_y': c_lely, 'LeftLip_z': c_lelz,
        'RightLip_x': c_rlx, 'RightLip_y': c_rly, 'RightLip_z': c_rlz,
        'JawLeft_x': c_jlx, 'JawLeft_y': c_jly, 'JawLeft_z': c_jlz,
        'JawRight_x': c_jrx, 'JawRight_y': c_jry, 'JawRight_z': c_jrz,
        }
for landmark in dict_match.keys():
    # create list
    for i in range(len(data_facemesh[landmark])):
        save_facemesh[landmark].append(-data_facemesh[landmark][i])
    # cortex value
    landmark_cortex = dict_match[landmark]
    for i in range(len(data_cortex[landmark_cortex])):
        if i % down_sample_ratio == 0:
            save_cortex[landmark_cortex].append(data_cortex[landmark_cortex][i])
    # rescale
    save_facemesh[landmark], _ = rescale(save_cortex[landmark_cortex], save_facemesh[landmark], leader_offset=True, set_offset=offset)
    # filter
    save_facemesh[landmark] = butter_lowpass_filter(save_facemesh[landmark], 12, fps, order=5)

y_facemesh = save_facemesh[landmark_show]
y_cortex = save_cortex[dict_match[landmark_show]][:len(y_facemesh)]
x = np.linspace(0, len(y_facemesh), len(y_facemesh))

# Variables to store marker positions
markers = []

# Function to handle mouse click events
def onclick(event):
    if event.button == 1:  # Left mouse button
        markers.append(event.xdata)
        plt.axvline(event.xdata, color='r')  # Draw a vertical line at marker position
        plt.draw()
    elif event.button == 3 and markers:  # Right mouse button
        plt.axvline(markers.pop(), color='b')  # Remove the last marker and revert to previous state
        plt.draw()

# Plotting the initial signal
plt.figure(figsize=(17, 5))
plt.plot(x, y_facemesh, label="FaceMesh")
plt.plot(x, y_cortex, label="Cortex")
plt.title('Signal Trimming')
plt.xlabel('frames')
plt.ylabel(landmark_show)
plt.legend()

# Attach the onclick event handler
cid = plt.gcf().canvas.mpl_connect('button_press_event', onclick)

# Display the plot
plt.show()

# Sort and trim the signal based on marker positions
markers.sort()
if len(markers) >= 2:
    start_index = int(np.searchsorted(x, markers[0]))
    end_index = int(np.searchsorted(x, markers[1]))
    trimmed_x = x[start_index:end_index]
    trimmed_y = y_facemesh[start_index:end_index]
    trimmed_cortex = y_cortex[start_index:end_index]
    # Plot the trimmed sample in a new window
    plt.plot(trimmed_x, trimmed_y, label="FaceMesh")
    plt.plot(trimmed_x, trimmed_cortex, label="Cortex")
    plt.title('Trimmed Signal')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
else:
    print("At least two markers are needed to trim the signal.")

for landmark in dict_match.keys():
    # trim
    save_facemesh[landmark] = save_facemesh[landmark][start_index:end_index]
    save_cortex[dict_match[landmark]] = save_cortex[dict_match[landmark]][start_index:end_index]

def save_explorer():
    root = tk.Tk() # Create the root window
    root.withdraw()  # Hide the main tkinter window
    # Open file dialog for save location selection
    save_path = filedialog.asksaveasfilename()
    root.destroy()
    # Check if a file path was selected
    if save_path:
        print("Selected file path:", save_path)
    else:
        print("No file path selected.")

trimmed_facemesh_df = pd.DataFrame(save_facemesh)
trimmed_facemesh_df.to_csv(save_explorer(), index=False)

trimmed_cortex_df = pd.DataFrame(save_cortex)
trimmed_cortex_df.to_csv(save_explorer(), index=False)

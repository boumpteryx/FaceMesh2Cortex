import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def align_time_series(cortex, facemesh, shift):
    shifted_facemesh = facemesh.copy()
    shifted_facemesh['Time'] = facemesh['Time'] + shift
    return shifted_facemesh

def plot_time_series(cortex, facemesh, markers):
    fig, ax = plt.subplots()
    ax.plot(cortex['Time'], cortex['Data'], label='Cortex')
    ax.plot(facemesh['Time'], facemesh['Data'], label='Facemesh')
    ax.set_xlabel('Time')
    ax.set_ylabel('Data')

    # Add vertical markers
    for marker in markers:
        ax.axvline(x=marker, color='red', linestyle='--')

    ax.legend()
    st.pyplot(fig)

def main():
    # Generate sample data (replace with your own data)
    cortex_data = {'Time': [0, 1, 2, 3, 4], 'Data': [1, 2, 3, 4, 5]}
    facemesh_data = {'Time': [0, 1, 2, 3, 4], 'Data': [2, 4, 6, 8, 10]}

    cortex = pd.DataFrame(cortex_data)
    facemesh = pd.DataFrame(facemesh_data)

    # Title and description
    st.title('Time Series Alignment and Trimming')
    st.write('Move the Facemesh time series left or right compared to Cortex.')

    # Sidebar controls
    shift = st.slider('Shift Facemesh', min_value=-10, max_value=10, value=0)

    # Align time series
    shifted_facemesh = align_time_series(cortex, facemesh, shift)

    # Plot time series and markers
    markers = []
    plot_time_series(cortex, shifted_facemesh, markers)

    # Handle mouse clicks on the plot
    if st.button('Save'):
        if len(markers) >= 2:
            # Find the indices corresponding to the markers
            left_marker_idx = markers[0]
            right_marker_idx = markers[1]

            # Trim the signals between the markers
            trimmed_cortex = cortex.iloc[left_marker_idx:right_marker_idx]
            trimmed_facemesh = shifted_facemesh.iloc[left_marker_idx:right_marker_idx]

            # Save the trimmed signals or perform further processing
            st.write('Trimmed Cortex Data:')
            st.write(trimmed_cortex)

            st.write('Trimmed Facemesh Data:')
            st.write(trimmed_facemesh)
        else:
            st.write('Please place both left and right markers before saving.')

        # Handle button click to delete the last marker
    if st.button('Delete Last Marker'):
        if markers:
            markers.pop()

        # Get mouse click event on the plot
    event = st.button('Add Marker')

    # Process mouse click events
    if event and len(markers) < 2:
        x = st.session_state.mousePointX
        markers.append(x)

    # Plot time series and markers
    plot_time_series(cortex, shifted_facemesh, markers)

if __name__ == '__main__':
    main()

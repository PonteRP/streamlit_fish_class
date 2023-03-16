# Imports
import streamlit as st
import tempfile
#import cv2
#from pathlib import Path
import requests
import pandas as pd
from matplotlib import pyplot as plt


def main():

    # Write a page title
    st.title('A.I. for fish monitoring! 🐟')

    # Subheader
    st.subheader('A.I. tool to evaluate fish populations crossing dams')
    # Text
    st.text('The tool searches for the following species: Bleek, Eel, Mullet, Sunfish, Others')
    # Using st.write
    #st.write('You can upload a video file in .mp4 or .mov format to a max size of 200MB and the tool will process it and output both a csv file with the species count as well as video with the detected species. The species count is merely a baseline estimation that takes as a proxy the max number of individuals in a single frame for a specific time frame')

    st.sidebar.title('Settings')
    st.sidebar.markdown('---')
    confidence = st.sidebar.slider('Confidence', min_value=0.0, max_value=1.0, value=0.25)
    st.sidebar.markdown('---')

    custom_classes = st.sidebar.checkbox('Use Custom Classes')
    assigned_classes_id = []
    names = ['Bleak', 'Eel', 'Mullet', 'Other', 'Sunfish']
    if custom_classes:
        assigned_class = st.sidebar.multiselect('Select The Custom Classes', names, default='Mullet')
        for each in assigned_class:
            assigned_classes_id.append(names.index(each))

    st.sidebar.markdown('---')

    uploaded = False  # track whether a video has been uploaded

    ###uploading our video:
    video_file_buffer = st.sidebar.file_uploader("Upload a video", type=["mp4", "mov", "avi", "asf", "m4v"])


    # Create a submit button that will submit a request to the API once the video is uploaded
    if video_file_buffer is not None:
        uploaded = True
        st.sidebar.video(video_file_buffer)

        if st.button("Submit", key=1):
            with st.empty():
                st.write('Processing video...')
                files = {'file' : video_file_buffer}
                result = requests.post('https://fishing-nbwxp2xc2a-ew.a.run.app/predict', files=files, headers={'confidence': str(confidence)}, stream=True)


                st.write('Video processing complete!')

            fish_str = result.headers.get('X-fishes')
            #st.write(f'results : {result.content}')
             # Display the processed video in the main part of the page
            #stframe.video(result.content)

            fish_dict = dict((a.strip(), b.strip())
                for a, b in (element.split(':')
                            for element in fish_str.split(', ')))
            #st.markdown(fish_dict.items())


            ## Display the results of the fish count in a table
            df = pd.DataFrame(list(fish_dict.items()), columns=['Fish Type', 'Count'])
            df['Fish Type'] = df['Fish Type'].str.replace("'", "")
            df['Count'] = df['Count'].str.replace("'", "")
            df['Count'] = df['Count'].str.replace("}", "")
            df = df.iloc[1:]
            df['Count'] = df['Count'].astype(int)

            # Display the table
            st.table(df)

            st.video(result.content)

            color_palette = ['#1b4965', '#2c728e', '#3f9cb3', '#80ced7', '#b8d9db']

            fig, ax = plt.subplots(facecolor='black')
            ax.barh(df['Fish Type'], df['Count'], height=0.5, color=color_palette)
            ax.set_title('Fish Count by Type', fontsize=16, color='white')
            ax.set_xlabel('Fish Type', fontsize=12, color='white')
            ax.set_ylabel('Count', fontsize=12, color='white')
            ax.tick_params(axis='both', labelsize=10, colors='white')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            st.pyplot(fig)

            #content = result.content



    #Display Demo video
    DEMO_VIDEO = 'tool_overview.mp4'  # name of demo video
    tfflie = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
    vid = cv2.VideoCapture(DEMO_VIDEO)
    tfflie.name = DEMO_VIDEO
    dem_vid = open(tfflie.name, 'rb')
    demo_bytes = dem_vid.read()
    st.sidebar.text("Tool Overview")
    st.sidebar.video(demo_bytes)


    stframe = st.empty()
    st.markdown('---')
    st.sidebar.markdown('---')


if __name__ == '__main__':
    try:
        main()
    except:
        SystemExit()

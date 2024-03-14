import streamlit as st
import cv2
import requests
import json
import numpy as np
from PIL import Image as im
from lip_detect.solo_vid import lip_detect
import imageio
import base64

##########################################
##  Title, Tabs, and Sidebar            ##
##########################################
col1, col2 = st.columns([3,8])
with col1:
    st.image("https://raw.githubusercontent.com/ecem/lip_translate_front/master/logo.png", use_column_width = True)

with col2:
    st.title("LIP TRANSLATE")
    st.markdown('''##### <span style="color:black">Turning silence into words</span>
                ''', unsafe_allow_html=True)

tab_overview, tab_ourmodel, tab_aboutus = st.tabs(["OVERVIEW",
                                                    "OUR MODEL",
                                                              "ABOUT US"])


#col1, col2 = st.columns([1, 3])

# Display the image in the first column
#with col1:
#st.image("lips_final2.png", width=200)

# Display the title in the second column
#with col2:
#st.title("Lip Reader")

with tab_overview:
    st.markdown('''<div style="text-align: justify;">

Welcome to Lip Translate, where cutting-edge data science meets the art of communication! Our groundbreaking project utilizes state-of-the-art neural networks to decipher speech through the intricate movements of the lips with unparalleled accuracy.
    </div>''', unsafe_allow_html=True)
    ""
    st.markdown('''<div style="text-align: justify;">
    In our increasingly interconnected world, communication takes many forms, and for individuals with hearing impairments or in noisy environments, visual cues like lip movements play a crucial role in understanding speech.
    Leveraging the advancements in machine learning, particularly in the realm of computer vision, we introduce a groundbreaking lip reading model.
    This model harnesses the power of deep learning algorithms to decode spoken language from visual cues, paving the way for more inclusive and accessible communication technologies.
    </div>''', unsafe_allow_html=True)
    ""
    st.image('200w.gif',  use_column_width=True)

    st.markdown(" #### Analysing data from real world")
    st.markdown('''<div style="text-align: justify;">
Our model was trained on nearly 2000 videos from 15 individuals, carefully selected from an initial dataset of 1000 videos spanning 34 individuals. Through meticulous curation and rigorous analysis, we refined this dataset to capture the nuanced lip movements of our chosen subjects.
This curated dataset formed the foundation for the development of our advanced machine learning model. By prioritizing quality over quantity, we crafted a robust and versatile model capable of accurately interpreting diverse lip movements, facilitating improved communication and understanding.
    </div>''', unsafe_allow_html=True)
    ""

    st.markdown('''<div style="text-align: justify;">
    The model uses a combination of convolutional and recurrent neural networks to interpret lip movements from videos. Essentially, it analyzes sequences of images showing lip movements to predict what words are being spoken.
    By integrating Dlib, a popular library for facial landmark detection, we've enhanced the capabilities of our lip reading system. Dlib helps identify key points on the face, such as the corners of the mouth, which are crucial for accurately tracking lip movements.
    </div>''', unsafe_allow_html=True)
    ""


#########################################
## RACES TAB                           ##
#########################################

with tab_ourmodel:

    st.markdown('''## <span style="color:black">How It Works</span>
            ''', unsafe_allow_html=True)
    "Below, we're sending a video into the model to get back a lip reading prediction... Let's see how well it does :)"

    video_file = st.file_uploader("", type=["mp4", "mov"])
    final_request = None
# Display video if a file is selected
    if video_file is not None:
        st.video(video_file)
        if video_file is not None and final_request is None:
            giff
        vid = video_file.name
        with open(vid, mode='wb') as f:
            f.write(video_file.read()) # save video to disk

        #st.write('---- saved to disk ----')

        vidcap = cv2.VideoCapture(vid)
        success = True
        i = 0

        #st.write('---- video capturing ----')

        frames = []
        while success:
            # while vidcap.isOpened():
        # while i <= 10:
            success, frame = vidcap.read()
            if frame is not None:
                lips = lip_detect(np.array(im.fromarray(frame).convert('L')))
                frames.append(lips.tolist())
                i += 1
                if i % 10 == 0:
                    response = requests.post("https://lip-reader-docker-zn34um6luq-nw.a.run.app/send_frames/", json=json.dumps(frames))
                    if response.ok:
                            frames = []
                    #else:
                        #st.write(response)
                        #st.write(f'---- frame {i} complete {str(response)} ----')

        vidcap.release()

        response = requests.post("https://lip-reader-docker-zn34um6luq-nw.a.run.app/send_frames/", json=json.dumps(frames))

        #with open("bin_day_1.", "w") as outfile:
            #outfile.write(json.dumps(frames))
        #np.savez("please_read_it_now.npz", frames)


        #st.write(response)

        st.image(lips)

        #st.write('---- all frames captured ----')

        # AWAITING CORRECT API LINK
        result = requests.get("https://lip-reader-docker-zn34um6luq-nw.a.run.app/predict/")
        final_request = result.ok
        #st.write('---- post request sent ----')

        #st.write(response)
        #st.write(type(response.json()))
        st.write(f"Prediction: {result.json()['prediction']}")

        if result.ok:
            st.balloons()

with tab_aboutus:
  column1, column2 = st.columns([3,9])
  with column1:
        ""
        st.image("lips_girish.png", use_column_width = True)
        ""
        ""
        st.image("lips_alessia.png", use_column_width = True)
        ""
        ""
        ""
        st.image("lips_mathilda.png", use_column_width = True)
        ""
        ""
        ""
        st.image("lips_ecem.png", use_column_width = True)
        ""
        ""
        ""

  with column2:
    ""
    st.subheader("GIRISH JOSHI", divider = "grey")
    st.markdown('''<span style="text-align: center;">
    Project Leader & Data Scientist
    </div>
    <br>
    <a href="https://github.com/girishgautam">Github</a>''',  unsafe_allow_html=True)
    ""
    ""
    ""
    ""
    st.subheader("ALESSIA STRONI", divider = "grey")
    st.markdown('''<span style="text-align: center;">
    Data Scientist
    </div>
    <br>
    <a href="https://github.com/a6677654s880">Github</a>''', unsafe_allow_html=True)
    ""
    ""
    ""
    ""
    st.subheader("MATHILDA WESTON", divider = "grey")
    st.markdown('''<span style="text-align: center;">
    Data Scientist
    </div>
    <br>
    <a href="https://github.com/mathildaweston">Github</a>''', unsafe_allow_html=True)
    ""
    ""
    ""
    ""
    st.subheader("ECEM KOCASLAN", divider = "grey")
    st.markdown(f'''<span style="text-align: center;">
    Data Scientist
    </div>
    <br>
    <a href="https://github.com/ecemkocaslan">Github</a>''' , unsafe_allow_html=True)
    ""
    ""
    ""
    ""

import streamlit as st
from langchain_helper import few_shot_query_selector
import os
import time

# Path to the folder containing images
folder_path = "src/images"

db_chain, db_info = few_shot_query_selector()


# Function to list image files in a folder
def list_images(folder_path):
    files = os.listdir(folder_path)
    image_files = [
        file for file in files if file.endswith((".jpg", ".jpeg", ".png", ".gif"))
    ]
    return image_files


st.title("Data Base Chat Bot :robot_face:")


image_files = list_images(folder_path)
for image_file in image_files:
    image_name = image_file.split(".")[0]
    st.header(f"{image_name} Table Info")
    st.image(
        os.path.join(folder_path, image_file), caption=image_file, use_column_width=True
    )

question = st.text_input(label="Ask the Robo !")
button_click = st.button("Submit")

if question and button_click:
    alert = st.success(
        "Your Question Submitted!",
    )
    time.sleep(3)  # Wait for 3 seconds
    alert.empty()

    result = db_chain.run(question)
    st.header("Answer:")
    st.write(result)

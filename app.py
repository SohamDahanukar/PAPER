import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables
from PIL import Image

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize our Streamlit app frontend setup
st.set_page_config(page_title="Gemini BloodCell Classification App")
st.header("Gemini BloodCell Classification App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the blood cell type")

input_prompt = """
You are an expert in hematology, specializing in the classification of white blood cells.Analyze the provided image and classify it into one of the following white blood cell types:
 Eosinophil, Lymphocyte, Monocyte, or Neutrophil. Use the detailed characteristics below to guide your analysis.
 Pay special attention to the features that can be identified even in grainy, low-quality images.

Eosinophils-
Nucleus: Bi-lobed, often resembling a pair of sunglasses. Even in low-quality images, look for the distinct bi-lobed structure.
Cytoplasm: Contains large, red-orange granules that are usually visible even in grainy images due to their size and color contrast.
Function: Combat parasitic infections and participate in allergic reactions by releasing enzymes that break down parasites and modulate inflammation.
Appearance: Similar in size to neutrophils but distinguished by their bright granules. The granules' color and size make them identifiable in low-quality images.

Lymphocytes-
Nucleus: Large, round, and occupies most of the cell, leaving a thin rim of cytoplasm. In low-quality images, focus on the large, dark nucleus and the minimal cytoplasm.
Cytoplasm: Thin, pale blue rim around the nucleus. This can be challenging to see in low-quality images, so prioritize the nucleus size and shape.
Function:
B cells: Produce antibodies that target specific pathogens.
T cells: Helper T cells (CD4+), Cytotoxic T cells (CD8+), and Regulatory T cells.
Natural Killer (NK) cells: Provide a rapid response to virally infected cells and tumor formation.
Appearance:
Small lymphocytes: Feature a dense nucleus with minimal cytoplasm.
Large lymphocytes: Have a more substantial amount of cytoplasm and may be activated lymphocytes or NK cells.
The nucleus is typically very dark (dense chromatin) and round, occupying most of the cell's volume. In low-quality images, the prominent dark nucleus is key.

Monocytes-
Nucleus: Kidney-shaped or folded, often described as horseshoe-shaped. This unique shape can still be identified in lower quality images.
Cytoplasm: Abundant, grayish-blue. In low-quality images, look for the large cell size and distinctive nucleus shape.
Function: Differentiate into macrophages and dendritic cells to break down bacteria and present antigens.
Appearance: Largest white blood cells with a distinctive nucleus shape. Their large size helps identify them in grainy images.

Neutrophils-
Nucleus: Multi-lobed (2-5 lobes), segmented or polymorphonuclear. In low-quality images, focus on the segmented nature of the nucleus.
Cytoplasm: Contains fine granules that stain light pink or purple. These granules may be less visible in low-quality images, so rely on the nucleus.
Function: Respond to bacterial infections through phagocytosis.
Appearance: Larger than red blood cells with a distinctive lobed nucleus. The nucleus structure is the key feature in grainy images.

Instructions-
Analyze the uploaded image and identify the type of white blood cell present.
Provide the following details:
Type of white blood cell: [Type]
Explanation: [Detailed reasoning based on nucleus, cytoplasm, function, and appearance]
Model accuracy: [Accuracy percentage in detecting the image]
"""

if submit and uploaded_file is not None:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        if response:
            st.header("The Response is")
            st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")
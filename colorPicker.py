import streamlit as st
import numpy as np
import cv2
from sklearn.cluster import KMeans

# Fungsi untuk ekstraksi warna dominan
def extract_dominant_colors(image, k=5):
    img = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(img)
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    sorted_indices = np.argsort(counts)[::-1]
    dominant_colors = colors[sorted_indices]
    return dominant_colors

# CSS untuk mempercantik tampilan
st.markdown(
    """
    <style>
    .upload-text {
        font-size: 18px;
        color: #777;
        margin-top: 20px;
    }
    .color-block {
        display: inline-block;
        width: 80px;
        height: 80px;
        margin: 20px;
        border-radius: 50%;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .color-block:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.3);
    }
    .color-label {
        margin-top: 10px;
        font-weight: bold;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        color: #222;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul aplikasi
st.title('Dominant Color Picker')

# Unggah gambar
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    # Baca gambar
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Konversi gambar dari BGR ke RGB untuk tampilan yang benar
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Tampilkan gambar yang diunggah
    st.image(image_rgb, caption='Uploaded Image.', use_column_width=True)
    st.write("")

    # Ekstraksi warna dominan
    st.write("Extracting dominant colors...")
    dominant_colors = extract_dominant_colors(image_rgb, k=5)

    # Tampilkan warna dominan
    st.write("Dominant colors:")
    cols = st.columns(5)  # Membuat kolom untuk layout yang lebih baik
    for i, color in enumerate(dominant_colors):
        color_hex = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
        with cols[i]:
            st.markdown(
                f'<div class="color-block" style="background-color: rgb({color[0]}, {color[1]}, {color[2]});"></div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div class="color-label">RGB: {color}<br>HEX: {color_hex}</div>', unsafe_allow_html=True)
else:
    st.markdown('<p class="upload-text">Choose a JPG, JPEG, or PNG file to get started.</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

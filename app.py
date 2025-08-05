import streamlit as st
import cv2
import time
from src.video_stream import VideoStream
from src.detector import Detector
import src.config as config

st.set_page_config(page_title="CCTV AI Pipeline", layout="wide")
st.title("📹 CCTV AI Pipeline - Real-time Detection & Tracking")

st.sidebar.header("Tentang Proyek")
st.sidebar.info(
    "Pipeline ini mendeteksi dan melacak objek (orang) secara real-time "
    "dari sumber video. Dibangun dengan arsitektur modular dan tangguh "
    "terhadap gangguan koneksi"
)

if 'is_running' not in st.session_state:
    st.session_state.is_running = False
    
start_button = st.sidebar.button("Start Pipeline", type="primary", use_container_width=True)
stop_button = st.sidebar.button("Stop Pipeline", use_container_width=True)

if start_button:
    st.session_state.is_running = True
if stop_button:
    st.session_state.is_running = False
    st.info("Pipeline dihentikan")
    st.stop()

if st.session_state.is_running:
    image_placeholder = st.empty()
    
    with st.spinner("Memuat model dan menghubungkan ke stream..."):
        detector = Detector()
        video_stream = VideoStream(config.RTSP_URL)
        
    st.success("Pipeline berhasil dimulai")
    
    frame_counter = 0
    annotated_frame = None
    
    while st.session_state.is_running:
        ret, frame = video_stream.read()
        
        if not ret:
            st.warning("Stream terputus atau video telah selesai. Mencoba menyambung ulang...")
            time.sleep(config.RECONNECT_DELAY_SECONDS)
            continue
          
        frame_counter += 1  

        if frame_counter % config.FRAME_SKIP == 0:
            annotated_frame = detector.detect_and_track(frame)
        
        display_frame = annotated_frame if annotated_frame is not None else frame
        
        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        
        image_placeholder.image(frame_rgb, caption=f"Frame #{frame_counter}", use_container_width=True)
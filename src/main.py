import cv2
import config
from detector import Detector
from video_stream import VideoStream

def run():
    detector = Detector()
    
    video_stream = VideoStream(config.RTSP_URL)
    
    print("Memulai pipeline...")
    
    while True:
        ret, frame = video_stream.read()
        if not ret:
            print("Tidak ada frame, menunggu koneksi ulang...")
            break
        
        annotated_frame = detector.detect_and_track(frame)
        
        cv2.imshow("Pipeline CCTV - Robust Conncetion", annotated_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_stream.release()
    cv2.destroyAllWindows()
    print("Program dihentikan")

if __name__ == "__main__":
    run()
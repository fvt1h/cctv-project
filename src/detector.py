from ultralytics import YOLO
import src.config as config

class Detector:
    def __init__(self,model_path=config.MODEL_PATH):
        """
        Inisialisasi detector dengan model YOLO
        """
        self.model = YOLO(model_path)
        print(f"Model detector dimuat dari {model_path}")
        
    def detect_and_track(self, frame):
        """
        Menerima sebuah fraame, melakukan deteksi dan tracking,
        lalu mengembalikan frmae yang sudah dianotasi
        
        Args:
            frame: Frame video dari OpenCV
            
        Returns:
            annotated_frame: Frame yang sudah digambari bounding box dan ID
        """
        
        result = self.model.track(
            frame,
            persist=True,
            classes=[0],
            tracker="bytetrack.yaml",
            verbose=False
            )
        
        annotated_frame = result[0].plot()
        
        return annotated_frame
        
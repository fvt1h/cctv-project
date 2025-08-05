import cv2
import time
import src.config as config

class VideoStream:
    def __init__(self, stream_url):
        """
        Inisialisasi stream video
        Args:
            stream_url (str): URL dari RTSP stream atau path ke file video
        """
        self.stream_url = stream_url
        self.cap = None
        self.connect()
    
    def connect(self):
        """Mencoba terhubung atau menyambung ulang ke stream video"""
        print(f"Mencoba mengubungkan ke stream di {self.stream_url}...")
        self.cap = cv2.VideoCapture(self.stream_url)
        
        if not self.cap.isOpened():
            print(f"gagal terhubung. akan mencoba lagi dalam {config.RECONNECT_DELAY_SECONDS} detik")
            self.cap = None
        else:
            print("Berhasil terhubung ke stream")
    
    def read(self):
        """
        Membaca frame dari stream. Jika stream terputus, akan mencoba menyambung ulang
        Returns:
            (bool, frame): Tuple berisi status (True/False) dan frame video
        """
        if self.cap is None or not self.cap.isOpened():
            time.sleep(config.RECONNECT_DELAY_SECONDS)
            self.connect()
            if self.cap is None:
                return False, None
            
        ret, frame = self.cap.read()
            
        if not ret:
            print("Stream terputus atau video selesai")
            self.release()
            return False, None
        
        return True, frame
    
    def release(self):
        """Melepaskan resource VideoCapture"""
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
            
        
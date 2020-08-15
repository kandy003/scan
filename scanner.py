import cv2
import numpy as np
from pyzbar.pyzbar import decode
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton



class ScannerApp(MDApp):

    def build(self):
        screen=Screen()
        btn=MDRectangleFlatButton(text='Scan',
                         pos_hint={'center_x':0.5,'center_y':0.5},
                                  on_release=self.scan)
        screen.add_widget(btn)
        return screen
    def scan(self,obj):
        cap = cv2.VideoCapture(0)
        close_button = MDFlatButton(text='close',
                                    on_release=self.close_dialog)
        self.dialog = MDDialog(buttons=[close_button])
        cap.set(3, 640)
        cap.set(4, 480)


        while True:
            sucess, img = cap.read()
            for barcode in decode(img):
                mydata = barcode.data.decode('utf-8')
                print(mydata)
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(img, [pts], True, (255, 0, 255), 5)
                pts2 = barcode.rect
                cv2.putText(img, mydata, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)

            cv2.imshow('Result', img)
            cv2.waitKey(10)


    def close_dialog(self,obj):
        self.dialog.dismiss()



ScannerApp().run()

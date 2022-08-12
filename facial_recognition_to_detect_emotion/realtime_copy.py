import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model

facedata = "haarcascade_frontalface_default.xml"
        
cascade = cv2.CascadeClassifier(facedata)

model = load_model('model_weights.h5')

def live_user_emotion():
    cap=cv2.VideoCapture(0)  
        
    while cap.isOpened():  
        ret,test_img=cap.read()# captures frame and returns boolean value and captured image  
        if not ret:  
            continue  
        gray_img= cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)  
        
        faces_detected = cascade.detectMultiScale(gray_img)  
        
        for (x,y,w,h) in faces_detected:  
            cv2.rectangle(test_img,(x,y),(x+w,y+h),(0,255,255),thickness=2)  
            roi_gray=gray_img[y:y+w,x:x+h]  #cropping region of interest i.e. face area from  image 
            roi_gray=cv2.resize(roi_gray,(48,48))
                
            if np.sum([roi_gray])!=0:
                img_pixels = roi_gray.astype('float')/255
                img_pixels = tf.keras.utils.img_to_array(img_pixels)
                img_pixels = np.expand_dims(img_pixels, axis = 0)
                    
                predictions = model.predict(img_pixels) 
        
                #find max indexed array  
                max_index = np.argmax(predictions[0])  
        
                emotions = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')  
                predicted_emotion = emotions[max_index]
                predicted_emotion1 = emotions[max_index]
                #print("predicted_emotion:",predicted_emotion) 
            
                cv2.putText(test_img, predicted_emotion, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            else:
                cv2.putText(test_img, 'No Faces', (30,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)  
        
        cap.release()  
        cv2.destroyAllWindows
        return predicted_emotion, predicted_emotion1

if __name__=='__main__':
    live_user_emotion=live_user_emotion()
    print("Emotion:",live_user_emotion[0])
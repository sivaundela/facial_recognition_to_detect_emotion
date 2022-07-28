import matplotlib.pyplot as plt
import numpy as np
import cv2
import base64

def emotion_analysis(emotions):
    objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, emotions, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('percentage')
    plt.title('emotion')
    res=(max(emotions))
    j=0
    for i in emotions:
        if(i==res) : 
            break
        else : 
            j=j+1
    Emotion=str(objects[j])
    print('Emotion Detected : ' + Emotion)
    print('Accuracy : '+ str(res*100))
    return Emotion.accuracy

def facecrop(image):
    image = image[23:]
    facedata = "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(facedata)
    img_b64decode = base64.b64decode(image) # base64 decoding
    img_array = np.fromstring(img_b64decode,np.uint8) # convert np sequence
    img=cv2.imdecode(img_array,cv2.COLOR_BGR2RGB) # Convert Opencv format
    try:
        minisize = (img.shape[1],img.shape[0])
        miniframe = cv2.resize(img, minisize)
        faces = cascade.detectMultiScale(miniframe)
        print(faces)
        for f in faces:
            x, y, w, h = [ v for v in f ]
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            sub_face = img[y:y+h, x:x+w]
            cv2.imwrite('capture.jpg', sub_face)
            #print ("Writing: " + image)
    except Exception as e:
        print (e)
        #cv2.imshow(image, img)
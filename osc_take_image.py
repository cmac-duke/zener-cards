import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications
from keras.utils.np_utils import to_categorical
import math
import cv2
from pythonosc import osc_message_builder
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1",12000)

top_model_weights_path = 'bottleneck_fc_model.h5'
cap = cv2.VideoCapture(0)
class_dictionary = np.load('class_indices.npy').item()
num_classes = len(class_dictionary)
print("I'm working...")
model2 = load_model('./cardsfinal.h5')
image = cv2.imread("larger_image.jpg", -1)

while(True):
    # load the class_indices saved in the earlier step
    ret,frame = cap.read()
    img = cv2.resize(frame, (224, 224))
    image = img_to_array(img)

    # important! otherwise the predictions will be '0'
    image = image / 255
    image = np.expand_dims(image, axis=0)
    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    # get the bottleneck prediction from the pre-trained VGG16 model
    bottleneck_prediction = model.predict(image)

    # build top model
    #model = Sequential()
    #model.add(Flatten(input_shape=bottleneck_prediction.shape[1:]))
    #model.add(Dense(256, activation='relu'))
    #model.add(Dropout(0.5))
    #model.add(Dense(num_classes, activation='sigmoid'))
    #model.load_weights(top_model_weights_path)

    # use the bottleneck prediction on the top model to get the final
    # classification
    class_predicted = model2.predict_classes(bottleneck_prediction)

    probabilities = model2.predict_proba(bottleneck_prediction)

    inID = class_predicted[0]

    inv_map = {v: k for k, v in class_dictionary.items()}

    label = inv_map[inID]

    # get the prediction label
    print("Image ID: {}, Label: {}".format(inID, label))
    print("Probability: {}".format(probabilities))

    # display the predictions with the image
    cv2.putText(frame, "Predicted: {}".format(label), (10, 30),
                cv2.FONT_HERSHEY_PLAIN, 1.5, (43, 99, 255), 2)

    client.send_message("/filter", "{}".format(label))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


predict()
cv2.destroyAllWindows()
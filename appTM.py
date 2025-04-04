from keras.models import load_model  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("models/keras_model.h5", compile=False)

# Load the labels
class_names = open("models/labels.txt", "r").readlines()

# CAMERA can be 0 or 1 based on default camera of your computer
camera = cv2.VideoCapture(0)

while True:
    # Grab the webcamera's image.
    ret, image = camera.read()

    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make a copy of the image to display text
    display_image = image.copy()

    # Double the size of the display image (adjust dimensions as needed)
    display_image = cv2.resize(display_image, (700, 700), interpolation=cv2.INTER_LINEAR)

    # Make the image a numpy array and reshape it to the models input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predicts the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Prepare text to display
    text = f"Class: {class_name[2:].strip()} | Confidence: {np.round(confidence_score * 100):.0f}%"

    # Overlay the text on the image
    cv2.putText(display_image, text, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (0, 255, 0), 3)

    # Show the image in a window
    cv2.imshow("Webcam Image", display_image)

    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break

camera.release()
cv2.destroyAllWindows()

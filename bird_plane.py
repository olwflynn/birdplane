
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model, Sequential
from PIL import Image

def bird_plane_evaluate(image_file):
    model_vgg16 = load_model('vgg16_conv_150pixels.h5')
    model_connected = load_model('bird_plane_connectedontopvgg16.h5')
    #combine vgg16 conv layers with connected model
    model = Sequential()
    model.add(model_vgg16)
    model.add(model_connected)

    img = load_img(image_file)
    width = 150
    height = 150
    img_resized = img.resize((width, height), Image.ANTIALIAS)
    x = img_to_array(img_resized)
    x = x.reshape(1,150,150,3)
    print 'predicting...'
    preds = model.predict_classes(x, verbose=0)
    preds_prob = model.predict_proba(x)

    preds_list=[]
    for element in preds:
        if element <0.5:
            preds_list.append('bird')
        else:
            preds_list.append('plane')

    print preds_prob
    return ("ITS A %s") % (str(preds_list[0]).upper())
from argparse import ArgumentParser
import os, json
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model, Sequential
import pandas as pd
from gooey import Gooey, GooeyParser
from PIL import Image


@Gooey(program_name="Is it a Bird or a Plane! (VGG16)")

def parse_args():
    """ Use ArgParser to build up the arguments we will use in our script
    Save the arguments in a default json file so that we can retrieve them
    every time we run the script.
    """
    stored_args = {}
    # get the script name without the extension & use it to build up
    # the json filename
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    # Read in the prior arguments as a dictionary
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)

    parser = GooeyParser(description='Is it a Bird or a Plane! (VGG16)')
    parser.add_argument('image_file',
                            action='store',
                            widget= 'FileChooser',
                            help="Source image")

    parser.add_argument('output_directory',
                            action='store',
                            help="Output path/filename to save result [bird/plane]")

    args = parser.parse_args()

    # Store the values of the arguments so we have them next time we run
    with open(args_file, 'w') as data_file:
        # Using vars(args) returns the data as a dictionary
        json.dump(vars(args), data_file)
    return args

if __name__ == '__main__':
    conf = parse_args()
    model_vgg16 = load_model('vgg16_conv_150pixels.h5')
    model_connected = load_model('bird_plane_connectedontopvgg16.h5')

    #combine vgg16 conv layers with connected model
    model = Sequential()
    model.add(model_vgg16)
    model.add(model_connected)

    img = load_img(conf.image_file)
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

    predictions = {'predictions': preds_list}

    pred_df = pd.DataFrame(predictions)
    print 'saving to csv'
    pred_df.to_csv(conf.output_directory)
    print preds_prob
    print("ITS A %s") % (str(preds_list[0]).upper())

    #make sure to use "pythonw" in terminal as opposed to python
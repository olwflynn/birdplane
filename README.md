# birdplane
Image recognition bird plane project

An exploration into Deep Learning ----

Started a project hoping to detect whether an input image is a bird or plane inspired by David Newman and Robert Benton’s bookbased on the comic Superman. The technical discussion is outside the scope of this post but for those interested we used Keras (running Tensorflow) to train a connected model on top of a VGG16 model (pre-trained on the ImageNet database). The model was trained on 2000 images of each class (birds and planes) taken from Flickr API. We then put together a very (very!) rough Flask app on Heroku to allow us to share it

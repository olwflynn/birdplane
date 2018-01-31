from keras.applications.vgg16 import VGG16

#Get back the convolutional part of a VGG network trained on ImageNet
model_vgg16_conv = VGG16(weights='imagenet', include_top=False, input_shape=(224,224,3))
model_vgg16_conv.summary()

#save model
model_vgg16_conv.save('vgg16_conv_150pixels.h5')

# Image Processing Platform (IPP)

USC CSCI577a Team04

## Team members

* Hao Wu
* Meiyi Yang
* Yifan Liu
* Xiangchen Zhao
* Vinny DeGenova
* Xinhui Liu
* Junran Liu

## Environment for the project

* Ubuntu 14.04 / 14.10 / 15.04/ 16.04
* Mysql 5.7
* Python 3.5
* Django 1.9.2
* Celery 1.3
* Tensorflow r0.11

## Hardware and Software

Tensorflow has two version: CPU version and GPU version. The GPU version will have a shorter time for retraining the model. (Actually during our testing, the GPU version only has half or one third of training time than the CPU version.) Our system is running in the GPU version Tensorflow environment. However, the CPU version is also compatiable here. <br><br>
The GPU version works best with Cuda Toolkit 8.0 and cuDNN v5. Other versions are supported (Cuda toolkit >= 7.0 and cuDNN >= v3) only when installing from sources. This TensorFlow GPU support requires having a GPU card with NVidia. Supported cards include but are not limited to: NVidia Titan, NVidia Titan X, NVidia K20, NVidia K40. <br><br>
For more details about the Tensorflow GPU version, please check https://www.tensorflow.org/versions/r0.11/get_started/os_setup.html#optional-install-cuda-gpus-on-linux <br>

## System Overview

### Structure

* Image Recognition: 1.Home Page --> 2.Image Uploading --> 3.Result 
* Model Training: 1.Home Page --> 5.Label List --> 6.Image Uploading to Certain Label --> 7.Training Progress

### Image Recognition

Here we could upload images AT MOST 5 from the local computer for image recognition and select certain image recognition model.  <br>

* Image Uploading Page
   * Model Selection: There are two models availble here: one is an original model provided by our team and one is the latest retrain model which was trained in the "Model Training" part.
   * Image Uploading: You could upload at most 5 images here from the local computer. All the images which is uploaded successfully will be shown in the image list below.
   * Begin Button: Begin to recognite the uploaded images with selected model. The whole process of the image recognition will last for about 2 second per image.

* Result Page
   * The result showing in the "Result" page are both image and its recognited label. One thing must be paid attention here is the label result is only selected from the labels which have been registed in the system before. This label list is shown and could be modified in the "5. Label List".

### Model Training

Our system has provided an origin model for image recognition, you could see the label list for the original image here or retrain a model by yourselve in this part. <br>
 <br>
When you begin to retrain the model, the WHOLE image dataset will be retrained and generate a new model. The whole process may last from 10 minutes to 2 hours. You could use this retrained model in the "Image Recognition" part.

* Label List Page:
   * Add Label: You could add a new label to the label list and then upload images to this label. 
   
   * Select Label for Uploading images: After adding a new label or selecting an old label, you will go to next page to upload images.
    
	* Label List: The images in CIFAR 100 dataset are divided into 100 clasess. For usage of the Tensorflow, images in one class must be put in a folder named by this class. And the whole dataset should be one folder containing all these sub-folders. The label list showing here is the 100 classes at first. And an original model has been trained using these 100 classes by our team. Here is some information for the model: 
	
> Algorithm: Tensorflow, Convolutional Neural Networks, 5000 iterations<br>
https://www.tensorflow.org/versions/r0.11/tutorials/image_recognition/index.html#image-recognition<br>
> Image Dataset: CIFAR 100<br>
https://www.cs.toronto.edu/~kriz/cifar.html<br>
> Label List ("classes" in the CIFAR 100)<br>
>> aquatic mammals: beaver, dolphin, otter, seal, whale<br>
fish: aquarium fish, flatfish, ray, shark, trout<br>
flowers: orchids, poppies, roses, sunflowers, tulips<br>
food containers: bottles, bowls, cans, cups, plates<br>
fruit and vegetables: apples, mushrooms, oranges, pears, sweet peppers<br>
household electrical devices: clock, computer keyboard, lamp, telephone, television<br>
household furniture: bed, chair, couch, table, wardrobe<br>
insects: bee, beetle, butterfly, caterpillar, cockroach<br>
large carnivores: bear, leopard, lion, tiger, wolf<br>
large man-made outdoor things: ridge, castle, house, road, skyscraper<br>
large natural outdoor scenes: cloud, forest, mountain, plain, sea<br>
large omnivores and herbivores: camel, cattle, chimpanzee, elephant, kangaroo<br>
medium-sized mammals: fox, porcupine, possum, raccoon, skunk<br>
non-insect invertebrates: crab, lobster, snail, spider, worm<br>
people: baby, boy, girl, man, woman<br>
reptiles: crocodile, dinosaur, lizard, snake, turtle<br>
small mammals: hamster, mouse, rabbit, shrew, squirrel<br>
trees: maple, oak, palm, pine, willow<br>
vehicles 1: bicycle, bus, motorcycle, pickup truck, train<br>
vehicles 2: lawn-mower, rocket, streetcar, tank, tractor<br>

* Image Uploading to Certain Label Page
   * Image Uploading: Here is a limitation that you have to upload MORE THAN 30 images because our model requires a large scale of data for accuracy. All the images you uploaded successfully will be shown here. (Attention: we don't show the images already have in this label). 
   * Begin Button: retrain the model by current dataset. The whole process will last from 10 minutes to several hours. You could see the progress in the next page or just close it.
   
* Training Progress Page
   * Training Progress: the training progress will be shown here. You could close this page and back to this page.











Memebot 1.0

Memebot 1.0 is an open source search engine for memes that you can train and use for making some dank ass meme references. 

Memebot 1.0 works with 2 main components : 
1. text to image 
2. actor recognition 

Training

The first step to running this project is to retrain the pre-trained tensor flow model with your favourite memes. To do this, install tensorflow using pip. 

>pip install tensorflow

This installs tensorflow and also lets you use the tensorflow library in python. 
Next clone the tensorflow git repository. This is so that you can retrain and create a new tensorflow binary trained on your dank ass memes. 

>git clone https://github.com/tensorflow/tensorflow

Once you're done, you need to build the Inception tensorflow binary for the first time, trained on imagenet images. To do this, 

>brew install bazel

>bazel build tensorflow/examples/image_retraining:retrain

(This will take atleast 20 - 30 minutes, computing power notwithstanding. For additional details : https://www.tensorflow.org/tutorials/image_retraining)
Now you can retrain the last layer of Inception that is just created with your memes. To do that : 

>bazel-bin/tensorflow/examples/image_retraining/retrain --image_dir ~/memes

(Arrange your memes directory, such that you have different subfolders each with a label indicating what the images inside it are. The labels could be anything, for instance, actors.)

Once this is done, you're done with the first part, training a tensorflow model. 

Running

Setup

To run, you need to setup a few things. 

1. flask (pip install flask)
2. pymongo (pip install pymongo)
3. tesserocr (pip install tesseract)

You need to setup a MongoDb in your system. To do that : 

>brew install mongodb

>sudo mkdir -p /data/db

>sudo chmod +x /data/db

Now you've setup mongodb. Next we need to start the mongo server. To do this:

>mongod

You should see the server running with the last line saying 'waiting for connections on port 27017'. If not, debug at https://docs.mongodb.com/master/tutorial/install-mongodb-on-os-x/

Next you need to start the backend server. To do this : 

>cd Scripts

>python app.py

This should start a server in localhost:5000. If it works correctly the message should be : ""Debugger is active!""

Once you're here, you can actually run your meme searches. Open a new tab in the browser and go to http://localhost:5000/ . This should show you a message saying ""Hello world"". To search type http://localhost:5000/main/api/v1.0/memes?text=<insert_senseless_meme_text>&actor=<insert_actor_name>. This should show you a list of json objects with information on top memes matching your search query, with the image name as one of the fields . If you get an empty list, see the next section. 

Populating data

Once you have a working system, you can populate your mongodb with memes so that you can search them. This is important, because otherwise your searches would likely return empty. To do this: 

>python insert_memes.py -i <root_directory_with_memes_to_add>

This should take some time and show you some random outputs with your labels. Once it's all run you should see the message : ""All memes inserted. Vanakkam Mahan"". 
Now you can go back to searching and making 130 crores and 76 million meme references.

UI

To run the UI for Memebot, go to the UI directory and start a server. The simplest way to start a server is
> python -m SimpleHTTPServer <port>

Then go to localhost:<port> and you should be able to see the ui. 


FAQs
1. The UI shows up, but when I search for something, I do not see the results. Why?

A: To do this, you need to ensure 2 things.
1. The mongo server is running (mongod)
2. The backend server is running (python app.py)

Even after this if you do not see results, then the issue is most likely caused by CORS. To confirm this, open up the console and then search for something, you should see an error like this 
> XMLHttpRequest cannot load http://cl.ly/2wr4. No 'Access-Control-Allow-Origin' header is present on the requested resource. Origin 'localhost:4001' is therefore not allowed access.

This is basically due to the fact that chrome (and most other browsers) do not allow a localhosted ui to communicate with a localhosted backend (because communism) . So to get around this, you can either use firefox and die or install this extension: https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi?hl=en and enable it while searching in MemebotUI, like a normal person. 


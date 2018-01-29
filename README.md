# dl

by Joe Hahn,<br />
jmh.datasciences@gmail.com,<br />
16 January 2018<br />
git branch=master


### Intro:

This demo uses an LSTM neural network for text classification. In this demo we download about
90 books from Project Gutenberg including titles like Dracula, Moby Dick, Wuthering Heights,
etc, with these books then exploded into about one hundred thousand chunks of text
that are each 100 words long. Each text-chunk is then vectorized in a way that preserves
word order, so note that a bag-of-words approach is NOT used here.
The demo then splits these text-chunks into training and
testing samples and then trains a long short term memory (LSTM) neural
network to predict the author of each text-chunk in the testing sample. LSTM is useful
when making predictions from ordered data such as text, and is why it is used here.
The model accuracy is then assessed.

This model is executed on a gpu-ready g2.2xlarge instance in the AWS cloud using the Bitfusion
Tensorflow AMI, and the _Setup_ section below describes how to launch that instance and 
prep the input data in the Amazon cloud, with results detailed in the _Execute_ section. 

### Setup:


1 Launch a g2.2xl EC2 instance in AWS using these settings:

    EC2 > launch instance > Community AMIs
    search for 'Bitfusion Ubuntu TensorFlow' > g2.2xlarge
    set tag Name=dl
    security group settings:
        set SSH and TCP entries to have Source=My IP         #this permits ssh and jupyter
        add custom TCP rule, port=6006, Source=My IP         #this permits tensorboard
    create keypair with name=dl
    Launch

this instance provides 26 ECUs, 8 vCPUs, 2.6 GHz, Intel Xeon E5-2670, 15 Gb memory, 
10 Gb SSD Storage, cost=$0.74/hr

2 store private ssh key tf-demo.pem in subfolder 'private' with these permissions:

    chmod 400 private/dl.pem

3 obtain the instance's public IP address from the EC2 console, and then ssh into the instance:

    ssh -i private/dl.pem ubuntu@ec2-52-11-206-236.us-west-2.compute.amazonaws.com

4 clone this repo:

    git clone https://github.com/joehahn/dl.git
    cd dl

5 install additional python libraries

    sudo pip install seaborn
    #sudo pip install gensim

6 download an ISO CD of 600 Project Gutenberg books from a mirror (note that Gutenberg
often blocks wget from an EC2 instance), then mount:

    wget http://mirrors.pglaf.org/gutenberg-iso/PG2003-08.ISO
    mkdir iso
    sudo mount -ro loop PG2003-08.ISO iso
    ls -R iso

6 parse the input books:

    ./parse_texts.py

8 update locate database:

    sudo updatedb

9 change this line in ~/.jupyter/jupyter_notebook_config.py, so Jupyter stores its notebooks in dl:

    c.NotebookApp.notebook_dir = u'/home/ubuntu/dl'

10 stash instance-id:

    echo $(ec2metadata --instance-id) > instance-id
    cat instance-id

11 kill the jupyter processes originally launched by this bitfusion AMI:

    ps -aux | grep jupyter
    sudo kill -9 XXXX

since those Jupyter UIs wont let you navigate to this repo.

12 then start jupyter:

    jupyter notebook

13 browse jupyter at public_IP:8888 and log in with password=instance-id

    ec2-52-11-206-236.us-west-2.compute.amazonaws.com:8888


14 use dl.ipynb notebook to train tf model to do text classification


15 Monitor GPU usage:

    watch -n0.1 nvidia-smi

16 start tensorboard

    tensorboard --logdir=tf_logs/

17 browse tensorboard at

    ec2-52-11-206-236.us-west-2.compute.amazonaws.com:6006

18 Monitor GPU usage:

    watch -n0.1 nvidia-smi




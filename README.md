# dl

by Joe Hahn,<br />
jmh.datasciences@gmail.com,<br />
16 January 2018<br />
git branch=master


### Intro:

this will eventually become a simple demo of deep learning on aws with keras and 
gpus...in progress...


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

    tensorboard --logdir=logs/

17 browse tensorboard at

    ec2-52-11-206-236.us-west-2.compute.amazonaws.com:6006

18 Monitor GPU usage:

    watch -n0.1 nvidia-smi




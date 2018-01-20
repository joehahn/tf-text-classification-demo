# dl

by Joe Hahn,<br />
jmh.datasciences@gmail.com,<br />
16 January 2018<br />
git branch=master


### Intro:

this will eventually become a simple demo of deep learning on aws with keras and 
gpus...in progress...


### Setup:

1 Clone this repo:

    git clone https://github.com/joehahn/dl.git
    cd dl

2 Launch a g2.2xl EC2 instance in AWS via recipe detailed in  
https://hackernoon.com/keras-with-gpu-on-amazon-ec2-a-step-by-step-instruction-4f90364e49ac
using these settings:

    EC2 > launch instance > Community AMIs
    search for 'Bitfusion Ubuntu TensorFlow' > g2.2xlarge ($2.86/hr)
    set tag Name=dl
    security group settings:
        set SSH and TCP entries to have Source=My IP (this enables ssh and jupyter)
        add custom TCP rule, port=6006, Source=My IP (to enable tensorboard)
    create keypair dl.pem
    Launch

3 Get the public IP address from the EC2 console, then ssh into the instance. The 
following assumes the ssh private key is stored in private/dl.pem:

    chmod 400 private/dl.pem
    ssh -i private/dl.pem ubuntu@ec2-54-190-198-117.us-west-2.compute.amazonaws.com

4 Update locate:

    sudo updatedb

5 Get instance ID:

    ec2metadata --instance-id

6 Start jupyter:

    sudo jupyter notebook --allow-root

7 Browse jupyter at public_IP:8888 ie

    ec2-54-190-198-117.us-west-2.compute.amazonaws.com:8888

8 Train a CNN on CIFAR-10 images:

    cd ~/tensorflow-models/tutorials/image/cifar10
    python ./cifar10_multi_gpu_train.py

9 start tensorboard:

    cd ~/tensorflow-models/tutorials/image/cifar10
    tensorboard --logdir .

then browse

    ec2-54-190-198-117.us-west-2.compute.amazonaws.com:6006

and log in with password=instance-id

10 Monitor GPU usage:

    watch -n0.1 nvidia-smi

11



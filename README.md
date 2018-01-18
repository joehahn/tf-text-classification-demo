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

    git clone https://github.com/joehahn/epi_int_lite.git
    cd epi_int_lite

2 Launch a g2.2xl EC2 instance in AWS via recipe detailed in  
https://hackernoon.com/keras-with-gpu-on-amazon-ec2-a-step-by-step-instruction-4f90364e49ac
with these settings:

    EC2 > launch instance > Community AMIs
    search for 'Bitfusion Ubuntu TensorFlow' > g2.2xlarge
    set tag Name=DL
    set security groups SSH and TCP entries to have Source=My IP      #for ssh and jupyter
    add custom inbound & outbound TCP rule, port=6006, Source=My IP   #for tensorboard
    choose keypair
    Launch

3 Get the public IP address from the EC2 console, then ssh into the instance ..the 
following assumes my ssh key is stored in folder 'private':

    ssh -i private/datasci.pem ubuntu@ec2-54-218-123-225.us-west-2.compute.amazonaws.com

4 Get instance ID:

    ec2metadata --instance-id

5 Start jupyter:

    sudo jupyter notebook 

6 Browse jupyter at public_IP:8888 ie

    ec2-54-218-123-225.us-west-2.compute.amazonaws.com:8888

and log in with password=instance-id

7 Train CNN on CIFAR-10 images:

    python ~/tensorflow-models/tutorials/image/cifar10/cifar10_multi_gpu_train.py

8 Monitor GPU usage:

    watch -n0.1 nvidia-smi

9

# dl

by Joe Hahn,<br />
jmh.datasciences@gmail.com,<br />
16 January 2018<br />
git branch=master


### Intro:

This demo uses an LSTM neural network for text classification. Begin by downloading about
90 books from Project Gutenberg including titles like Dracula, Moby Dick, Wuthering Heights,
etc, with these books then exploded into about one hundred thousand chunks of text
that are each 100 words long. Each text-chunk is then vectorized in a way that preserves
word order, so note that a bag-of-words approach is NOT used here.
The demo then gathers these text-chunks into training and
testing samples, and then trains a long short term memory (LSTM) neural
network to predict the authors of the testing text-chunks. LSTM is useful
when making predictions from ordered data such as text, and is why it is used here.
Model accuracy is then assessed.

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
10 Gb SSD Storage at a cost of $0.74/hr.

2 The above creates private ssh key named tf-demo.pem that you should store subfolder 'private'
with these permissions:

    chmod 400 private/dl.pem

3 Obtain the instance's public IP address from the EC2 console, and then ssh into the instance:

    ssh -i private/dl.pem ubuntu@ec2-52-11-206-236.us-west-2.compute.amazonaws.com

4 Clone this repo to the instance:

    git clone https://github.com/joehahn/dl.git
    cd dl

5 Install additional python library:

    sudo pip install seaborn

6 Download a CD of 600 Project Gutenberg books from a mirror (since Gutenberg
often blocks downloads from an EC2 instance), then mount:

    wget http://mirrors.pglaf.org/gutenberg-iso/PG2003-08.ISO
    mkdir iso
    sudo mount -ro loop PG2003-08.ISO iso
    ls -R iso

6 Parse the input books:

    ./parse_texts.py

this admittedly unsophisticated script attempts to extract the author and title from each
Gutenberg book (with success ~50% of the time). For each book having a known author and
title, the script explodes the book into 100-word-long chunks of text, and preserves
text-chunks from those books that are at least 750 chunks long. If however a book is longer
than 2200 chunks, only a random selection of 2200 chunks is preserved. Also if an author
has multiple books in this sample, only the longest book is preserved. This results in a
a sample of about 100,000 text-records that are extracted from 88 distinct books, with
each book contributing anywhere between 750 and 2200 records each. So the input sample
does suffer from a modest degree of class imbalance, and that class imbalance is not
corrected here

9 Now prep Jupyter by changing this line in ~/.jupyter/jupyter_notebook_config.py:

    c.NotebookApp.notebook_dir = u'/home/ubuntu/dl'

this allows you to use Jupyter to navigate to this repo.

10 Stash the instance-id:

    echo $(ec2metadata --instance-id) > instance-id
    cat instance-id

11 Kill the jupyter processes that was originally launched by this bitfusion AMI:

    ps -aux | grep jupyter
    sudo kill -9 XXXX

since Bitfusion's Jupyter wont let you navigate to this repo.

12 Then start jupyter:

    jupyter notebook

13 and browse jupyter at public_IP:8888 and log in with password=instance-id

    ec2-52-11-206-236.us-west-2.compute.amazonaws.com:8888


14 Navigate to the dl.ipynb Jupyter notebook and click Kernel > Run to
read the text-chunks and to train the LSTM model on that data. Execution time
is about 20 minutes.

15 You can monitor GPU usage:

    watch -n0.1 nvidia-smi

16 Start tensorboard via

    tensorboard --logdir=tf_logs/

17 And then browse tensorboard UI at

    ec2-52-11-206-236.us-west-2.compute.amazonaws.com:6006

which useful when tuning the neural network parameters.


### Execute

The notebook reads the 100-word-long chunks of text that parse_texts.py extracted
from 88 books downloaded from the Gutenberg Project. The notebook then splits
that data into test, train, and validation samples. It then vectorizes these chunks of
text in a way that preserves word order, and then trains a LSTM model on the test data:
![](figs/model.png)
The Tensorboard UI also provides this interesting graph of the neural network:
![](figs/tensorboard.png)
The notebook takes about 20 minutes to execute, and plots the LSTM model classifier's
accuracy vs training epoch:
![](figs/accuracy.png)
and loss function versus training epoch:
![](figs/loss.png)
That the model achieves 100% accuracy in predicting the authors of the
training text-chunks yet only 75% accuracy in predicting the authors
of the validation text-chunks tells us that this model suffers from some degree of
overfitting.


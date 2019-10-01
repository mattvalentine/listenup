# STT Listen Up Display

## Overview
The main idea is to create an interface that provides visual cues to environmental state which would normally only be available via sound.

Specifically, this system listens for speech, sends it off to Azure for processing, and then parses the results looking for keywords. The text is then sent to an Arduino to display on a 16x2 LCD and if a keyword is found it adds a character indicating the color of an LED to light. 

## Setup
To setup the environment, I'd recommend using <a href="https://docs.conda.io/en/latest/">conda</a>:

```console
conda create -n STT python=3.7 pip
```

And then within Conda, use pip for a couple of packages:

```console
conda activate STT
pip install pyserial azure-cognitiveservices-speech
```

This gives us a known environment to work within. To get out of this environment, use `conda deactivate` (depending on how your terminal is setup you should see either `(base)` or `(STT)` to the left of your command prompt indicating the active environment). 

If you run `conda list` you should see something like this:
```console
# Name                    Version                   Build  Channel
azure-cognitiveservices-speech 1.7.0                    pypi_0    pypi
ca-certificates           2019.8.28                     0  
certifi                   2019.9.11                py37_0  
libcxx                    4.0.1                hcfea43d_1  
libcxxabi                 4.0.1                hcfea43d_1  
libedit                   3.1.20181209         hb402a30_0  
libffi                    3.2.1                h475c297_4  
ncurses                   6.1                  h0a44026_1  
openssl                   1.1.1d               h1de35cc_1  
pip                       19.2.3                   py37_0  
pyserial                  3.4                      pypi_0    pypi
python                    3.7.4                h359304d_1  
readline                  7.0                  h1de35cc_5  
setuptools                41.2.0                   py37_0  
sqlite                    3.29.0               ha441bb4_0  
tk                        8.6.8                ha441bb4_0  
wheel                     0.33.6                   py37_0  
xz                        5.2.4                h1de35cc_4  
zlib                      1.2.11               h1de35cc_3  
```

 See below for more info:

## Azure setup

You'll need to sign up for Azure, but you'll get 5 hours of speech to text per month for free (at this time). So you can try this out quite a bit before it costs you anything, and it's something like a dollar per hour thereafter, so even then it's not that expensive. 

See details here:

https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows

## Two Versions

You'll see that there are two versions of the python script. One is the initial setup with synchronous STT, and the other attempts to add asynchronous STT and greater interaction through the use of a button.
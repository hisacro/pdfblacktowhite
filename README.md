# pdfblacktowhite

This Python script automatically converts dark-background pdf pages to white-background pages with texts color. It supports selective page processing, allowing you to specify which pages to convert. I created this script because I faced the issue with a pdf having random pages with dark backgrounds and white text, which I wanted to be all white. This code processes those pages by changing the background to white and the text to black, resulting in an output pdf with white pages and properly colored text.


# What it does?
 Takes your PDF and lets you pick which pages to fix.
 Changes only those chosen pages into pictures.
 Makes the pictures have white backgrounds and black text (vice versa).
 Changes the pictures back into PDF pages.
 Puts these fixed pages back into the original PDF without changing the other pages.
 Creates a new PDF that is easier to read on the pages you fixed.

<img width="767" height="598" alt="sample1" src="https://github.com/user-attachments/assets/ed516dc1-bd0a-40ea-8270-b6f9817bd1ac" />


# How to Use

### Requirements: 

* Python 3.13.11
* Python packages: pypdf and Pillow
* ghostscript 10.06.0       

### Installation 

You need to creates a new virtual environment in the same directory you are working in. A virtual environment is like a separate, isolated workspace for Python projects where you can install packages without affecting your main system Python or other projects. You can make VE using below command,

```
python -m venv <myenv>
```

Once done making a virtual environment, you need to activate the environmnet using below command,

```
source myenv/bin/activate
```

you will see (myenv) at the start of the prompt, which tells you the virtual environment is active.
Now install the other python package with,

```
pip install pypdf Pillow
```

### Running the Script

Now we have everything ready, its time to run it, using below command inside venv. 
Lets say, I have 3 to 21 all black and I want to convert it to white, I will use below command
```
python pdfcolorinvert.py input.pdf output.pdf 3-21
```

#### completion
You will see "Your output is written to: {output_pdf}", once you have successfully gotten the output.
Enjoy!!

          

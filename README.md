# Visdiff
Visdiff (aka pdiff) is a visual comparison tool.  It compares two existing screenshots and reports the percent  
difference as well as the raw pixel difference count.  Additionally, it merges both images and overlays a color mask  
that makes it easy for a human to see where the differences are.  The base images are darkened and the differences  
are highlighted in yellow.
For the last hackday, functionality was added that allows for masking of a base image with the fucia color.  
Any areas masked in this color will be ignored by the tool, this allows us to test layout and ignore content,  
for example, in the template marketplace we can mask the templates so that when a new one is added or one is removed  
it won't cause a test to break even though the layout is correct.

## Running pdiff
Running pdiff is as simple as 1 command in a terminal.  Simply run `python pdiff.py <image1> <image1> <match-threshold>`  
where image1 and image2 are images of the same dimension and image format (comparing a .jpeg to a .png will fail).  
Additionally a match-threshold is required to tell pdiff how strict to be when when comparing the images.  The lower  
the number, the more strict the match (note: a stricter match will raise the percent difference count).  Through  
trial and error, a good baseline difference threshold is 40.
Example run:  
`python pdiff.py marketplace1.png marketplace2.png 40`

## Prerequisites
PIL is required by python to run this tool.
Install PIL thusly:  
`pip install PIL --allow-external PIL --allow-unverified PIL`


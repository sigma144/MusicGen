# Music Generation

## System Diagram

![alt text](musicgenarch.png?raw=true)

## Brainstorming

In order to make use of the MIDI files, we could do something like what's explained here (extracting trios from MIDI files):
https://github.com/MatthewAwesome/AIComposer/blob/master/AI_Composer_notebook.ipynb


## Project Proposal

Music composition has always been an interesting area to study for computational  creativity. Many extraordinary pieces of music were developed by musicians with their creative minds throughout the years. A computational model that can generate music similar to these musicians would be a great contribution for the development of the area. However, it could be hard to make a generation process that can generate all kinds of music without limitation. Thus, the objective of our project is to develop a model that can take the basic melody and structure of a song and use them to arrange that song in a different style, genre, or mood.

To approach this problem, our current plan is to use concepts of music theory along with random number generation to create pieces that include many of the patterns of typical music, but with unexpected variations that a human composer would not typically consider. To do this, we will break down music into its component concepts (genre, melody, chords, rhythm, structure) and write random generation scripts for each one. To prevent it from being entirely random, we will make critic functions which judge the value of the concepts, possibly informed by data from other musical pieces. We will then create a method to convert these concepts into an output MIDI file. Because the system will need to be able to take a MIDI piece as input, we will write an algorithm that reads the MIDI and extracts musical concepts from the piece (mainly melody and song structure). We might also introduce random variations on the input MIDI concepts (such as changing the melody slightly) to create more variety.

This application will demonstrate creativity by creating novel artefacts that we would not have come up with on our own. We believe this will happen because of two reasons: a large amount of randomness, and critic functions which pull ideas from the overall field rather than just from our own musical preferences. It would also be neat to incorporate some kind of creative autonomy as outlined by Jennings, but this may not be feasible within the scope of our project. Still, we hope that with the randomness and background knowledge, we will be able to create enough interesting artefacts to demonstrate that our system is creative to some degree.

We’ve found a few resources that will likely be very useful in this project. Since we’ll be working with MIDI files, we’ll need a large library of MIDI files to work with, which we’ve found online. We’ve also found a few other similar projects that generate music, namely MuseNet and Magenta. These are two fairly high quality music generators that produce interesting music. These, however, are very heavily based on machine learning and deep learning, which we’re not planning on using extensively in this project. They will provide us with general ideas for our project though.

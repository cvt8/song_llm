# Generate Harmonically correct songs using LLMs
Charles MONTE : charles.monte@telecom-paris.fr \
Constantin VAILLANT TENZER  constantin.tenzer@ens.psl.eu \
Julien BOUDIER julien.boudier@ensae.fr \
Sacha BINDER sacha.binder@eleves.enpc.fr 

This project explores song generation with an emphasis on the respect of harmony and rhythm theory. Our goal is to develop a model capable of generating songs that we will then evaluate with a custom grade out of 20 describing the consonance of harmonies and the consistency in rhythm.

**References:** \
https://github.com/fegounna/LLM-Fine-Tuning-for-Music-Generation/tree/master \
https://github.com/CodeName-Detective/Prompt-to-Song-Generation-using-Large-Language-Models/blob/main/report.pdf \
SongComposer: A Large Language Model for Lyric and Melody Composition in Song Generation https://arxiv.org/abs/2402.17645 \
An Automatic Chord Progression Generator Based On Reinforcement Learning https://ieeexplore.ieee.org/document/8554901 

# Installation

Using the `environment.yml` file, you can setup and activate a conda environment with the following command: 
```console
conda env create -n song_llm -f environment.yml
conda activate song_llm
```

# Using the code

The code is mainly split into two notebooks: 
- `model_creation.ipynb` which tackles all the implementation of the model, from the definition of the Tokenizer to the training and saving of the model;
- `inference.ipynb` aims at evaluating the performance of the best model, qualitatively but also quantitatively thanks to the custom notation described in `notation.py`;
- `text_to_midi.py` is a small library to convert a generated text to a MIDI sequence.

A pretrained model is available in `models/` and allows for the use of `inference.ipynb` to generate songs and evaluate them.

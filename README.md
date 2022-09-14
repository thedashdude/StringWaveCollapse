# String Wave Collapse
Wave Function Collapse algorithm in 2d for strings

## Overview

This program adapts the Wave Function Collapse algorithm to work for string values. 

The algorithm is based on quantum collapses, where particles in super-positions of many states are collapsed to single states when any one of 
them picks a state.

For this version, a large corpus of text is provided by the user (provided is the list of all President's names) and scanned by program.

It then develops a model of the relationships between nearby characters. So, if the letter 'a' is always followed by the letter 'b', this will 
be reflected in the final product.

The `radius` variable determines how wide these relationships are. With `radius=1`, each character generated must be immediately preceeded 
and followed by characters it was preceeded and followed by in the original corpus, but only those immediate characters.

This makes the results chaotic compared to `radius = 2`, where each character must fit within the first two characters preceeding it and following it. 

Having developed the model, the program creates a "wave" in super-position, or an array that tracks every option for every character. Then it begins 
its collapse, choosing the character with the least possible correct options and forcing it out of super-position into a single option. This collapse 
propogates, and soon a random string is settled on that follows all the patterns found in the corpus text.

In the example provided, the String Wave Collapse has produced what it considers names that look like presidential names.

For detailed explanations of the algorithm, there are plenty of resources online:

https://www.youtube.com/watch?v=2SuvO4Gi7uY

https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/

https://www.youtube.com/watch?v=TO0Tx3w5abQ

## Execution

To run the wave collapse there are two options:
1. Running the file
2. Running the notebook

### File
 
To run the file, navigate to the `Source` folder and run `python main.py`. 

You can experiment with the program by editing `main.py` and inputting different files or using different length and radius parameters.

### Notebook

Using Jupyter Notebooks, simply run through all the code in order. 

Re-run the `produce()` function to get new results, or edit the parameters, or try a different base body of text.

## Example Output

Your output, while random, should looks something like this:

```John Clingtonroe
Calvin A. Arthur
Dwight H. Grover
Andrew John Taft
George W. Bush
Grover Arterson
Gerald Jefferce
Zacharry Clerce
Warrew Jefferce
John Art Hoover
Ger A. Tyleveld
Cherter Cleverce
Woodroversonanan
Frahard Bushing
Zachames Adams
Geord Mon Poln
Jimmy A. Kennedy
John F. Growerce
Andon H. Hayley
James Ken Adams

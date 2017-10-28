#######################

This code is from "" with some modification

To use the peptide visualize software,the following requirements are needed.

`pymol` can ce download in
`http://www.pymol.org/`
`python==3.6` with packages :`optparse`,`numpy`

You can use `pip` to install these packages
```
pip install optparse
pip install numpy
```
>Start to use the software
>=========
>First,you needed to make the propensity score file for the perl script.
>---------
>Run the `make_PS.py` to make the file
>
>```
>python make_PS.py -f [scorecard] -t [type:PS or DPS] -n [normalize] -o [outputname]
>```
>For example :
>```
>python make_PS -f example_scorecard -t DPS -n -o DPS.tab
>```
>
>### Second,using the perl to draw the peptide.
>
>```
>perl SCM_color_v3.pl
>```
>Then,key in the PDB , propensity score , smooth parameter and the output file(.pml).
>
>### Third,open the PDB file with pymol, then click file>run and choose the .pml file.
>
># Finally,you can see the visualize scorecard result of any peptide.

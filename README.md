# Cogorza

A program to predict BAC in bloodstream giving a set of drinks by assuming mass conservation.

----
### Requirements:
 
+ python 3
+ numpy
+ pandas
+ matplotlib
+ scipy

----

### Input parameters:

+ Body Mass: M (in kg)
+ Gender : man/woman
+ Mass to blood ratio: Cs (L/kg) : 0.067 L/kg
+ Proportion of alcohol absorbed : Abs : 10% for man, 12% for woman
+ Time of alcohol absorption : tabs (between 15 and 60 min, depending on amount and type of food in stomach)

+ initial BAC : a0 (by default, 0 g/L)
+ simulation lenght : in hours
+ time step integration, in seconds (by default, 1s)
+ start time of simulation (0 s by default)

+ For each drink:
 1. Volumne ingested (in mL)
 2. Strenght of alcoholic drink (divided by 100, ej. beer of 5% graduation is 0.05)
 3. initial time of ingestion (in seconds since start time)
 4. final time of ingestion (in secods from start time of simulation)

### Resources: 

+ An implementation of Python program is provided in Cogorza.py file. The same implementation is provided in jupyter notebook version (Cogorza.ipynb).

+ BACPY.csv is the output data file provided by running the program

+ The "Ouput" folder, a set of output examples are presented as png files. Example:

![A test image](Outputs/Cogorza_2b.png)

--- 

### How to run Cogorza:

To run it using python :

+ In CLI, just type "python Cogorza.py"

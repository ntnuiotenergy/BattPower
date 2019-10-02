# BattPower
Install package
  -	Pyomo
  -	Matplotlib
  -	Pandas

Make_Tab_Files_BatPower.py
  -	Convert parameter data in excel to tab-files
  
  BatPower.py
  - Create
 -  indexes
 -  Sets
 -  Scalars
 -	Parameters
     -Load parameters from tab-files made in “Make¬_Tab_Files_BatPower.py”
 - Variables
 - Objective function
 - Constraints
    - Battery
    - Energy flow
    - Energy balance
 - Solver
 - Write the optimal value
 
  Results_BatPower.py
 - Collect the variables and parameters from the solved problem in “ BatPower.py” and transport them into a excel file


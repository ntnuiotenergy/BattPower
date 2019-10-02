# BattPower
Install package
  -	Pyomo
  -	Matplotlib
  -	Pandas

Make¬_Tab_Files_BatPower.py
  -	Convert parameter data in excel to tab-files
BatPower.py
  - Create
    o	indexes
    o	Sets
    o	Scalars
    o	Parameters
      - Load parameters from tab-files made in “Make¬_Tab_Files_BatPower.py”
    o	Variables
  -	Objective function
  -	Constraints
    o	Battery
    o	Energy flow
    o	Energy balance
  -	Solver
  -	Write the optimal value
Results_BatPower.py
  -	Collect the variables and parameters from the solved problem in “ BatPower.py” and transport them into a excel file


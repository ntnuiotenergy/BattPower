from __future__ import division
from pyomo.environ import *
# from pyomo.core.expr  import current as EXPR
# import numpy as np
import math
import csv
import numpy as np
from Results_BatPower import write_results

model = AbstractModel()


###################################### Scalars and constants##########################################################
######################################################################################################################


######################################  Time, Scenarios and Buses  #######################################

model.Periods = 672  # Number of periods of analysis of the energy variables
model.Years = 8  # Number of years of the project

model.week = (model.Years * 26)

model.Scenarios = 1
model.Buses = 31
model.BusesM = 10
model.BusesL = 31
model.BusesLV1 = 13
model.BusesLV2 = 15
model.BusesLV3 = 18
model.BusesLV4 = 23
model.BusesLV5 = 26
model.BusesLV6 = 28
model.BusesLV7 = 31




######################################  Battery  ####################################################################
model.Efficiency_Dis = Param(initialize=0.95)
model.Efficiency_Ch = Param(initialize=0.95)
model.force_no_batteries = Param(initialize=1)
model.start_precentage_bat = Param(initialize=0.15)

######################################  Battery1  ##################################################################

model.Batt_Max_Capacity_1 = Param(initialize=2)
model.Batt_Min_Capacity_1 = Param(initialize=0.4)
model.Discharge_rate_1 = Param(initialize=0.6)
model.Ch_rate_1 = Param(initialize=0.6)
model.Cost_Batt_1 = Param(initialize=41300)

######################################  Battery2  #################################################################

model.Batt_Max_Capacity_2 = Param(initialize=40)
model.Batt_Min_Capacity_2 = Param(initialize=8)
model.Discharge_rate_2 = Param(initialize=12)
model.Ch_rate_2 = Param(initialize=12)
model.Cost_Batt_2 = Param(initialize=788161)





#####################################  SETS  #########################################################################
######################################################################################################################

model.periods = RangeSet(1, model.Periods)  # Creation of a set from 1 to the number of periods in each year
model.years = RangeSet(1, model.Years)  # Creation of a set from 1 to the number of years of the project
model.scenario = RangeSet(1, model.Scenarios)  # Creation of a set from 1 to the numbero scenarios to analized
model.buses = RangeSet(1, model.Buses)
model.busesM = RangeSet(0, model.BusesM)
model.busesMtest = RangeSet(1, model.BusesM)
model.busesMOut = [1,6,9]
model.busesL = RangeSet(model.BusesM, model.BusesL)
model.busesLV1 = RangeSet(model.BusesM + 1, model.BusesLV1)
model.busesLV2 = RangeSet(model.BusesLV1 + 1, model.BusesLV2)
model.busesLV3 = RangeSet(model.BusesLV2 + 1, model.BusesLV3)
model.busesLV4 = RangeSet(model.BusesLV3 + 1, model.BusesLV4)
model.busesLV5 = RangeSet(model.BusesLV4 + 1, model.BusesLV5)
model.busesLV6 = RangeSet(model.BusesLV5 + 1, model.BusesLV6)
model.busesLV7 = RangeSet(model.BusesLV6 + 1, model.BusesLV7)


########################################  Parameters   ###############################################################
######################################################################################################################

############################################ Load ##########################################################
model.Load = Param(model.scenario, model.periods, model.busesL, default=0.0)

############################################ RES ##########################################################

model.solarMV = Param(model.scenario, model.periods, model.busesMtest, default=0.0)
model.solarLV = Param(model.scenario, model.periods, model.busesL, default=0.0)

model.wind = Param(model.scenario, model.periods, model.busesL, default=0.0)
model.windMV = Param(model.scenario, model.periods, model.busesMtest, default=0.0)

############################################ Costs ##########################################################

model.Grid_Cost = Param(model.scenario, model.periods, default=0.0)
model.Grid_Sold = Param(model.scenario, model.periods, default=0.0)
model.Transform_price = Param(model.scenario, model.busesM, default=0.0)

######################################## Line and transformer ######################################################

model.line_Max = Param(model.scenario, model.busesM, model.busesM, default=0.0)
model.matrix = Param(model.scenario, model.busesM, model.busesM, default=0.0)
model.Loss_trans_Line = Param(model.scenario, model.busesMtest, default=0.0)
model.Loss_Line = Param(model.scenario, model.busesM, model.busesM, default=0.0)

model.transformer_Old_Capacity = Param(model.scenario, model.busesM, default=0.0)
model.transformer_upgrade = Param(model.scenario, model.busesM, default=0.0)



print("Reading Parameters")


######################################## Loading Parameters   ########################################################
######################################################################################################################

data = DataPortal()

data.load(filename='Data/Energy/Example/Load_Load.tab', param=model.Load, format="table")


data.load(filename='Data/Energy/Example/Solar__LV.tab', param=model.solarLV, format="table")
data.load(filename='Data/Energy/Example/Solar_MV.tab', param=model.solarMV, format="table")

data.load(filename='Data/Energy/Example/Wind_LV.tab', param=model.wind, format="table")
data.load(filename='Data/Energy/Example/Wind__MV.tab', param=model.windMV, format="table")

data.load(filename='Data/Energy/Example/Grid_Cost.tab', param=model.Grid_Cost, format="table")
data.load(filename='Data/Energy/Example/Grid_Revenue.tab', param=model.Grid_Sold, format="table")

data.load(filename='Data/Energy/Example/Connect_Grid_LineCap.tab', param=model.line_Max, format="table")
data.load(filename='Data/Energy/Example/Connect_Grid_LineConnect.tab', param=model.matrix, format="table")

data.load(filename='Data/Energy/Example/Transformer_Capacity.tab', param=model.transformer_Old_Capacity, format="table")
data.load(filename='Data/Energy/Example/Transformer_Upgrade.tab', param=model.transformer_upgrade, format="table")
data.load(filename='Data/Energy/Example/Transformer_Cost.tab', param=model.Transform_price, format="table")
data.load(filename='Data/Energy/Example/Connect_Grid_LossesTrans.tab', param=model.Loss_trans_Line, format="table")
data.load(filename='Data/Energy/Example/Connect_Grid_LossLines.tab', param=model.Loss_Line, format="table")

print("Read and declared parameters")

#####################################  Variables  ####################################################################
######################################################################################################################


#####################################  Battery 1  ####################################################################


model.batt_Disch_1 = Var(model.scenario, model.periods, model.buses, within=NonNegativeReals)
model.batt_Ch_1 = Var(model.scenario, model.periods, model.buses, within=NonNegativeReals)
model.State_of_Charge_1 = Var(model.scenario, model.periods, model.buses, within=NonNegativeReals)

#####################################  Battery 2  ####################################################################


model.batt_Disch_2 = Var(model.scenario, model.periods, model.buses, within=NonNegativeReals)
model.batt_Ch_2 = Var(model.scenario, model.periods, model.buses, within=NonNegativeReals)
model.State_of_Charge_2 = Var(model.scenario, model.periods, model.buses, within=NonNegativeReals)


#####################################  Energy in line  ###############################################################

model.energy_line = Var(model.scenario, model.busesM, model.busesM, model.periods, within=NonNegativeReals)
model.inputLV = Var(model.scenario, model.periods, model.busesM, within=NonNegativeReals)
model.outputLV = Var(model.scenario, model.periods, model.busesM, within=NonNegativeReals)

#########################################  Decision ##################################################################

model.binary_transformer = Var(model.scenario, model.busesM, within=NonNegativeIntegers)
model.Integers_1 = Var(model.scenario, model.buses, within=NonNegativeIntegers)
model.Integers_2 = Var(model.scenario, model.buses, within=NonNegativeIntegers)


######################################### Objective ##################################################################

model.F_optimal = Var(model.scenario, within=NonNegativeReals)



print("made variables")


######################################  Objective and Constraints  ####################################################
###########################################  Model formulation  #######################################################
#######################################################################################################################


############################################  objective function  ####################################################
######################################################################################################################

def f_optimal_function(model):
    return sum(model.F_optimal[i] for i in model.scenario)

model.f_optimal_function = Objective(rule=f_optimal_function, sense=minimize)


def F_optimal(model, i):

    foo = []
    for f in model.periods:
        foo.append((i, f))

    LV = []
    for h in model.buses:
        LV.append((i, h))

    MV = []
    for k in model.busesMtest:
        MV.append((i, k))

    MV1 = []
    for l in model.busesMtest:
        MV1.append((i, l))

    return model.F_optimal[i] == model.week * sum((model.energy_line[i, 0, 1, t] * model.Grid_Cost[i, t]) -
        (model.Grid_Sold[i, t] * model.energy_line[i, 1, 0, t]) for i, t in foo) + \
           sum((model.Integers_1[i, n] * model.Cost_Batt_1) for i, n in LV) + \
           sum((model.Integers_2[i, n] * model.Cost_Batt_2) for i, n in LV) + \
           sum((model.Transform_price[i, n] * model.binary_transformer[i, n]) for i, n in MV1)


model.F_optimal_con = Constraint(model.scenario, rule=F_optimal)


#########################################  Constraints  #############################################################
#####################################################################################################################


#########################################  Battery 1 #################################################################


###########################################  SoC  ####################################################################

def state_of_charge_eq1(model, i, t, n):
    if t == 1:  # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_of_Charge_1[i, t, n] == 0.4 * model.Integers_1[i, n] - model.batt_Disch_1[i, t, n] / \
               model.Efficiency_Dis + model.batt_Ch_1[i, t, n] * model.Efficiency_Ch
    if t > 1:
        return model.State_of_Charge_1[i, t, n] == model.State_of_Charge_1[i, t - 1, n] - \
               model.batt_Disch_1[i, t, n] / model.Efficiency_Dis + model.batt_Ch_1[i, t, n] * model.Efficiency_Ch


model.SoCh1 = Constraint(model.scenario, model.periods, model.buses, rule=state_of_charge_eq1)



###################################### features ###################################################################

def max_capacity_bat_1(model, i, t, n):
    return model.State_of_Charge_1[i, t, n] <= model.Batt_Max_Capacity_1 * model.Integers_1[i, n]


model.MaxCapa1 = Constraint(model.scenario, model.periods, model.buses, rule=max_capacity_bat_1)


def min_capacity_bat_1(model, i, t, n):
    return model.State_of_Charge_1[i, t, n] >= model.Batt_Min_Capacity_1 * model.Integers_1[i, n]


model.MinCapa1 = Constraint(model.scenario, model.periods, model.buses, rule=min_capacity_bat_1)


def max_discharge_1(model, i, t, n):
    return model.batt_Disch_1[i, t, n] <= model.Discharge_rate_1 * model.Integers_1[i, n] * 00


model.MaxDisch1 = Constraint(model.scenario, model.periods, model.buses, rule=max_discharge_1)


def max_charge_1(model, i, t, n):
    return model.batt_Ch_1[i, t, n] <= model.Ch_rate_1 * model.Integers_1[i, n] * 0


model.MaxCh1 = Constraint(model.scenario, model.periods, model.buses, rule=max_charge_1)



###################################### Battery 2 #################################################################


######################################### SoC ####################################################################

def state_of_charge_eq2(model, i, t, n):
    if t == 1:  # The state of charge (State_Of_Charge) for the period 0 is equal to the Battery size.
        return model.State_of_Charge_2[i, t, n] == 8 * model.Integers_2[i, n] - model.batt_Disch_2[i, t, n] / \
               model.Efficiency_Dis + model.batt_Ch_2[i, t, n] * model.Efficiency_Ch
    if t > 1:
        return model.State_of_Charge_2[i, t, n] == model.State_of_Charge_2[i, t - 1, n] - \
               model.batt_Disch_2[i, t, n] / model.Efficiency_Dis + model.batt_Ch_2[i, t, n] * model.Efficiency_Ch



###################################### features ###################################################################

model.SoCh2 = Constraint(model.scenario, model.periods, model.buses, rule=state_of_charge_eq2)

def max_capacity_bat_2(model, i, t, n):
    return model.State_of_Charge_2[i, t, n] <= model.Batt_Max_Capacity_2 * model.Integers_2[i, n]


model.MaxCapa2 = Constraint(model.scenario, model.periods, model.buses, rule=max_capacity_bat_2)


def min_capacity_bat_2(model, i, t, n):
    return model.State_of_Charge_2[i, t, n] >= model.Batt_Min_Capacity_2 * model.Integers_2[i, n]


model.MinCapa2 = Constraint(model.scenario, model.periods, model.buses, rule=min_capacity_bat_2)


def max_discharge_2(model, i, t, n):
    return model.batt_Disch_2[i, t, n] <= model.Discharge_rate_2 * model.Integers_2[i, n] * 0


model.MaxDisch2 = Constraint(model.scenario, model.periods, model.buses, rule=max_discharge_2)


def max_charge_2(model, i, t, n):
    return model.batt_Ch_2[i, t, n] <= model.Ch_rate_2 * model.Integers_2[i, n] * 0


model.MaxCh2 = Constraint(model.scenario, model.periods, model.buses, rule=max_charge_2)




###################################### Lines #################################################################

def line_limit(model, i, j, n, t):
    return model.energy_line[i, j, n, t] <= model.line_Max[i, n, j] * model.matrix[i, n, j]


model.Line_C_12 = Constraint(model.scenario, model.busesM, model.busesM, model.periods, rule=line_limit)





###################################### Transformer #################################################################

def max_transformer_in(model, i, t, n):
    return model.inputLV[i, t, n] <= model.transformer_Old_Capacity[i, n] + \
           model.transformer_upgrade[i, n] * model.binary_transformer[i, n]


model.Transformer = Constraint(model.scenario, model.periods, model.busesM, rule=max_transformer_in)


def max_transformer_out(model, i, t, n):
    return model.outputLV[i, t, n] <= model.transformer_Old_Capacity[i, n] + \
           model.transformer_upgrade[i, n] * model.binary_transformer[i, n]


model.Transformer1 = Constraint(model.scenario, model.periods, model.busesM, rule=max_transformer_out)


########################################Energy Balance MV-nodes #################################################



def energy_balance_2(model, i, t, n):
    Di = []
    for r in model.busesM:
        Di.append(r)

    return model.outputLV[i, t, n] * model.Loss_trans_Line[i, n] + model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
           model.solarMV[i, t, n] + model.windMV[i, t, n] + sum((model.energy_line[i, j, n, t] * model.Loss_Line[i, j, n]) for j in Di) \
           == sum(model.energy_line[i, n, j, t] for j in Di) + model.batt_Ch_1[i, t, n] + model.batt_Ch_2[i, t, n] + model.inputLV[i, t, n]


model.Energy_bal_2 = Constraint(model.scenario, model.periods, model.busesMtest, rule=energy_balance_2)


########################################Energy Balance LV-nodes #################################################


def energy_balance_lv_2(model, i, t):
        Dis = []
        for r in model.busesLV1:
            Dis.append(r)

        return model.inputLV[i, t, 2] * model.Loss_trans_Line[i, 2] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
        model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] \
        + model.batt_Ch_2[i, t, n] for n in Dis) + model.outputLV[i, t, 2]


model.energy_bal_2_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_2)


def energy_balance_lv_3(model, i, t):
    Dis1 = []
    for r in model.busesLV2:
        Dis1.append(r)

    return model.inputLV[i, t, 3] * model.Loss_trans_Line[i, 3] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
            model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis1) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] + \
            model.batt_Ch_2[i, t, n] for n in Dis1) + model.outputLV[i, t, 3]


model.energy_bal_3_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_3)


def energy_balance_lv_4(model, i, t):
    Dis2 = []
    for r in model.busesLV3:
        Dis2.append(r)

    return model.inputLV[i, t, 4] * model.Loss_trans_Line[i, 4] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
            model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis2) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] + model.batt_Ch_2[i, t, n] \
            for n in Dis2) + model.outputLV[i, t, 4]


model.energy_bal_4_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_4)


def energy_balance_lv_5(model, i, t):
    Dis3 = []
    for r in model.busesLV4:
        Dis3.append(r)
    return model.inputLV[i, t, 5] * model.Loss_trans_Line[i, 5] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
        model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis3) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] + model.batt_Ch_2[i, t, n] for n in Dis3) + model.outputLV[i, t, 5]


model.energy_bal_5_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_5)


def energy_balance_lv_7(model, i, t):
    Dis4 = []
    for r in model.busesLV5:
        Dis4.append(r)
    return model.inputLV[i, t, 7] * model.Loss_trans_Line[i, 7] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
        model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis4) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] + \
        model.batt_Ch_2[i, t, n] for n in Dis4) + model.outputLV[i, t, 7]


model.energy_bal_7_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_7)


def energy_balance_lv_8(model, i, t):
    Dis5 = []
    for r in model.busesLV6:
        Dis5.append(r)
    return model.inputLV[i, t, 8] * model.Loss_trans_Line[i, 8] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
        model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis5) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] \
        + model.batt_Ch_2[i, t, n] for n in Dis5) + model.outputLV[i, t, 8]

model.energy_bal_8_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_8)


def energy_balance_lv_10(model, i, t):
    Dis6 = []
    for r in model.busesLV7:
        Dis6.append(r)
    return model.inputLV[i, t, 10] * model.Loss_trans_Line[i, 10] + sum(model.batt_Disch_1[i, t, n] + model.batt_Disch_2[i, t, n] + \
        model.solarLV[i, t, n] + model.wind[i, t, n] for n in Dis6) == sum(model.Load[i, t, n] + model.batt_Ch_1[i, t, n] \
        + model.batt_Ch_2[i, t, n] for n in Dis6) + model.outputLV[i, t, 10]


model.energy_bal_10_lv = Constraint(model.scenario, model.periods, rule=energy_balance_lv_10)


def energy_balance_lv_None(model, i, t, n):

        return model.inputLV[i, t, n] * model.Loss_trans_Line[i, n] == model.outputLV[i, t, n]

model.energy_bal_1_lv = Constraint(model.scenario, model.periods, model.busesMOut, rule=energy_balance_lv_None)



######################################## Solver ########################################################


instance = model.create_instance(data)  # load parameters

opt = SolverFactory('gurobi', Verbose=True)  # Solver use during the optimization
results = opt.solve(instance, tee=True)  # Solving a model instance
instance.solutions.load_from(results)  # Loading solution into instance

resultspi = write_results(instance)



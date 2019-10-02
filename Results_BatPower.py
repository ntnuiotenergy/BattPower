import pandas as pd


def write_results(instance):

    ########################### Import Variables #############################################################

    Batt_Disch_1_R = instance.batt_Disch_1.get_values()
    Batt_Disch_2_R = instance.batt_Disch_2.get_values()

    Batt_Ch_1_R = instance.batt_Ch_1.get_values()
    Batt_Ch_2_R = instance.batt_Ch_2.get_values()

    SoC_1 = instance.State_of_Charge_1.get_values()
    SoC_2 = instance.State_of_Charge_2.get_values()

    Int_1_R = instance.Integers_1.get_values()
    Int_2_R = instance.Integers_2.get_values()

    Line_R = instance.energy_line.get_values()
    Batt_InputLV = instance.inputLV.get_values()
    binary_trans_R = instance.binary_transformer.get_values()
    OutputLV_R = instance.outputLV.get_values()

    ########################### Import Parameters #############################################################

    Solar_RLV = instance.solarLV
    Solar_RMV = instance.solarMV
    Wind_R31 = instance.wind

    Load_R1 = instance.Load
    Cost_R = instance.Grid_Cost
    Sold_r = instance.Grid_Sold


    ##################### Writing the different variables and Parameters into excel##############################

    df_auto = []
    busesk = instance.Buses + 1
    busesMV = instance.BusesM + 1
    i = instance.Scenarios
    periodsi = instance.Periods + 1
    for j in range(1, busesk + 1):
        df_auto.append(j)

    #################################### Writing the MV-nodes into Excel ##########################################

    for n in range(1, busesMV):
        df_auto[n] = pd.DataFrame({'Line0' + str(n): Line_R[i, 0, n, t], 'Line1' + str(n): Line_R[i, 1, n, t],
                                   'Line2' + str(n): Line_R[i, 2, n, t], 'Line3' + str(n): Line_R[i, 3, n, t],
                                   'Line4' + str(n): Line_R[i, 4, n, t], 'Line5' + str(n): Line_R[i, 5, n, t],
                                   'Line6' + str(n): Line_R[i, 6, n, t], 'Line7' + str(n): Line_R[i, 7, n, t],
                                   'Line8' + str(n): Line_R[i, 8, n, t], 'Line9' + str(n): Line_R[i, 9, n, t],
                                   'Line10-' + str(n): Line_R[i, 10, n, t], 'Line' + str(n) + '0': Line_R[i, n, 0, t],
                                   'Line' + str(n) + '1': Line_R[i, n, 1, t], 'Line' + str(n) + '2': Line_R[i, n, 2, t],
                                   'Line' + str(n) + '3': Line_R[i, n, 3, t], 'Line' + str(n) + '4': Line_R[i, n, 4, t],
                                   'Line' + str(n) + '5': Line_R[i, n, 5, t], 'Line' + str(n) + '6': Line_R[i, n, 6, t],
                                   'Line' + str(n) + '7': Line_R[i, n, 7, t], 'Line' + str(n) + '8': Line_R[i, n, 8, t],
                                   'Line' + str(n) + '9': Line_R[i, n, 9, t], 'Line' + str(n) + '-10': Line_R[i, n, 10, t],
                                   'Batt_Disch_1_' + str(n): Batt_Disch_1_R[i, t, n], 'Batt_Disch_2_' + str(n): Batt_Disch_2_R[i, t, n],
                                   'Batt_Ch_1_' + str(n): Batt_Ch_1_R[i, t, n], 'Batt_Ch_2_' + str(n): Batt_Ch_2_R[i, t, n],
                                   'Input_LV_' + str(n): Batt_InputLV[i, t, n], 'SoC_1_' + str(n): SoC_1[i, t, n],
                                   'SoC_2_' + str(n): SoC_2[i, t, n], 'Binary_Bat_1_' + str(n): Int_1_R[i, n],
                                   'Binary_Bat_2_' + str(n): Int_2_R[i, n], 'OutputLV_' + str(n): OutputLV_R[i, t, n],
                                   'Binary_trans_' + str(n): binary_trans_R[i, n], 'Cost_Energy': Cost_R[i, t],
                                   'Revenue_Energy': Sold_r[i, t],  'solarMV_' + str(n): Solar_RMV[i, t, n]} for t in range(1, periodsi))


    #################################### Writing the LV-nodes into Excel ##########################################

    for n in range(busesMV, busesk):
        df_auto[n] = pd.DataFrame(
            {'Batt_Disch_1_' + str(n): Batt_Disch_1_R[i, t, n], 'Batt_Disch_2_' + str(n): Batt_Disch_2_R[i, t, n],
             'Batt_Ch_1_' + str(n): Batt_Ch_1_R[i, t, n], 'Batt_Ch_2_' + str(n): Batt_Ch_2_R[i, t, n],
             'SoC_1_' + str(n): SoC_1[i, t, n], 'SoC_2_' + str(n): SoC_2[i, t, n],
             'Load_' + str(n): Load_R1[i, t, n], 'Binary_Bat_1_' + str(n): Int_1_R[i, n],
             'Binary_Bat_2_' + str(n): Int_2_R[i, n], 'SolarLV' + str(n): Solar_RLV[i, t, n],
             'Wind_LV' + str(n): Wind_R31[i, t, n]} for t in range(1, periodsi))

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    w_auto = pd.ExcelWriter('Results/Energy/R_auto.xlsx', engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.

    for k in range(1, busesk):
        r_auto = df_auto[k].to_excel(w_auto, index=False, sheet_name='Node' + str(k))

    w_auto.save()

    return r_auto

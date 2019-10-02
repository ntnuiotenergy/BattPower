from pyomo.environ import *
import pandas as pd

model = AbstractModel()
model.is_constructed()


def read_file(excel,sheet,columns):
    input_excel = pd.ExcelFile(excel)
    input_sheet = pd.read_excel(input_excel, sheet, skiprows=1)

    #First make it so it takes all the rows and the amount of columns I want
    #Second makes the labels in the colums with _ and not space

    data_table = input_sheet.iloc[:,columns]
    data_table.columns = pd.Series(data_table.columns).str.replace(' ', '_')
    data_nonempty = data_table.dropna()

    save_csv_frame = pd.DataFrame(data_nonempty)

    save_csv_frame.replace('\s', '', regex=True, inplace=True)

    save_csv_frame.to_csv(excel.replace(".xlsx", "_") + sheet + '.tab', header=True, index=None, sep='\t', mode='w')
    #print(excel.replace(".xlsx", "_") + sheet + '.tab')
    input_excel.close()



read_file("Data/Grid.xlsx", "Cost", [0, 1, 2])
read_file('Data/Grid.xlsx', 'Revenue', [0, 1, 2])

read_file('Data/Load.xlsx', 'Load', [0, 1, 2, 3])

read_file('Data/Solar_.xlsx', 'LV', [0, 1, 2, 3])

read_file('Data/Wind.xlsx', 'LV', [0, 1, 2, 3])
read_file('Data/Wind_.xlsx', 'MV', [0, 1, 2, 3])


read_file('Data/Solar.xlsx', 'MV', [0, 1, 2, 3])



read_file('Data/Transformer.xlsx', 'Cost', [0, 1, 2])
read_file('Data/Transformer.xlsx', 'Capacity', [0, 1, 2])
read_file('Data/Transformer.xlsx', 'Upgrade', [0, 1, 2])
read_file('Data/Connect_Grid.xlsx', 'LineCap', [0, 1, 2, 3])

read_file("Data/Connect_Grid.xlsx", "LineConnect", [0, 1, 2, 3])
read_file("Data/Connect_Grid.xlsx", "LossesTrans", [0, 1, 2])
read_file("Data/Connect_Grid.xlsx", "LossLines", [0, 1, 2, 3])
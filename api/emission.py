import pandas as pd



def read_and_merge():
    dt2017 = pd.read_excel('../data/17tstcar-2018-05-30.xlsx')
    dt2018 = pd.read_excel('../data/18tstcar-2018-10-24.xlsx')
    dt2019 = pd.read_excel('../data/19tstcar-2020-10-02.xlsx')
    dt2020 = pd.read_excel('../data/20tstcar-2021-03-02.xlsx')
    dt2021 = pd.read_excel('../data/21-tstcar-2022-04-15.xlsx')
    dt2022 = pd.read_excel('../data/22-testcar-2023-06-13.xlsx')
    dt2023 = pd.read_excel('../data/23-testcar-2024-05-17_0.xlsx')
    dt2024 = pd.read_excel('../data/24-testcar-2024-05-17_0.xlsx')
    dataframes = [dt2017, dt2018, dt2019, dt2020, dt2021, dt2022, dt2023, dt2024]

    # Concatenate dataframes vertically
    co2 = pd.concat(dataframes, axis=0)

    # Reset index to ensure the indices are unique
    co2.reset_index(drop=True, inplace=True)
    co2.drop_duplicates(inplace=True)
    return co2

def generate_mapping(co2):
    mapping = {}
    for index, row in co2.iterrows():
        brand = row['Represented Test Veh Make']
        car = row['Represented Test Veh Model']
        year = row['Model Year']
        emission = row['CO2 (g/mi)']
        year = str(year)
        key = brand + " " + car + " " + year
        mapping[key] = emission
    return mapping

def calculate_emission(per_mile, total):
    return per_mile * total


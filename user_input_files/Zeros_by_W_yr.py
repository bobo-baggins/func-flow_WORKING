# Checks number of zeros in each water year and outputs to csv for QAQC

import pandas as pd

def cnt_zero_flows():
    # Ask for the input and output file names
    input_filename = input("Please enter the input file name: ")
    output_filename = input("Please enter the output file name: ")

    #reads in csv file name supplied
    df =pd.read_csv(input_filename)

    #Ensures date is in correct format for pandas fucntion calling
    df['date'] = pd.to_datetime(df['date'])

    #Create water year coloumn using lambda function if October, November, Decemeber, 
    # adds 1 to year and stores it in water_year coloum otherwise grabs year from x 'date' entry.
    df['water_year'] = df['date'].apply(lambda x: x.year+1 if x.month >= 10 else x.year)

    #Zero count coloumn
    df['is_zero'] = (df['flow'] == 0).astype(int)

    #Sum zeros entries from flow
    zero_flows_per_Wyear = df.groupby('water_year')['is_zero'].sum()

    #Converts series to DF
    df_zero_flows_per_Wyear = zero_flows_per_Wyear.reset_index()
    
    df_zero_flows_per_Wyear.columns = ['water_year', 'num_zero_flows']

    #Writes DF to csv file and prints Series
    df_zero_flows_per_Wyear.to_csv(output_filename, index=False)
    print(zero_flows_per_Wyear)

cnt_zero_flows()
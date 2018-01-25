import matplotlib
matplotlib.use('Agg')
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from utils.helpers import is_multiple_date_data
from utils.matrix_convert import convert_raw_data_to_matrix
from utils.calc_general_metric import calculate_average_each_row

np.warnings.filterwarnings('ignore')

def dim_hydrograph_plotter(start_date, directoryName, endWith):

    gauge_class_array = []
    gauge_number_array = []
    row_average = []
    for root,dirs,files in os.walk(directoryName):
        for file in files:
            if file.endswith(endWith):

                fixed_df = pd.read_csv('{}/{}'.format(directoryName, file), sep=',', encoding='latin1', dayfirst=False, header=None).dropna(axis=1, how='all')

                if is_multiple_date_data(fixed_df):
                    print('Current Datset uses one date per column of data')
                    step = 2
                else:
                    print('Current Datset uses the same date per column of data')
                    step = 1

                current_gaguge_column_index = 1

                while current_gaguge_column_index <= (len(fixed_df.iloc[1,:]) - 1):

                    current_gauge_class, current_gauge_number, year_ranges, flow_matrix, julian_dates = convert_raw_data_to_matrix(fixed_df, current_gaguge_column_index, start_date)

                    """General Info"""
                    gauge_class_array.append(current_gauge_class)
                    gauge_number_array.append(current_gauge_number)

                    """Dimensionless Hydrograph Plotter"""
                    row_average.append(calculate_average_each_row(flow_matrix))
                    number_of_rows = len(flow_matrix)
                    number_of_columns = len(flow_matrix[0,:])
                    normalized_matrix = np.zeros((number_of_rows, number_of_columns))
                    percentiles = np.zeros((number_of_rows, 5))

                    for row_index, row_data in enumerate(flow_matrix[:,0]):
                        for column_index, column_data in enumerate(flow_matrix[row_index, :]):
                            normalized_matrix[row_index,column_index] = flow_matrix[row_index,column_index]/row_average[-1][row_index]

                        percentiles[row_index,0] = np.nanpercentile(normalized_matrix[row_index,:], 10)
                        percentiles[row_index,1] = np.nanpercentile(normalized_matrix[row_index,:], 25)
                        percentiles[row_index,2] = np.nanpercentile(normalized_matrix[row_index,:], 50)
                        percentiles[row_index,3] = np.nanpercentile(normalized_matrix[row_index,:], 75)
                        percentiles[row_index,4] = np.nanpercentile(normalized_matrix[row_index,:], 90)

                    x = np.arange(0,366,1)
                    label_xaxis = np.array(julian_dates[0:366])
                    
                    plt.figure(current_gaguge_column_index)
                    plt.plot(percentiles[:,0], color = 'navy')
                    plt.plot(percentiles[:,1], color = 'blue')
                    plt.plot(percentiles[:,2], color = 'red')
                    plt.plot(percentiles[:,3], color = 'blue')
                    plt.plot(percentiles[:,4], color = 'navy')
                    plt.fill_between(x, percentiles[:,0], percentiles[:,1], color = 'powderblue')
                    plt.fill_between(x, percentiles[:,1], percentiles[:,2], color = 'powderblue')
                    plt.fill_between(x, percentiles[:,2], percentiles[:,3], color = 'powderblue')
                    plt.fill_between(x, percentiles[:,3], percentiles[:,4], color = 'powderblue')
                    plt.title("Dimensionless Hydrograph")
                    plt.xlabel("Julian Date")
                    plt.ylabel("Daily Flow/Average Annual Flow")
                    plt.grid(which = 'major', linestyle = '-', axis = 'y')
                    ax = plt.gca()
                    tick_spacing = [0, 50, 100, 150, 200, 250, 300, 350]
                    ax.set_xticks(tick_spacing)
                    tick_labels = label_xaxis[tick_spacing]
                    ax.set_xticklabels(tick_labels)

                    plt.savefig("post_processedFiles/Hydrographs/{}.png".format(int(current_gauge_number)))

                    current_gaguge_column_index = current_gaguge_column_index + step

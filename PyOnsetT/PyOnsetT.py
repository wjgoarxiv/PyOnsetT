#!/usr/bin/env python

# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ruptures as rpt
import argparse
import shutil
import glob
import os 
import time 
from tabulate import tabulate

def main():
    # Argparse
    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-ps', '--pnum', type=int, default=1, help='Pressure sensor number (1 or 2), (default=1)')
    parser.add_argument('-ts', '--tnum', type=int, default=1, help='Temperature sensor number (1, 2, 3, or 4), (default=1)')
    parser.add_argument('-d', '--dirloc', type=str, default='./', help='Directory location of the csv files, (default=./)')
    parser.add_argument('-r', '--range', type=int, default=50, help='The range detecting the onset of the temperature change near the rupture [Unit: steps], (default=50)')
    parser.add_argument('-pi', '--pinit', type=int, default = 20, help='The minimum pressure value during the onset temperature measurements [Unit: bar], (default=20 bar)')
    parser.add_argument('-pf', '--pfinal', type=int, default = 34, help='The maximum pressure value during the onset temperature measurements [Unit: bar], (default=34 bar)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.6')

    args = parser.parse_args()

    # Assign arguments to variables
    input_pressure_sensor_num = args.pnum
    input_temp_sensor_num = args.tnum
    input_range = args.range
    input_dirloc = args.dirloc
    input_pinit = args.pinit
    input_pfinal = args.pfinal

    #---------argsparse ends---------#

    # Code artwork
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print(f.renderText('--------'))
    print(f.renderText('PyOnsetT'))
    print(f.renderText('--------'))
    print('------------------------')
    print('\n')
    print('If you have any questions, please send your questions to my email.')
    print('\nOr, please suggest errors and areas that need updating.')
    print('\n 📨 woo_go@yahoo.com')
    print('\n')
    print('\nVisit https://github.com/wjgoarxiv/PyOnsetT for more information.')
    print('\n')
    print('------------------------')
    print('\n')

    # Show user input value 
    print('INFO The pressure sensor number is', input_pressure_sensor_num)
    print('INFO The temperature sensor number is', input_temp_sensor_num)
    print('INFO The directory location is', input_dirloc)
    print('INFO The pressure range you are interested in is', input_pinit, 'bar' , ' ~ ', input_pfinal, 'bar')
    print('INFO The range detecting the onset of the temperature change near the rupture is', input_range, 'steps')
    time.sleep(1.0)

    # Ignore warnings
    import warnings
    warnings.filterwarnings(action='ignore')

    # 1. File number and name checking
    file_list = glob.glob(input_dirloc + '*.csv')
    file_list.sort()
    try:
        if len(file_list) == 0:
            raise Exception
        else:
            pass
    except:
        print("\nINFO There is no csv file in your directory. Please check the directory location.")
        time.sleep(0.2)
        print("INFO The program will stop.")
        time.sleep(1)
        exit()

    # Label file numbers and show all the files
    file_num = []
    for i in range(len(file_list)):
        file_num.append(i)
    print(tabulate({'File number': file_num, 'File name': file_list}, headers='keys', tablefmt='psql'))

    file_number = int(input('INFO These are the files that are in the folder. Please check the file number that you want to use: '))

    # Give one more chance to check the file name
    print("INFO The file name that would be utilized is", file_list[file_number])
    print("INFO Do you want to use this file? (y/n)")

    # Define df based on the file number
    df = pd.read_csv(file_list[file_number], encoding='cp949', header=1)

    # If the user wants to use the file, then continue the program
    if input() == 'y':
        print("INFO The program will continue.")
        pass
    # If the user doesn't want to use the file, then stop the program
    else:
      print("INFO The program will stop.")
      exit() 

    # 2. Get pressure, temperature, and time data
    pressure = df.iloc[1:,int(input_pressure_sensor_num)+1]
    raw_temp = df.iloc[1:,int(input_temp_sensor_num)+3]
    time_sec = df.iloc[1:,1]
    
    # 3. Note that all data are 'object', therefore, we need to convert them to float
    pressure = pressure.astype(float)
    raw_temp = raw_temp.astype(float)
    temp = raw_temp/10 # Since the raw temperature is in 10x scale, we need to divide it by 10 to get real temperature
    time_sec = time_sec.astype(float)
    time_min = time_sec/60 # Convert time from second to minute

    # PLOT 1: P & T - time
    fig, ax1 = plt.subplots()
    color = 'tab:red'
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Pressure (bar)', color=color)
    ax1.plot(time_min, pressure, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax2 = ax1.twinx() # Instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Temperature (℃)', color=color) # we already handled the x-label with ax1
    ax2.plot(time_min, temp, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    fig.tight_layout() # otherwise the right y-label is slightly clipped
    fig.savefig('PLOT1_P&T-time.png', dpi=300) # Saving the figure! 

    # 4. Change the data into numpy array
    pressure_np = np.array(pressure)
    temperature_np = np.array(temp)
    time_sec_np = np.array(time_sec)
    time_min_np = np.array(time_min)

    # 5. Ruptures to find the abrupt change in pressure data
    algo = rpt.Pelt(model="normal").fit(pressure_np)
    result = algo.predict(pen=1400) # Seems that pen = 1400 is the best choice
    result = result[:-1] # Remove the last element of the result list

    #------------------------#
    print('\nINFO The data has been elaborated successfully.')
    #------------------------#

    # 6. Find the change point where the pressure is in the range of pi ~ pf bar. Don't include the last change point, since it is the end of the experiment.
    result = [i for i in result if input_pinit <= pressure_np[i] <= input_pfinal]

    # PLOT2: P & T - time with change points
    rpt.display(pressure_np, result, computed_chg_pts=result, computed_chg_pts_linewidth=1.5, computed_chg_pts_color='purple')

    ## Label the pressure value with the time when the pressure suddenly decreases.
    for i in result:
      plt.text(time_min_np[i], pressure_np[i], str(pressure_np[i]) + ' bar', fontsize=12, color='blue')
      plt.text(time_min_np[i], temperature_np[i], str(round(temperature_np[i], 2)) + ' ℃', fontsize=11, color='tab:orange')
      plt.text(time_min_np[i], 0, str(round(time_min_np[i], 2)) + ' min', fontsize=11, color='purple')

    ## Plot the temperature according to the logging time with second y-axis.
    plt.twinx()
    plt.plot(time_min_np, temperature_np, color='tab:orange')

    ## Store the value in a list 
    onsetT = []
    onsetT_time = []

    ## Find the onset temperature and the time when the pressure suddenly decreases.
    for i in result:
      onsetT.append(temperature_np[i])
      onsetT_time.append(time_min_np[i])

    ## Print the onset temperature and the time when the pressure suddenly decreases.
    print('\nINFO The onset temperature is ', onsetT, '℃')

    ## Convert the onset temperature into Kelvin
    onsetT_K = [i + 273.15 for i in onsetT]

    ## Create a dataframe
    df_finalonset = pd.DataFrame({'onsetT (℃)': onsetT, 'onsetT (K)': onsetT_K, 'onsetT_time (min)': onsetT_time})

    ## Download the plot
    plt.savefig('PLOT2_P&T-time_with_change_points.png', dpi=300)

    # 7. Find exact onset temperatures with the change point
    l=0
    for i in result:
      onsetT_index = df.iloc[i-input_range:i+input_range, int(input_temp_sensor_num)+3].diff().idxmax() - 1
      print('INFO Onset temperature' + str(l+1) + ':', round(df.iloc[onsetT_index, 4]/10, 2), '℃')

      # Iteratively save the new onset temperature and the time into the new dataframe entitled 'df_finalonset'.
      df_finalonset.loc[l, 'onsetT (℃)'] = round(df.iloc[onsetT_index, 4]/10, 2)
      df_finalonset.loc[l, 'onsetT (K)'] = round(df.iloc[onsetT_index, 4]/10, 2) + 273.15
      df_finalonset.loc[l, 'onsetT_time (min)'] = round(df.iloc[onsetT_index, 1]/60, 2)
      
      l+=1 # count the number of iteration 

    # Download the new dataframe
    df_finalonset.to_csv('DATA1_obtained+onset+temperatures.csv')

    # PLOT3: Exact onset temperatures with the change point (magnified view)
    fig, axs = plt.subplots(3, 3, figsize=(8, 6))

    ## Loop for all the onset temperatures
    k=0
    for i in result:
      onsetT_index = df.iloc[i-input_range:i+input_range, int(input_temp_sensor_num)+3].diff().idxmax() - 1
      axs[k//3, k%3].plot(df.iloc[:, 1]/60, df.iloc[:, int(input_temp_sensor_num)+3]/10, color='tab:orange')
      axs[k//3, k%3].set_xlabel('Time (min)')
      axs[k//3, k%3].set_ylabel('Temperature (℃)')
      axs[k//3, k%3].tick_params(axis='y', labelcolor='tab:orange')

      axs[k//3, k%3].set_xlim(df.iloc[onsetT_index-input_range, 1]/60-10, df.iloc[onsetT_index+input_range, 1]/60 + 10)
      axs[k//3, k%3].set_ylim(df.iloc[onsetT_index-input_range, int(input_temp_sensor_num)+3]/10-3.0, df.iloc[onsetT_index+input_range, int(input_temp_sensor_num)+3]/10 + 3.0)

      axs[k//3, k%3].text(df.iloc[onsetT_index, 1]/60, df.iloc[onsetT_index, int(input_temp_sensor_num)+3]/10, str(round(df.iloc[onsetT_index, int(input_temp_sensor_num)+3]/10, 2)) + ' ℃', fontsize=12, color='tab:orange')

      ## Title for each subplot (locate at the top of each subplot, and make sure not to be overlapped by the super title.)
      axs[k//3, k%3].set_title('Onset temperature ' + str(k+1), y=1.05)

      ## If there is no more graph, delete the empty subplot.
      if k == len(result)-1:
        for j in range(k+1, 9):
          fig.delaxes(axs[j//3, j%3])

      fig.suptitle('Obtained onset temperatures', fontsize = 14, fontweight='bold')
      plt.tight_layout()
      k+=1
    
    fig.savefig('PLOT3_Exact_onset_temperatures_with_the_change_point.png', dpi=300)

    # 8. Save all the file (shutil)
    ## Create a new folder (same as raw csv file name)
    file_name = os.path.splitext(os.path.basename(file_list[file_number]))[0]
    os.mkdir(file_name)

    ## Move all the files into the new folder
    shutil.move('DATA1_obtained+onset+temperatures.csv', file_name)
    shutil.move('PLOT1_P&T-time.png', file_name)
    shutil.move('PLOT2_P&T-time_with_change_points.png', file_name)
    shutil.move('PLOT3_Exact_onset_temperatures_with_the_change_point.png', file_name)

    ## Zip the folder
    shutil.make_archive(file_name, 'zip', file_name)
    shutil.rmtree(file_name)

    # 9. Completion message to user
    print('\nINFO The data has been successfully processed and stored in the zip folder named "'+file_name+".zip"+'".')
    time.sleep (0.8)
    print('\nINFO Make sure to check the onset temperatures are correct.')
    time.sleep (0.8)
    print('\nINFO IF not, please change the input range (-r) and run the program again.')
    print('\nINFO For more information, please type "pyonsett -h" or "pyonsett --help".')

# Entry point
if __name__ == '__main__':
  main()
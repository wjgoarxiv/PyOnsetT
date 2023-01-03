# **Example Files Descriptions** 
## **About `.csv` files**
* `Example1.csv` and `Example2.csv` are both experimental results of CO2 hydrate onset temperature measurements.
* Note that `Example1.csv` shows 5 onset temperatures and `Example2.csv` shows 2. No matter how many onset temperatures are measured, PyOnsetT well identifies the onset temperature.
## **What Should You Consider In Your Experimental Data?**
1. First, consider the pressure options that you are adjusted in your experiment. Depending on the gas type, you may need to adjust the pressure range. This can be done by managing your `-pi` and `-pf` options. These pressure ranges are need to be carefully selected to avoid the pressure range that is not suitable for hydrate formation.
2. Consider your pressure and temperature sensor number. The example files showed that the pressure and temperature sensors are 1 and 1, respectively. This can be changed by managing your `-ps` and `-ts` options.
3. Do not include other experimental raw files in your target directory. PyOnsetT will automatically read all `.csv` files in your target directory. If you have other experimental raw files in your target directory, PyOnsetT will read them as well. This may cause an serious error.

# =============================================================================
#
# Script that checks whether a year is a leap year or not.
#
# File:          exercise_1.py     
# Date:          08.01.2018
# Author:        Tabea Mendez
# 
#    (c) Institute for Communication Systems ICOM
#    CH-8640 Hochschule Rapperswil HSR
#    http://icom.hsr.ch
#
# =============================================================================

if __name__ == '__main__':
    # read in years
    yearStr = input('Enter one or more years: ')
    
    # convert string of years into list of numbers
    yearsLst = []
    ind = yearStr.find(' ')
    while ind >= 0:
        if ind > 0:
            year = int(yearStr[:ind])
            yearsLst.append(year)
        yearStr = yearStr[ind+1:]
        ind = yearStr.find(' ')
    year = int(yearStr)
    yearsLst.append(year)
    
    # check if year is a leap year
    for y in yearsLst:
        if y < 0:
            print(y, 'is not a valid input')
            continue
        
        if y % 4 == 0:
            if y % 100 == 0:
                if y % 400 == 0:
                    print('The year', y, 'is a leap year.')
                else:
                    print('The year', y, 'is not a leap year.')
            else:
                print('The year', y, 'is a leap year.')
        else:
            print('The year', y, 'is not a leap year.')
    
    
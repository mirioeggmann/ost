# =============================================================================
#
# Script that checks whether a year is a leap year or not.
#
# File:          master.py     
# Date:          09.01.2018
# Author:        Tabea Mendez
# 
#    (c) Institute for Communication Systems ICOM
#    CH-8640 Hochschule Rapperswil HSR
#    http://icom.hsr.ch
#
# =============================================================================

import leapYear as ly

def main():
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
    leapYearBool = ly.isLeapYear(yearsLst)
    for i in range(len(yearsLst)):
        if leapYearBool[i] is True:
            print('The year {0} is a leap year.'.format(yearsLst[i]))
        elif leapYearBool[i] is False:
            print('The year {0} is not a leap year.'.format(yearsLst[i]))
        else:
            print('{0} is not a valid input'.format(yearsLst[i]))
 
 
if __name__ == '__main__':
    main()
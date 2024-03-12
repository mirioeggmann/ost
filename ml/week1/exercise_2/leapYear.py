# =============================================================================
#
# function to check whether a year is a leap year or not.
#
# File:          leapYear.py     
# Date:          09.01.2018
# Author:        Tabea Mendez
# 
#    (c) Institute for Communication Systems ICOM
#    CH-8640 Hochschule Rapperswil HSR
#    http://icom.hsr.ch
#
# =============================================================================

def isLeapYear(years = [2018]):
    """ Checks for each year number in the list whether it is a leap year.
    
        Args:
            years:      list of year numbers
        Returns:
            leapYear:   list of booleans
    """
    
    leapYear = []
    for y in years:
        if y < 0:
            leapYear.append(None)
            continue
        
        if y % 4 == 0:
            if y % 100 == 0:
                if y % 400 == 0:
                    leapYear.append(True)
                else:
                    leapYear.append(False)
            else:
                leapYear.append(True)
        else:
            leapYear.append(False)

    return leapYear


if __name__ == '__main__':
    print('Start unit-Test for function isLeapYear.')

    # test-cases
    leapYears = [2010, 2008, 1700, 1701, 1702, 
                 1703, 1704, 1600, 1584, -1854]
    leapYearsBoolean = [False, True, False, False, False, 
                        False, True, True, True, None]

    # Calling the function with the default argument
    for b in isLeapYear():
        assert( b == False )
    
    # Calling the function with only one element in the list.
    for i in range(len(leapYears)):
        for b in isLeapYear([leapYears[i]]):
            assert( b == leapYearsBoolean[i] )
    
    # Calling the function with a list
    assert( isLeapYear(leapYears) == leapYearsBoolean )

    print('Unit-test was successful.')
    
    
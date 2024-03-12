def main():
    # read in string of years
    years_str = input("Enter one or more years: ")

    # convert string of years into list of numbers
    years = [int(y) for y in years_str.split()]

    # check if year is a leap year
    for year in years:
        try:
            if is_leap_year(year):
                print("The year", year, "is a leap year.")
            else:
                print("The year", year, "is not a leap year.")
        except ValueError:
            print(year, "is not a valid input.")


def is_leap_year(year=2024):
    """Check whether year is a leap year or not."""
    if year < 0:
        raise ValueError
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False


if __name__ == "__main__":
    main()

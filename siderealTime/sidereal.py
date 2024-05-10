import datetime as dt


def sidereal_time(date: dt.date, time: dt.time, lamda: float) -> float:
    """
    Calculates the local sidereal time given the date, the local time, 
    and the east longitude of the site.

    input:
        date: the date 
        time: local time
        lamda: east longitude of the site (degrees)

    return:
        theta: local sidereal time (degrees)
    """

    J0 = j0(date)

    # time in Julian centuries between the Julian day J0 and J2000
    T0 = (J0 - 2_451_545)/(36_525)

    # the Greenwich sidereal time at 0 h UT
    theta_G0 = 100.4606184 + 36_000.77004 * T0 + \
        0.000387933 * (T0**2) - 2.583e-8 * (T0**3)

    while theta_G0 > 360:
        theta_G0 -= 360

    # the Greenwich sidereal time
    theta_G = theta_G0 + 360.98564724 * \
        (time.hour + time.minute/60 + time.second/(60*60))/24

    # the local sidereal time
    theta = theta_G + lamda

    while theta > 360:
        theta -= 360

    return theta


def j0(date: dt.date) -> float:
    """ given the date return the julien day at 0 h UT """
    y = date.year    # 1900 < y < 2100
    m = date.month
    d = date.day

    j_0 = 367*y - int((7*(y+int((m+9)/(12))))/4) + \
        int((275*m)/(9)) + d + 1_721_013.5

    return j_0


def main():

    # START input: date, time, and east longitude
    date = dt.date(day=3, month=3, year=2004)
    time = dt.time(hour=4, minute=30, second=0)
    lamda = 139.8  # east longitude of the site
    # END input

    print(f"Date: {date}")
    print(f"Time: {time}")
    print(f"East longitude of site: {lamda:.2f} deg")
    print()

    lst = sidereal_time(date, time, lamda)
    print(f"The local sidereal time for the given input is: {lst:.2f} deg")


if __name__ == "__main__":
    main()

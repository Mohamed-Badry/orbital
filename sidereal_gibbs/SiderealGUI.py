import streamlit as st
import datetime as dt

from inspect import getsource
from sidereal import j0, sidereal_time


def main():

    st.title('Sidereal Time')

    st.header('App')
    st.write('This app calculates the local sidereal time by passing the date, the local time, and the east longitude of the site to the function defined below.')

    with st.form(key="sidereal"):
        date = st.date_input("Date: ",
                             min_value=dt.date(year=1900, month=1, day=1),
                             max_value=dt.date(year=2100, month=12, day=31))

        time = st.time_input("Time: ")

        lamda = st.slider("East longitude of the site (degrees):",
                          min_value=0.0,
                          max_value=360.0,
                          value=139.8,
                          step=0.01)

        st.form_submit_button("Calculate Sidereal Time")

        result = round(sidereal_time(date, time, lamda), 2)
        st.write(r"$\textsf{\normalsize The local sidereal time is:}$")
        # Increase font size and change color
        st.write(f"<span style='font-size: 24px; color: #e24d3f;'>{result}&deg; </span>",
                 unsafe_allow_html=True)

    # display the code of the functions
    st.header('Function Code')

    sidereal_code = getsource(sidereal_time)
    j0_code = getsource(j0)

    st.code(sidereal_code, language="python")
    st.code(j0_code, language="python")

    # made by note
    st.write('<style>.made-by { text-align: center; font-size: 12px; color: gray; }</style>',
             unsafe_allow_html=True)
    st.write('<div class="made-by">Made by Mohamed Badry!</div>',
             unsafe_allow_html=True)


if __name__ == "__main__":
    main()

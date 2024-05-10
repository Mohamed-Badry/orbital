import streamlit as st
import numpy as np

from gibbs import gibbs, orbital_elements
from inspect import getsource


def get_vector_input(col, label):
    with col.expander(f'$ \\vec {label[0]}_{label[1]}  \\space\\space (km)$'):
        x = st.number_input("$x$", key=f"{label}_x")
        y = st.number_input("$y$", key=f"{label}_y")
        z = st.number_input("$z$", key=f"{label}_z")

    return np.array([x, y, z])


def main():

    st.title('Gibbs\' method')

    st.header('App')
    st.write('This app takes 3 coplanar position vectors and calculates the 6 classical orbital elements using Gibbs\' method.')

    with st.form(key="gibbs"):
        r1_col, r2_col, r3_col = st.columns(3)

        r1 = get_vector_input(col=r1_col, label='r1')
        r2 = get_vector_input(col=r2_col, label='r2')
        r3 = get_vector_input(col=r3_col, label='r3')

        st.form_submit_button("Calculate Orbital Elements")

        try:
            result = gibbs(r1, r2, r3)
            st.write(f'$ h = {result[0]} \\space (km^2/s)$')
            st.write(f'$ i = {result[1]}\\degree $')
            st.write(f'$ \\Omega = {result[2]}\\degree $')
            st.write(f'$ e = {result[3]} $')
            st.write(f'$ \\omega = {result[4]}\\degree $')
            st.write(f'$ \\theta = {result[5]}\\degree $')
        except ValueError as e:
            st.error(e.args[0] +
                     '\nTry values for vectors that lie in the same plane.')

    # display the code of the functions
    st.header('Function Code')

    gibbs_code = getsource(gibbs)
    orb_elems_code = getsource(orbital_elements)

    st.code(gibbs_code, language="python")
    st.code(orb_elems_code, language="python")

    # made by note
    st.write('<style>.made-by { text-align: center; font-size: 12px; color: gray; }</style>',
             unsafe_allow_html=True)
    st.write('<div class="made-by">Made by Mohamed Badry!</div>',
             unsafe_allow_html=True)


if __name__ == "__main__":
    main()

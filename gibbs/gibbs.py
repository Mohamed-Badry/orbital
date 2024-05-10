import numpy as np


def gibbs(
    r1_vec: np.ndarray, r2_vec: np.ndarray, r3_vec: np.ndarray,
    mu: float = 398600, show_NDS: bool = False
) -> list:
    """
    Calculates the 6 orbital elements using Gibbs\' method.

    input:
        r1, r2, r3: coplanar position vectors at three successive times t1, t2, and t3 
        mu: standard gravitational parameter (km^3/s^2) (defaults to earth's value of mu)
        show_NDS: prints the intermediary vectors N, D, S, v2 that you calculate to 
        while applying Gibbs' method

    return: 
        the 6 orbital elements in a list in the order
            [h, i, Omega, e, omega, theta]
    """
    def mag(x):
        """returns the magnitude of the vector x"""
        return np.sqrt(x.dot(x))

    # tolerance for orthogonality check
    tol = 1e-5

    # vector magnitudes
    r1 = mag(r1_vec)
    r2 = mag(r2_vec)
    r3 = mag(r3_vec)

    # independant cross products of r1, r2, r3
    C12 = np.cross(r1_vec, r2_vec)
    C23 = np.cross(r2_vec, r3_vec)
    C31 = np.cross(r3_vec, r1_vec)

    # verify u_r1 is orthogonal to C23
    u_r1 = r1_vec/r1
    u_C23 = C23/mag(C23)
    if u_r1.dot(u_C23) > tol:
        raise ValueError(
            "Orthogonality check failed, the 3 vectors aren't coplanar.")

    # N, D, S vectors that arise while applying gibbs' method
    N = r1*C23 + r2*C31 + r3*C12

    D = C12 + C23 + C31

    S = r1_vec * (r2 - r3) + r2_vec * (r3 - r1) + r3_vec * (r1 - r2)

    v2 = np.sqrt(mu/(mag(N) * mag(D))) * (np.cross(D, r2_vec)/r2 + S)
    # if your linter shows that this code is unreachable this is a bug with
    # the np.cross function and doesn't affect the code
    if show_NDS:
        np.set_printoptions(precision=3, suppress=True)
        print(f"N = {N} (km^3)")
        print(f"D = {D} (km^2)")
        print(f"S = {S} (km^2)")
        print(f"v2 = {v2} (km/s)")
        print()

    return orbital_elements(r2_vec, v2, mu=mu)


def orbital_elements(
    r_vec: np.ndarray, v_vec: np.ndarray, mu: float = 398600,
) -> list:
    """
    Calculates the 6 orbital elements from a state vector [r, v]

    input:
        r_vec: position vector
        v_vec: velocity vector
        mu: standard gravitational parameter (km^3/s^2) (defaults to earth's value of mu)

    return: 
        the 6 orbital elements in a list in the order
            [h, i, Omega, e, omega, theta]
    """

    def mag(x):
        """returns the magnitude of the vector x"""
        return np.sqrt(x.dot(x))

    UNIT_K = np.array([0, 0, 1])

    r = mag(r_vec)  # distance
    v = mag(v_vec)  # speed

    # radial velocity
    v_r = np.dot(r_vec, v_vec) / r

    # specific angulat momentum
    h_vec = np.cross(r_vec, v_vec)
    h = mag(h_vec)

    # inclination
    i = np.rad2deg(np.arccos(h_vec[2] / h))

    # node line
    n_vec = np.cross(UNIT_K, h_vec)
    n = mag(n_vec)

    # right ascension of the ascending node
    Omega = np.rad2deg(np.arccos(n_vec[0] / n))
    # if N_y is less than 0 take the complement of OMEGA
    if n_vec[1] < 0:
        Omega = 360 - Omega

    # eccentricity vector
    e_vec = (1 / mu) * (
        (((v**2) - (mu / r)) * r_vec) - ((r * v_r) * v_vec)
    )
    # eccentricity
    e = mag(e_vec)

    # argument of perigee
    omega = np.rad2deg(np.arccos(np.dot(n_vec, e_vec) / (n * e)))
    # if e_z is less than 0 take the complement of omega
    if e_vec[2] < 0:
        omega = 360 - omega

    # the true anomaly
    theta = np.rad2deg(np.arccos(np.dot(e_vec, r_vec) / (e * r)))
    # if v_r is less than 0 take the complement of theta
    if v_r < 0:
        theta = 360 - theta

    element_values = np.round([h, i, Omega, e, omega, theta], 2)

    return element_values


def main():

    # START input: vectors
    r1_vec = np.array([-294.32, 4265.1, 5986.7])
    r2_vec = np.array([-1365.5, 3637.6, 6346.8])
    r3_vec = np.array([-2940.3, 2473.7, 6555.8])
    # END input

    h, i, Omega, e, omega, theta = gibbs(r1_vec, r2_vec, r3_vec, show_NDS=True)

    print(f"specific angular momentum: {h}")
    print(f"inclination: {i}")
    print(f"right ascenscion of ascending node: {Omega}")
    print(f"eccentricity: {e}")
    print(f"argument of perigee: {omega}")
    print(f"true anomaly: {theta}")


if __name__ == "__main__":
    main()

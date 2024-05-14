"""
Copyright 2024 David Woodburn

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "David Woodburn"
__license__ = "MIT"
__date__ = "2024-05-08"
__maintainer__ = "David Woodburn"
__email__ = "david.woodburn@icloud.com"
__status__ = "Development"

import numpy as np
import scipy.optimize as opt

def windows(K, density=64):
    """
    Build an array of averaging window sizes for Allan variances analysis.

    Parameters
    ----------
    K : int
        Number of time samples.
    density : int, default 64
        Desired number of window sizes per decade.

    Returns
    -------
    M : integer np.ndarray
        Array of averaging window sizes.

    Notes
    -----
    Because the elements of `M` should be unique, it cannot be guaranteed that
    there will be exactly `density` sizes in each decade.
    """

    e_max = np.log10(np.floor(K/2))
    M_real = np.logspace(0, e_max, round(e_max*density))
    M = np.unique(np.round(M_real)).astype(int)
    return M


def variance(y, M):
    """
    Calculate the Allan variance of y with the array of averaging window sizes
    specified by M.

    Parameters
    ----------
    y : (K,) or (J, K) float np.ndarray
        Array of `K` values in time or matrix of rows of such arrays.
    M : (I,) integer np.ndarray
        Array of `I` averaging window sizes. Each element of `M` must be an
        integer.

    Returns
    -------
    v : (I,) float np.ndarray
        Array of `I` Allan variances.
    """

    if np.ndim(y) == 1:
        v = np.zeros(len(M))
        Y = np.cumsum(y)
        for n_tau, m in enumerate(M):
            Yc = Y[(2*m - 1):] # Ending integrals
            Yb = Y[(m - 1):(-m)] # Middle integrals
            Yj = Y[:(1 - 2*m)] # Beginning integrals
            yj = y[:(1 - 2*m)] # Beginning
            delta = (Yc - 2*Yb + Yj - yj)/m
            v[n_tau] = np.mean(delta**2)/2
    else:
        J, K = y.shape
        v = np.zeros((J, len(M)))
        Y = np.cumsum(y, axis=1)
        for n_tau, m in enumerate(M):
            Yc = Y[:, (2*m - 1):] # Ending integrals
            Yb = Y[:, (m - 1):(-m)] # Middle integrals
            Yj = Y[:, :(1 - 2*m)] # Beginning integrals
            yj = y[:, :(1 - 2*m)] # Beginning
            delta = (Yc - 2*Yb + Yj - yj)/m
            v[:, n_tau] = np.mean(delta**2, axis=1)/2

    return v


class params:
    def __init__(self, vc, vfogm=None, tfogm=None):
        """
        Parameters
        ----------
        vc : (5,) np.ndarray
            Variances of the five basic component noises: quantization, white,
            flicker, walk, and ramp. If `fogms` is not 0, the third element of `vc`
            will be zero. For any elements of `mask` which are `False`, the
            corresponding elements of `vc` will be zero.
        vfogm : (F,) np.ndarray, default None
            Array of FOGM variances.
        tfogm : (F,) np.ndarray, default None
            Array of FOGM time constants (s).
        """

        # Convert lists and tuples to arrays.
        if isinstance(vc, (list, tuple)):
            vc = np.array(vc)
        if len(vc) != 5:
            raise ValueError("vc should be a 5-element array.")
        if isinstance(vfogm, (list, tuple)):
            vfogm = np.array(vfogm, dtype=float)
        elif isinstance(vfogm, (int, float)):
            vfogm = np.array([vfogm], dtype=float)
        if isinstance(tfogm, (list, tuple)):
            tfogm = np.array(tfogm, dtype=float)
        elif isinstance(tfogm, (int, float)):
            tfogm = np.array([tfogm], dtype=float)

        # Get the number of FOGMs.
        self.F = 0 if vfogm is None else len(vfogm)
        
        # Save the arrays.
        self.vc = vc
        self.vfogm = vfogm
        self.tfogm = tfogm


def ideal(tau, p):
    """
    Generate an ideal Allan variance curve given the component variances.

    Parameters
    ----------
    tau : (I,) np.ndarray
        Array of averaging periods (s).
    p : params object
        Object defining the variances and time constants of the noise.

    Returns
    -------
    va : (I,) np.ndarray
        Array of the ideal sum of component Allan variances.
    vac : (5+F, I) np.ndarray
        Matrix of the component Allan variances. `F` is the number of
        first-order, Gauss-Markov noise components.
    """

    # Define the basic component noise Allan variances.
    vac = np.zeros((5 + p.F, len(tau)))
    vac[0, :] = p.vc[0] * 3/(tau**2)
    vac[1, :] = p.vc[1] * 1/tau
    vac[2, :] = p.vc[2] * 2*np.log(2)/np.pi + 0*tau
    vac[3, :] = p.vc[3] * tau/3
    vac[4, :] = p.vc[4] * (tau**2)/2

    # Include any FOGMs.
    if p.F != 0:
        T = tau[0]
        M = tau/T
    for f in range(p.F):
        q = np.exp(-T/p.tfogm[f])
        vac[5 + f, :] = (p.vfogm[f]/M**2)*(M*(1 - q)**2 + 2*q*M*(1 - q)
                - 2*q*(1 - q**M) - q*(1 - q**M)**2)/(1 - q)**2

    # Sum the component Allan variances.
    va = np.sum(vac, axis=0)

    return va, vac


class fit_metrics:
    n = 0
    nmae = None
    mask = None
    fogm = None

    def init(N):
        fit_metrics.n = 0
        fit_metrics.nmae = np.zeros(N)
        fit_metrics.mask = np.zeros(N)
        fit_metrics.fogm = np.zeros(N)

    def append(nmae, mask, fogm):
        fit_metrics.nmae[fit_metrics.n] = nmae
        fit_metrics.mask[fit_metrics.n] = mask
        fit_metrics.fogm[fit_metrics.n] = fogm
        fit_metrics.n += 1

    def trim():
        fit_metrics.nmae = fit_metrics.nmae[:fit_metrics.n]
        fit_metrics.mask = fit_metrics.mask[:fit_metrics.n]
        fit_metrics.fogm = fit_metrics.fogm[:fit_metrics.n]


def fit(tau, va, mask=None, fogms=0, tol=0.007):
    """
    Fit component variances to a single Allan variance curve.

    Parameters
    ----------
    tau : (I,) np.ndarray
        Array of averaging periods (s).
    va : (I,) np.ndarray
        Array of Allan variances.
    mask : (5,) bool array_like, default None
        Array to mask which component variances to use. Left as `None`, no basic
        component variances will be excluded. However, a positive value for
        `fogms` will override the third element of the mask, regardless of
        whether it is `True` or `False`.
    fogms : int, default 0
        The maximum number of first-order, Gauss-Markov (FOGM) noise components
        to try to fit to the data. This is the maximum number, not the required
        number. The best fit might not use any.
    tol : float, default 0.007
        Normalized mean absolute error tolerance to meet as various combinations
        of the component noises are applied to the fitting.

    Returns
    -------
    vf : (I,) np.ndarray
        Fitted Allan variance curve.
    p : params object
        Object defining the variances and time constants of the noise.

    Notes
    -----
    This function will iterate through the various permutations of component
    noises, starting with 0 FOGMs. If a fit satisfies the specified `tol`, the
    search will end. Otherwise, the best fit will be used.
    """

    def fopt(k, H, M, T, va):
        """
        Parameters
        ----------
        k : (B + 2*F,) np.ndarray
            Array of variables to tune for, starting with some `B` basic noise
            component variances followed by `F` pairs of FOGM variances and time
            constants.
        H : (I, B) np.ndarray
            Matrix of functions of the averaging period.
        M : (I,) np.ndarray
            Array of averaging window sizes.
        T : float
            Sampling period.
        va : (I,) np.ndarray
            Array of Allan variances to fit.
        """

        # Get the number of basic components and FOGM components.
        B = H.shape[1]
        F = (len(k) - B)//2

        # Initialize the normalized fit with the basic components.
        vfn = H/va[:, None] @ np.abs(k[:B])

        # Add to the fit each of the FOGM components.
        for f in range(F):
            v = abs(k[B + 2*f])
            t = abs(k[B + 2*f + 1])
            q = np.exp(-T/t)
            vfn += (1/va)*(v/M**2)*(M*(1 - q)**2 + 2*q*M*(1 - q)
                    - 2*q*(1 - q**M) - q*(1 - q**M)**2)/(1 - q)**2

        return vfn - 1

    # Adjust the mask.
    if mask is None:
        mask = np.ones(5, dtype=bool)
    if isinstance(mask, (list, tuple)):
        mask = np.array(mask, dtype=bool)
    if fogms > 0:
        mask[2] = False

    # Build the basic component Allan variances.
    qnt = 3/(tau**2)
    wht = 1/tau
    flk = 2*np.log(2)/np.pi + 0*tau
    bwn = tau/3
    rmp = (tau**2)/2
    H5 = np.array([qnt, wht, flk, bwn, rmp]).T
    H = H5[:, mask]

    # Get the dimensions.
    B = H.shape[1] # number of basic components to consider

    # Get the range of averaging periods.
    T = tau[0] # sampling period
    talg = np.log10(T)
    tblg = np.log10(tau[-1])

    # Define the reused arrays.
    I = len(va)
    OI = np.ones(I)
    M = tau/T # averaging window sizes

    # Initialize the outputs.
    vf = np.zeros(I)
    p = params(np.zeros(5), np.zeros(fogms), np.zeros(fogms))

    # Define the NMAE components.
    va_lg = np.log10(va)
    range_lg = np.max(va_lg) - np.min(va_lg)
    nmae_min = np.inf

    # Initialize the metrics
    fit_metrics.init((2**B - 1)*(fogms + 1))

    # Estimate the component variances.
    for F in range(fogms + 1): # the number of possible FOGMs
        # Define the starting mask value. Allow for no basic components
        # if the number of FOGMs is nonzero.
        m = 1 if F == 0 else 0

        # For each mask value,
        for mask_value in range(m, 2**B): # the basic mask value
            # Get the H matrix for this permutation.
            maskp = [bool((mask_value >> i) & 1) for i in range(B)]
            Hp = H[:, maskp]
            Bp = Hp.shape[1] # number of components to consider

            # Optimize for this permutation.
            if F == 0: # no FOGMs
                try: # This can fail.
                    k = opt.nnls(Hp/va[:, None], OI)[0]
                except ValueError or RuntimeError:
                    continue
                # Get the fitted Allan variance.
                vfp = Hp @ k
            else: # some FOGMs
                try: # This can fail.
                    # Initialize the parameters, spacing out the FOGM time
                    # constants.
                    k = np.ones(Bp + 2*F)
                    k[Bp + 1::2] = np.logspace(talg, tblg, F + 2)[1:-1]
                    # Optimize.
                    k = np.abs(opt.leastsq(fopt, k,
                            args=(Hp, M, T, va), maxfev=1000)[0])
                except ValueError or RuntimeError:
                    continue
                # Get the fitted Allan variance.
                vfp = Hp @ np.abs(k[:Bp])
                for f in range(F):
                    v = abs(k[Bp + 2*f])
                    t = abs(k[Bp + 2*f + 1])
                    q = np.exp(-T/t)
                    vfp += (v/M**2)*(M*(1 - q)**2 + 2*q*M*(1 - q)
                            - 2*q*(1 - q**M) - q*(1 - q**M)**2)/(1 - q)**2

            # Evaluate the fit.
            er = va_lg - np.log10(vfp)
            nmae = np.mean(np.abs(er))/range_lg
            if nmae < nmae_min: # save the best
                # Track the minimum error.
                nmae_min = nmae

                # Save the metrics.
                fit_metrics.append(nmae, mask_value, F)

                # Save this fitted Allan variance.
                vf = vfp 

                # Save the basic component variances.
                vcp = np.zeros(B)
                vcp[maskp] = k[:Bp]
                p.vc[mask] = vcp

                if F > 0:
                    p.vfogm[:F] = k[Bp::2]
                    p.tfogm[:F] = k[Bp + 1::2]
            if nmae < tol: # quit early
                break

    # Save the number of FOGMs estimated.
    p.F = F

    # Trim the fit metrics.
    fit_metrics.trim()

    return vf, p


def noise(K, T, p):
    """
    Generate noise using the 5 basic component noise variances of the Allan
    variance analysis and any first-order, Gauss-Markov (FOGM) noises specified.
    The basic component noises are generated as the following:

        Type            Implementation
        ------------    ---------------------------------------
        quantization    differentiated white, Gaussian noise
        white           white, Gaussian noise
        flicker         first-order, Gauss-Markov (FOGM) noise
        walk            integrated white, Gaussian noise
        ramp            doubly integrated white, Gaussian noise

    Parameters
    ----------
    K : int
        Number of samples.
    T : float
        Sampling period (s).
    p : params object
        Object defining the variances and time constants of the noise.

    Returns
    -------
    y : (K,) np.ndarray
        Array of noise values over time.

    Notes
    -----
    Vectorizing this function to generate multiple rows of noise data does not
    actually improve the computation time above calling this function within a
    loop.

    Doubly integrated white noise grows faster the longer the signal. Therefore,
    in order to get the Allan variance of this generated noise to match the
    expected ideal Allan variance magnitude, the amplitude of the noise signal
    is scaled according to the number of samples.

    The scaling factors for the quantization and ramp noises have been empiric-
    ally, not analytically, derived. However, given their simplicity (`1` and
    `sqrt(2)`, respectively) and the very small errors between the average Allan
    variance curves of 10 thousand Monte-Carlo samples of noise and the ideal
    Allan variance curve, it seems they are correct.
    """

    # Initialize the noise array.
    y = np.zeros(K)

    # Quantization noise
    if p.vc[0] != 0:
        w = np.random.randn(K + 1)
        y += np.sqrt(p.vc[0])*np.diff(w)/T

    # White noise
    if p.vc[1] != 0:
        w = np.random.randn(K)
        y += np.sqrt(p.vc[1]/T)*w

    # Bias instability (flicker)
    #if p.vc[2] != 0:
    #    ka = np.exp(-T/taub)
    #    kb = np.sqrt(p.vc[2]*(1 - np.exp(-2*T/taub)))
    #    eta = kb*np.random.randn(K)
    #    x = np.sqrt(p.vc[2])*np.random.randn() # state
    #    for k in range(K):
    #        y[k] += x
    #        x = ka*x + eta[k]

    # Random walk noise
    if p.vc[3] != 0:
        w = np.random.randn(K)
        y += np.cumsum(np.sqrt(p.vc[3]*T)*w)

    # Ramp noise
    if p.vc[4] != 0:
        eta = np.sqrt(2*p.vc[4]/K) * T * np.random.randn(K)
        y += np.cumsum(np.cumsum(eta))

    # FOGM noises
    for f in range(p.F):
        ka = np.exp(-T/p.tfogm[f])
        kb = np.sqrt(p.vfogm[f]*(1 - np.exp(-2*T/p.tfogm[f])))
        eta = kb*np.random.randn(K)
        x = np.sqrt(p.vfogm[f])*np.random.randn() # state
        for k in range(K):
            y[k] += x
            x = ka*x + eta[k]

    return y

import numpy as np


def stf_trapezoidal(omega, trise, trupt):
    """
    Trapezoidal source time function, in frequency domain. 
    This routine is a copy of one in TBO'T's Matlab code, which is itself 
    apparently derived from AXITRA.
    
    The spectrum coded here is the Fourier Transform of the
    convolution of two unit-area boxcars, one of which is non-zero in the
    range [0,trise], and the other of which is non-zero in the range
    [-trupt/2, trupt/2].

    :param complex omega: Frequency at which evaluation is required (rad/s)
    :param float trise: Rise time (s)
    :param float trupt: Total duration of rupture (s)

    :returns: Amplitude of source time function
    """
    uu = np.ones(omega.shape, dtype="complex128")
    uxx = np.ones_like(uu)
    uex = np.ones_like(uu)
    wp = omega != 0
    uu[wp] = omega[wp] * trise * 1j
    uu[wp] = (1 - np.exp(-uu[wp])) / uu[wp]
    uxx[wp] = 1j * omega[wp] * trupt / 2
    uex[wp] = np.exp(uxx[wp])
    uxx[wp] = (uex[wp] - 1 / uex[wp]) / (2 * uxx[wp])
    return uu * uxx


def stf_cosine(omega, thalf):
    """
    Cosine source time function, in frequency domain.
    
    This function implements the Fourier transform of
    f(t, T) = 1/(2T) (1+ cos( pi t / T))     -T < t < T
            = 0                              otherwise
    with T <--> ``thalf``

    :param complex omega: Frequency at which evaluation is required (rad/s)
    :param float thalf: Half-width of source (s)

    :returns: Amplitude of source time function
    """
    # This is the fourier transform of
    # f(t, T) = 1/(2T) (1+ cos( pi t / T))     -T < t < T
    #         = 0                              otherwise
    # with T <--> `thalf`
    return (
        np.pi**2
        * np.sin(omega * thalf)
        / (omega * thalf * (np.pi**2 - (omega * thalf) ** 2))
    )

def stf_boxcar(omega, thalf):
    """
    Boxcar source time function, in frequency domain.

    This function implements the Fourier transform of 
    f(t, T) = 1/(2T)   -T < t < T
            = 0         otherwise
    with T <--> ``thalf``

    :param complex omega: Frequency at which evaluation is required (rad/s)
    :param float thalf: Half-width of boxcar (s)

    :returns: Amplitude of source time function
    """ 
    # This is the fourier transform of
    # f(t, T) = 1/(2T)   -T < t < T
    #         = 0         otherwise
    # with T <--> `thalf`
    return np.sin(omega * thalf) / (omega * thalf)

def stf_cosine_boxcar(omega, thalf, ratio=0.1):
    return np.pi**2 * np.cos(thalf*ratio*omega)*np.sin(thalf*omega*(ratio-1))/((ratio-1)*thalf*omega*(np.pi-2*ratio*thalf*omega)*(np.pi+2*ratio*thalf*omega))

def stf_ricker(omega, twidth):
    """
    Ricker wavelet.
    
    This function implements the Fourier transform of
    
    f(t,T) = 2/(sqrt(3T).pi^(1/4)) . (1-(t/T)^2) . exp(-t^2/ (2T^2))
    
    which is equivalent to scipy.signal.ricker with that function's `a` <--> `twidth`.
    
    :param complex omega: Frequency at which evaluation is required (rad/s)
    :param float twidth:  Width of wavelet. This is the 'standard deviation' parameter of the
                          Gaussian from which the Ricker wavelet is derived. The peak frequency
                          of the wavelet is related to twidth by:
                          
                          f_M = 1/ (sqrt(2) pi twidth)     Hz   
                          or
                          w_M = sqrt(2)/twidth             rad/s
     :returns: Amplitude of the filter.               
                          
    """
    return 2*np.sqrt(2/3)*np.exp(-0.5*(twidth*omega)**2)*(np.pi**0.25)*(twidth**2.5)*(omega**2)

def clp_filter(w, w0, w1):
    """
    Cosine low-pass filter.
    
    :param complex w: Frequency a t which evaluation is required (rad/s)
    :param float w0: Corner frequency for start of taper; at frequencies below this the filter has no impact.
    :param float w1: Corner frequency for end of taper; frequencies above this are stopped.

    :returns: Amplitude of the filter

    """
    if w1 <= w0:
        raise ValueError(
            "clp_filter upper corner frequency must be greater than lower corner!"
        )
    if np.real(w) < w0:
        return 1.0
    elif np.real(w) < w1:
        return 0.5 * (1 + np.cos(np.pi * (w - w0) / (w1 - w0)))
    else:
        return 0


def make_moment_tensor(strike, dip, rake, M0, eta=0, xtr=0):
    """
    Construct moment tensor from strike/dip/rake. Copied from F77 routine `makemom`
    of unknown origin. (J.H. Woodhouse?)

    :param float strike: strike azimuth (clockwise from N).
            Convention is that the fault dips
            to the right when looking along the strike azimuth.
    :param float dip: fault dip
    :param float rake: 'rake' angle
            Convention is that:
            rlam=  0, del=90  --> left lateral strike-slip
            rlam= 90, del=45  --> thrust fault
            rlam=-90, del=45  --> normal fault
    :param float M0: Scalar moment (i.e. the average of
            the largest eigenvalue and the negative of the smallest
            eigenvalue of the moment tensor).
    :param float eta: ratio of the intermediate eigenvalue to the
            scalar moment. For a double couple, eta=0.
    :param float xtr: ratio of the trace of the moment tensor to the
            scalar moment. If there is no volumetric component, xtr=0.

     Thus the three eigenvalues, in increasing order (P,N,T) are
       evp=scmom*(-1.-.5*eta+.5*xtr)
       evn=scmom*(       eta       )
       evt=scmom*( 1.-.5*eta+.5*xtr)

    :returns: 3x3 array, moment tensor in spherical polar coordinates (GCMT convention)
    """
    strike_r = np.deg2rad(strike)
    dip_r = np.deg2rad(dip)
    rake_r = np.deg2rad(rake)
    sv = np.array([0.0, -np.cos(strike_r), np.sin(strike_r)])
    d = np.array(
        [
            -np.sin(dip_r),
            np.cos(dip_r) * np.sin(strike_r),
            np.cos(dip_r) * np.cos(strike_r),
        ]
    )
    n = np.array(
        [
            np.cos(dip_r),
            np.sin(dip_r) * np.sin(strike_r),
            np.sin(dip_r) * np.cos(strike_r),
        ]
    )
    e = sv * np.cos(rake_r) - d * np.sin(rake_r)
    b = np.cross(e, n)
    t = (e + n) / np.sqrt(2)
    p = (e - n) / np.sqrt(2)
    ev = M0 * np.array([-1 - 0.5 * eta + 0.5 * xtr, eta, 1 - 0.5 * eta + 0.5 * xtr])
    fmom = np.zeros(6)
    fmom[:3] = ev[0] * p**2 + ev[1] * b**2 + ev[2] * t**2
    fmom[3] = ev[0] * p[0] * p[1] + ev[1] * b[0] * b[1] + ev[2] * t[0] * t[1]
    fmom[4] = ev[0] * p[0] * p[2] + ev[1] * b[0] * b[2] + ev[2] * t[0] * t[2]
    fmom[5] = ev[0] * p[1] * p[2] + ev[1] * b[1] * b[2] + ev[2] * t[1] * t[2]
    M = np.array(
        [
            [fmom[0], fmom[3], fmom[4]],
            [fmom[3], fmom[1], fmom[5]],
            [fmom[4], fmom[5], fmom[2]],
        ]
    )
    return M


def rtf2xyz(M):
    """Convert a moment tensor specified in an (r,theta,phi) coordinate system
    into one specified in an (x,y,z-up) system"""
    # M2 = np.zeros_like(M)
    # M2[0:2,0:2] = M[1:3,1:3]
    # M2[0:2,2] = M[0,1:3]
    # M2[2,0:2] = M[1:3,0]
    # M2[2,2] = M[0,0]
    # # M2[1,:]*=-1
    # # M2[:,1]*=-1

    M2 = np.array(
        [
            [M[2, 2], -M[2, 1], M[2, 0]],
            [-M[1, 2], M[1, 1], -M[1, 0]],
            [M[0, 2], -M[0, 1], M[0, 0]],
        ]
    )
    return M2


def latlon2xy(lat, lon, centre_lat, centre_lon, radius=6371.0):
    """
    Convert latitude/longitude to a local Cartesian coordinate system assuming spherical Earth
    :param float lat:
    :param float lon: Coordinates of point of interest
    :param float centre_lat:
    :param float centre_lon: Coordinates of origin of Cartesian system
    :param float radius: Radius of spherical planet
    :returns: (x,y) Cartesian coordinates
    """
    dlat = np.deg2rad(lat - centre_lat)
    dlon = np.deg2rad(lon - centre_lon)
    x = radius * np.cos(np.deg2rad(centre_lat)) * dlon
    y = radius * dlat
    return x, y

def earth_flattening_transformation(spherical_model_table, l, radius):
    """
    Apply the earth-flattening transformation (following Chapman & Orcutt, 
    The computation of body wave synthetic seismograms in laterally 
    homogeneous media, Rev. Geophys., 1985) to an earth model.

    Note that the transformation is approximate, with behaviour governed by
    the parameter l. A discussion of this can be found following eq.(70) in
    the Chapman & Orcutt paper. 

    Also, note that it may be necessary to apply transformations to other 
    quantities e.g. the depths of sources and buried receivers.  
   
    :param list spherical_model_table: The model as expressed in a spherical
        geometry. The model table should be given in a manner similar to that 
        expected by :py:class:`LayeredStructureModel` when `interface_depth_form=True`.
        Provide a list of tuples `(depth, vp, vs, rho)` where ``depth`` is the 
        depth (km) of the interface defining the top of the layer, and vp, vs and rho
        are the corresponding material parameters.
    :param float l: Parameter governing the detailed approximation used; see the 
        Chapman & Orcutt paper for more details. "A common choice is l=3".
    :param float radius: The radius (km) of the planet being modelled.
    
    :return: list, ``flattened_model_table``, in form suitable for passing to
        :py:class:`LayeredStructureModel` with `interface_depth_form=True`.
    """
    flattened_model = []
    for layer in spherical_model_table:
        interface_depth, vp_sph, vs_sph, rho_sph = layer
        if interface_depth>=radius: raise ValueError("Model layer depths inconsistent with radius of planet!")
        r = (radius-interface_depth)
        z = -radius*np.log(r/radius)
        vp_flat = (radius/r)*vp_sph
        vs_flat = (radius/r)*vs_sph
        rho_flat = ((r/radius)**(l+2)) * rho_sph
        flattened_model+=[(z, vp_flat, vs_flat, rho_flat)]
    return flattened_model




import numpy as np
from lcbuilder.helper import LcbuilderHelper
from astropy import units as u
from astropy.modeling.models import BlackBody

'''Calculates the Habitability Zone of a star based on the Kopparapu et al (2013) equations. These equations are only
valid for stars between 2600 K < Teff < 7200 K.'''


class HabitabilityCalculator:
    sun_luminosity = 1.
    G = 6.674e-11  # m3 kg-1 s-2
    ##
    ## Stellar flux coefficients (table 3 from kopparapu et al 2013)
    ##
    e_end = 1.00
    Nout = 10000
    e = np.linspace(0.0001, e_end, Nout, endpoint=False)

    def __init__(self):
        pass

    # equation (2) from kopparapu et al 2013, for non ecentric orbits
    def __seff(self, Seff_sun, a, b, c, d, t_star):
        Seff = Seff_sun + a * t_star + b * t_star ** 2 + c * t_star ** 3 + d * t_star ** 4
        return Seff

    # equation (3) from kopparapu et al 2013, for non ecentric orbits
    def __dis(self, Seff, luminosity):
        return (luminosity / self.sun_luminosity / Seff) ** 0.5

    # having equations (3) y (4) for eccentric orbits from kopparapu et al 2013
    def __seff_prime(self, A, e):
        return A / np.sqrt(1. - e ** 2)

    def calculate_hz(self, t_eff, luminosity):
        """
        Calculates the habitable zone ranges in astronomical units
        @param t_eff: the stellar effective temperature
        @param luminosity: the stellar luminosity in sun luminosities
        @return: a tuple of size 4 with the recent venus, moist greenhouse, maximum greenhouse and early mars orbital
        semi-major axises for the given star parameters.
        """
        if t_eff < 2600 or t_eff > 7200:
            return None
        t_star = t_eff - 5780
        # Recent Venus
        s_eff_rv = 1.7763
        a_rv = 1.4335e-4
        b_rv = 3.3954e-9
        c_rv = -7.6364e-12
        d_rv = -1.1950e-15
        Seff_rv = self.__seff(s_eff_rv, a_rv, b_rv, c_rv, d_rv, t_star)
        Dis_rv = self.__dis(Seff_rv, luminosity)
        Seff_prime_rv = self.__seff_prime(Seff_rv, self.e)
        Dis_prime_rv = self.__dis(Seff_prime_rv, luminosity)
        # Runaway Greenhouse
        s_eff_rg = 1.0385
        a_rg = 1.2456e-4
        b_rg = 1.4612e-8
        c_rg = -7.6345e-12
        d_rg = -1.7511e-15
        Seff_rg = self.__seff(s_eff_rg, a_rg, b_rg, c_rg, d_rg, t_star)
        Dis_rg = self.__dis(Seff_rg, luminosity)
        Seff_prime_rg = self.__seff_prime(Seff_rg, self.e)
        Dis_prime_rg = self.__dis(Seff_prime_rg, luminosity)
        # Moist Greenhouse
        s_eff_mog = 1.0146
        a_mog = 8.1884e-5
        b_mog = 1.9394e-9
        c_mog = -4.3618e-12
        d_mog = -6.8260e-16
        Seff_mog = self.__seff(s_eff_mog, a_mog, b_mog, c_mog, d_mog, t_star)
        Dis_mog = self.__dis(Seff_mog, luminosity)
        Seff_prime_mog = self.__seff_prime(Seff_mog, self.e)
        Dis_prime_mog = self.__dis(Seff_prime_mog, luminosity)
        # Maximun Greenhouse
        s_eff_mag = 0.3507
        a_mag = 5.9578e-5
        b_mag = 1.6707e-9
        c_mag = -3.0058e-12
        d_mag = -5.1925e-16
        Seff_mag = self.__seff(s_eff_mag, a_mag, b_mag, c_mag, d_mag, t_star)
        Dis_mag = self.__dis(Seff_mag, luminosity)
        Seff_prime_mag = self.__seff_prime(Seff_mag, self.e)
        Dis_prime_mag = self.__dis(Seff_prime_mag, luminosity)
        # Early Mars
        s_eff_em = 0.3207
        a_em = 5.4471e-5
        b_em = 1.5275e-9
        c_em = -2.1709e-12
        d_em = -3.8282e-16
        Seff_em = self.__seff(s_eff_em, a_em, b_em, c_em, d_em, t_star)
        Dis_em = self.__dis(Seff_em, luminosity)
        Seff_prime_em = self.__seff_prime(Seff_em, self.e)
        Dis_prime_em = self.__dis(Seff_prime_em, luminosity)
        return [Dis_rv, Dis_mog, Dis_mag, Dis_em]

    def calculate_hz_periods(self, t_eff, luminosity, mass):
        """
        Calculates the habitable zone ranges in periods
        @param t_eff: the stellar effective temperature
        @param luminosity: the stellar luminosity in sun luminosities
        @param mass: the stellar mass in sun masses
        @return: a tuple of size 4 with the recent venus, moist greenhouse, maximum greenhouse and early mars orbital
        periods for the given star parameters.
        """
        aus = self.calculate_hz(t_eff, luminosity)
        if aus is None:
            return None
        return [self.au_to_period(mass, au) for au in aus]

    def au_to_period(self, mass, au):
        """
        Calculates the orbital period for the semi-major axis assuming a circular orbit.
        @param mass: the stellar mass
        @param au: the semi-major axis in astronomical units.
        @return: the period in days
        """
        mass_kg = mass * 2.e30
        a = au * 1.496e11
        return ((a ** 3) * 4 * (np.pi ** 2) / self.G / mass_kg) ** (1. / 2.) / 3600 / 24

    def calculate_semi_major_axis(self, period, star_mass):
        period_seconds = period * 24. * 3600.
        mass_kg = star_mass * 2.e30
        a1 = (self.G * mass_kg * period_seconds ** 2 / 4. / (np.pi ** 2)) ** (1. / 3.)
        return a1 / 1.496e11

    def calculate_semi_major_axis_with_err(self, period, period_low_err, period_up_err, star_mass, star_mass_low_err,
                                           star_mass_up_err):
        a = self.calculate_semi_major_axis(period, star_mass)
        constant = (self.G / 4 / np.pi ** 2) ** (1 / 3)
        a_low_err = self.calculate_semi_major_axis_err(constant, period, period_low_err, star_mass, star_mass_low_err)
        a_up_err = self.calculate_semi_major_axis_err(constant, period, period_up_err, star_mass, star_mass_up_err)
        return a, a_low_err, a_up_err

    def calculate_semi_major_axis_err(self, constant, period, period_err, star_mass, star_mass_err):
        period_seconds = period * 24. * 3600.
        period_err_seconds = period_err * 24. * 3600.
        star_mass_kg = star_mass * 2.e30
        star_mass_err_kg = star_mass_err * 2.e30
        return constant * np.sqrt(
            (((star_mass_kg * period_seconds ** 2) ** (-2 / 3) / 3 * period_seconds ** 2) * star_mass_err_kg) ** 2 +
            (((star_mass_kg * period_seconds ** 2) ** (
                        -2 / 3) * 2 / 3 * star_mass_kg * period_seconds) * period_err_seconds) ** 2
        ) / 1.496e11

    def calculate_teq(self, star_mass, star_mass_low_err, star_mass_up_err, star_radius, star_radius_low_err,
                      star_radius_up_err,
                      period, period_low_err, period_up_err, star_teff, star_teff_low_err, star_teff_up_err):
        a, a_low_err, a_up_err = self.calculate_semi_major_axis_with_err(period, period_low_err, period_up_err,
                                                                         star_mass, star_mass_low_err, star_mass_up_err)
        a_rsun = LcbuilderHelper.convert_from_to(a, u.au, u.R_sun)
        a_low_err_rsun = LcbuilderHelper.convert_from_to(a_low_err, u.au, u.R_sun)
        a_up_err_rsun = LcbuilderHelper.convert_from_to(a_up_err, u.au, u.R_sun)
        constant = 1 / 4 ** 0.25
        teq = constant * star_teff * star_radius / a_rsun ** 0.5
        teq_low_err = self._calculate_teq_err(constant, a_rsun, a_low_err_rsun, star_radius, star_radius_low_err,
                                              star_teff, star_teff_low_err)
        teq_up_err = self._calculate_teq_err(constant, a_rsun, a_up_err_rsun, star_radius, star_radius_up_err,
                                             star_teff, star_teff_up_err)
        return teq, teq_low_err, teq_up_err

    def _calculate_teq_err(self, constant, a, a_err, star_radius, star_radius_err, star_teff, star_teff_err):
        return constant * np.sqrt(
            ((star_teff / a) * star_radius_err) ** 2 +
            ((star_radius / a) * star_teff) ** 2 +
            ((-star_teff / a ** 2 * star_radius) * a_err) ** 2
        )

    def get_TSM_scale_factor(self, radius):
        if radius <= 1.5:
            return 0.19
        elif radius <= 2.75:
            return 1.26
        elif radius <= 4:
            return 1.28
        else:
            return 1.15

    def calculate_TSM(self, planet_radius, planet_radius_low_err, planet_radius_up_err, planet_mass,
                      planet_mass_low_err, planet_mass_up_err,
                      t_eq, t_eq_low_err, t_eq_up_err, star_radius, star_radius_low_err, star_radius_up_err,
                      star_j_mag):
        """
        Calculates the Transmission Spectroscopy Metric (TSM).
        :param planet_radius: planet radius in earth radii
        :param planet_radius_low_err: planet radius lower uncertainty
        :param planet_radius_up_err: planet radius upper uncertainty
        :param planet_mass: planet mass
        :param planet_mass_low_err: planet mass lower uncertainty
        :param planet_mass_up_err: planet mass upper uncertainty
        :param t_eq: planet equilibrium temperature
        :param t_eq_low_err: teq lower uncertainty
        :param t_eq_up_err: teq upper uncertaint
        :param star_radius: star radius in sun radii
        :param star_radius_low_err: star radius lower uncertainty
        :param star_radius_up_err: star radius upper uncertainty
        :param star_j_mag: star J magnitude
        :return: the tsm and its lower and upper uncertainties
        """
        constant = self.get_TSM_scale_factor(planet_radius) * 10 ** (-star_j_mag / 5)
        tsm = constant * t_eq * planet_radius ** 3 / (planet_mass * star_radius ** 2)
        tsm_up_err = self._calculate_TSM_err(constant, planet_radius, planet_radius_up_err, planet_mass,
                                             planet_mass_up_err, t_eq, t_eq_up_err,
                                             star_radius, star_radius_up_err)
        tsm_low_err = self._calculate_TSM_err(constant, planet_radius, planet_radius_low_err, planet_mass,
                                              planet_mass_low_err, t_eq, t_eq_low_err,
                                              star_radius, star_radius_low_err)
        return tsm, tsm_low_err, tsm_up_err

    def _calculate_TSM_err(self, constant, planet_radius, planet_radius_err, planet_mass, planet_mass_err, t_eq,
                           t_eq_err, star_radius, star_radius_err):
        return constant * np.sqrt(((planet_mass * planet_radius ** 3 / (
                    planet_mass * star_radius ** 2) ** 2 * star_radius ** 2) * t_eq_err) ** 2 +
                                  ((t_eq * 3 / (
                                              planet_mass * star_radius ** 2) ** 2 * planet_radius ** 2 * planet_mass * star_radius ** 2) * planet_radius_err) ** 2 +
                                  ((-(t_eq / (
                                              planet_mass * star_radius ** 2) ** 2 * planet_radius ** 3 * star_radius ** 2)) * planet_mass_err) ** 2 +
                                  ((-t_eq * 2 / (
                                              planet_mass * star_radius ** 2) ** 2 * planet_radius ** 3 * planet_mass * star_radius) * star_radius_err) ** 2)

    def calculate_ESM(self, depth, depth_low_err, depth_up_err, teq, teq_low_err, teq_up_err, star_teff,
                      star_teff_low_err, star_teff_up_err, star_k_mag):
        """
        Calculates Emission Spectroscopy Metric (ESM). The uuncertainty is computed from the depth error and the black body difference between the value
        obtained for the teff and teq and their uncertainties.
        :param depth: the depth in ppts
        :param depth_low_err: depth lower uncertainty
        :param depth_up_err: depth upper uncertainty
        :param teq: planet equilibrium temperature
        :param teq_low_err: teq lower uncertainty
        :param teq_up_err: teq upper uncertainty
        :param star_teff: star effective temperature
        :param star_teff_low_err: teff lower uncertainty
        :param star_teff_up_err: teff upper uncertainty
        :param star_k_mag: star K magnitude
        :return: epm and its up and low uncertainties
        """
        depth_ppm = 10 ** 3 * depth
        ESM_bb_Tday = BlackBody(temperature=1.1 * teq * u.K)
        ESM_bb_Teff = BlackBody(temperature=star_teff * u.K)
        ESM_bb_Tday_low = BlackBody(temperature=1.1 * (teq - teq_low_err) * u.K)
        ESM_bb_Teff_low = BlackBody(temperature=(star_teff - star_teff_low_err) * u.K)
        ESM_bb_Tday_up = BlackBody(temperature=1.1 * (teq + teq_up_err) * u.K)
        ESM_bb_Teff_up = BlackBody(temperature=(star_teff + star_teff_up_err) * u.K)
        wavelength = 7.5 * u.micron
        epm = 4.29 * (ESM_bb_Tday(wavelength) / ESM_bb_Teff(wavelength)).value * depth_ppm * 10 ** (-star_k_mag / 5)
        epm_teff_low = 4.29 * (ESM_bb_Tday_low(wavelength) / ESM_bb_Teff_low(wavelength)).value * depth_ppm * 10 ** (
                    -star_k_mag / 5)
        epm_teff_up = 4.29 * (ESM_bb_Tday_up(wavelength) / ESM_bb_Teff_up(wavelength)).value * depth_ppm * 10 ** (
                    -star_k_mag / 5)
        return epm, epm - epm_teff_low + depth_low_err, epm_teff_up - epm + depth_up_err

    def calculate_semi_amplitude(self, period: float, period_low_err: float, period_up_err: float, planet_mass: float,
                                 planet_mass_low_err: float, planet_mass_up_err: float,
                                 star_mass: float, star_mass_low_err: float, star_mass_up_err: float,
                                 eccentricity: float = 0, inclination: float = np.pi / 2):
        """
        Calclates the estimated Radial Velocity semi amplitude in m/s
        :param period: planet period in days
        :param period_low_err: period lower uncertainty
        :param period_up_err: period upper uncertainty
        :param planet_mass: planet mass in earth masses
        :param planet_mass_low_err: planet mass lower uncertainty
        :param planet_mass_up_err: planet mass upper uncertainty
        :param star_mass: star mass in solar masses
        :param star_mass_low_err: star mass lower uncertainty
        :param star_mass_up_err: star mass upper uncertainty
        :param eccentricity: planet eccentricity in radians
        :param inclination: planet inclination in radians
        :return: the estimated semi amplitude in m/s and its lower and upper uncertainties
        """
        planet_mass = LcbuilderHelper.convert_from_to(planet_mass, u.M_earth, u.kg)
        planet_mass_up_err = LcbuilderHelper.convert_from_to(planet_mass_up_err, u.M_earth, u.kg)
        planet_mass_low_err = LcbuilderHelper.convert_from_to(planet_mass_low_err, u.M_earth, u.kg)
        star_mass = LcbuilderHelper.convert_from_to(star_mass, u.M_sun, u.kg)
        star_mass_up_err = LcbuilderHelper.convert_from_to(star_mass_up_err, u.M_sun, u.kg)
        star_mass_low_err = LcbuilderHelper.convert_from_to(star_mass_low_err, u.M_sun, u.kg)
        period = LcbuilderHelper.convert_from_to(period, u.day, u.s)
        period_up_err = LcbuilderHelper.convert_from_to(period_up_err, u.day, u.s)
        period_low_err = LcbuilderHelper.convert_from_to(period_low_err, u.day, u.s)
        constant = (2 * np.pi * HabitabilityCalculator.G) ** (1 / 3) * np.sin(inclination) * (
                    1 / (np.sqrt(1 - eccentricity ** 2)))
        semi_amplitude = constant * (1 / period) ** (1 / 3) * planet_mass / ((star_mass + planet_mass) ** (2 / 3))
        semi_amplitude_low_err = self._calculate_semi_amplitude_err(period, period_low_err, planet_mass,
                                                                    planet_mass_low_err, star_mass, star_mass_low_err,
                                                                    constant)
        semi_amplitude_up_err = self._calculate_semi_amplitude_err(period, period_up_err, planet_mass,
                                                                   planet_mass_up_err, star_mass, star_mass_up_err,
                                                                   constant)
        return semi_amplitude, semi_amplitude_low_err, semi_amplitude_up_err

    def _calculate_semi_amplitude_err(self, period: float, period_err: float, planet_mass: float,
                                      planet_mass_err: float, star_mass: float, star_mass_err: float, constant: float):
        return constant * np.sqrt(
            ((1 / period) ** (1 / 3) * ((star_mass + planet_mass) ** (2 / 3) + (star_mass + planet_mass) ** (-1 / 3) * (
                        -2 / 3) * planet_mass) * (star_mass + planet_mass) ** (-4 / 3) * planet_mass_err) ** 2 +
            (((1 / period) ** (-2 / 3) * (-1 / 3 / period ** 2 * planet_mass * (star_mass + planet_mass) ** (
                        -2 / 3))) * period_err) ** 2 +
            (((star_mass + planet_mass) ** (-5 / 3) * (-2) / 3 * (1 / period) ** (
                        1 / 3) * planet_mass) * star_mass_err) ** 2
        )

    def calculate_hz_score(self, t_eff, star_mass, luminosity, period):
        """
        Returns the semi-major axis and the HZ Area [I=Inner, HZ-IO=Habitable Zone (Inner Optimistic),
        HZ=Habitable Zone, HZ-OO=Habitable Zone (Outer Optimistic)
        @param t_eff: the star effective temperature
        @param star_mass: the star mass in sun masses
        @param luminosity: the star luminosity in sun luminosities
        @param period: the period to guess the semi-major axis
        @return: a tuple of semi-major axis and hz position string.
        """
        hz = self.calculate_hz(t_eff, luminosity) if t_eff is not None and not np.isnan(t_eff) else None
        a1_au = self.calculate_semi_major_axis(period, star_mass) if star_mass is not None and not np.isnan(star_mass) \
            else np.nan
        if np.isnan(a1_au) or hz is None:
            hz_position = "-"
        elif a1_au < hz[0]:
            hz_position = 'I'
        elif a1_au >= hz[0] and a1_au < hz[1]:
            hz_position = 'HZ-IO'
        elif a1_au >= hz[1] and a1_au < hz[2]:
            hz_position = 'HZ'
        elif a1_au >= hz[2] and a1_au < hz[3]:
            hz_position = 'HZ-OC'
        else:
            hz_position = 'O'
        return a1_au, hz_position

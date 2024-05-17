import logging
from typing import Optional

import lightkurve
import numpy as np
import astropy.io.fits as astropy_fits
import re
import pandas as pd
from abc import ABC, abstractmethod

from lightkurve import LightCurveCollection

from lcbuilder import constants
from lcbuilder.star.EpicStarCatalog import EpicStarCatalog
from lcbuilder.star.KicStarCatalog import KicStarCatalog
from lcbuilder.star.TicStarCatalog import TicStarCatalog


class LightcurveBuilder(ABC):
    OBJECT_ID_REGEX = "^(KIC|TIC|EPIC)[-_ ]([0-9]+)$"
    NUMBERS_REGEX = "[0-9]+$"

    def __init__(self):
        self.star_catalogs = {}
        self.star_catalogs[constants.MISSION_ID_KEPLER] = KicStarCatalog()
        self.star_catalogs[constants.MISSION_ID_KEPLER_2] = EpicStarCatalog()
        self.star_catalogs[constants.MISSION_ID_TESS] = TicStarCatalog()
        self.authors = {}
        self.authors[constants.MISSION_KEPLER] = constants.MISSION_KEPLER
        self.authors[constants.MISSION_K2] = constants.K2_AUTHOR
        self.authors[constants.MISSION_TESS] = constants.SPOC_AUTHOR
        self.authors[constants.MISSION_TESS + "_long"] = constants.TESS_SPOC_AUTHOR

    @abstractmethod
    def build(self, object_info, sherlock_dir, caches_root_dir):
        pass

    def parse_object_id(self, object_id):
        if object_id is None:
            return constants.MISSION_TESS, constants.MISSION_ID_TESS, None
        object_id_parsed = re.search(self.OBJECT_ID_REGEX, object_id)
        if object_id_parsed is None:
            return None, None, None
        mission_prefix = object_id[object_id_parsed.regs[1][0]:object_id_parsed.regs[1][1]]
        id = object_id[object_id_parsed.regs[2][0]:object_id_parsed.regs[2][1]]
        if mission_prefix == constants.MISSION_ID_KEPLER:
            mission = constants.MISSION_KEPLER
        elif mission_prefix == constants.MISSION_ID_KEPLER_2:
            mission = constants.MISSION_K2
        elif mission_prefix == constants.MISSION_ID_TESS:
            mission = constants.MISSION_TESS
        else:
            mission = None
        return mission, mission_prefix, int(id)

    @staticmethod
    def sort_lc_data(lcf: LightCurveCollection, mission_prefix: str):
        if mission_prefix == constants.MISSION_ID_KEPLER:
            args = np.argsort(lcf.quarter)
        elif mission_prefix == constants.MISSION_ID_KEPLER_2:
            args = np.argsort(lcf.campaign)
        elif mission_prefix == constants.MISSION_ID_TESS:
            args = np.argsort(lcf.sector)
        return args

    @staticmethod
    def search_lightcurve(target_name: str, mission_prefix: str, mission: str, cadence: int | str, sectors: list,
                          quarters: list, campaigns: list, author: str, download_dir: str, quality_bitmask: int | str,
                          sectors_limit: Optional[int] = None):
        lcf_search_results = lightkurve.search_lightcurve(target_name, mission=mission, exptime=cadence,
                                                          sector=sectors, quarter=quarters,
                                                          campaign=campaigns, author=author, limit=sectors_limit)
        lcf = lcf_search_results.download_all(download_dir=download_dir,
                                              quality_bitmask=quality_bitmask)
        if lcf == None:
            raise ValueError(
                f"There are no LightCurves for the given mission {mission}, author {author}, cadence {cadence} and sectors {sectors}")
        sort_indexes = LightcurveBuilder.sort_lc_data(lcf, mission_prefix)
        return lcf[sort_indexes]

    @staticmethod
    def search_tpf(target_name: str, mission_prefix: str, mission: str, cadence: Optional[int | str],
                   sectors: Optional[list], quarters: Optional[list], campaigns: Optional[list],
                   author: Optional[str], download_dir: Optional[str], quality_bitmask: Optional[int | str],
                   cutout_size: Optional[tuple], sectors_limit: Optional[int] = None):
        tpfs = lightkurve.search_targetpixelfile(target_name, mission=mission, exptime=cadence,
                                                 sector=sectors, quarter=quarters,
                                                 campaign=campaigns, author=author, limit=sectors_limit) \
            .download_all(download_dir=download_dir, cutout_size=cutout_size, quality_bitmask=quality_bitmask)
        if tpfs == None or len(tpfs) == 0:
            tpfs = lightkurve.search_tesscut(target_name, sectors).download_all(download_dir=download_dir,
                                                                                cutout_size=cutout_size,
                                                                                quality_bitmask=quality_bitmask)
        sort_indexes = LightcurveBuilder.sort_lc_data(tpfs, mission_prefix)
        return tpfs[sort_indexes]

    def extract_lc_data(self, lcf: LightCurveCollection):
        fit_files = [astropy_fits.open(lcf.filename) for lcf in lcf]
        time = []
        flux = []
        flux_err = []
        background_flux = []
        quality = []
        centroids_x = []
        centroids_y = []
        motion_x = []
        motion_y = []
        for fit_file in fit_files:
            time.append(fit_file[1].data['TIME'])
            try:
                flux.append(fit_file[1].data['PDCSAP_FLUX'])
                flux_err.append(fit_file[1].data['PDCSAP_FLUX_ERR'])
            except:
                # QLP curves that can contain KSPSAP_FLUX or DET_FLUX: https://tess.mit.edu/qlp/
                try:
                    flux.append(fit_file[1].data['KSPSAP_FLUX'])
                    flux_err.append(fit_file[1].data['KSPSAP_FLUX_ERR'])
                except:
                    flux.append(fit_file[1].data['DET_FLUX'])
                    flux_err.append(fit_file[1].data['DET_FLUX_ERR'])
            background_flux.append(fit_file[1].data['SAP_BKG'])
            try:
                quality.append(fit_file[1].data['QUALITY'])
            except KeyError:
                logging.info("QUALITY info is not available.")
                quality.append(np.full(len(fit_file[1].data['TIME']), np.nan))
            try:
                centroids_x.append(fit_file[1].data['MOM_CENTR1'])
                centroids_y.append(fit_file[1].data['MOM_CENTR2'])
                motion_x.append(fit_file[1].data['POS_CORR1'])
                motion_y.append(fit_file[1].data['POS_CORR2'])
            except:
                logging.warning("No centroid and position data in light curve")
        time = np.concatenate(time)
        flux = np.concatenate(flux)
        flux_err = np.concatenate(flux_err)
        background_flux = np.concatenate(background_flux)
        quality = np.concatenate(quality)
        if len(centroids_x) > 0:
            centroids_x = np.concatenate(centroids_x)
            centroids_y = np.concatenate(centroids_y)
            motion_x = np.concatenate(motion_x)
            motion_y = np.concatenate(motion_y)
        lc_data = pd.DataFrame(columns=['time', 'flux', 'flux_err', 'background_flux', 'quality', 'centroids_x',
                                        'centroids_y', 'motion_x', 'motion_y'])
        lc_data['time'] = time
        lc_data['flux'] = flux
        lc_data['flux_err'] = flux_err
        lc_data['background_flux'] = background_flux
        lc_data['quality'] = quality
        if len(centroids_x) > 0:
            lc_data['centroids_x'] = centroids_x
            lc_data['centroids_y'] = centroids_y
            lc_data['motion_x'] = motion_x
            lc_data['motion_y'] = motion_y
        lc_data.dropna(subset=['time'], inplace=True)
        for fit_file in fit_files:
            fit_file.close()
        return lc_data

    def extract_lc_data_from_df(self, lc_df: pd.DataFrame):
        time = []
        flux = []
        flux_err = []
        background_flux = []
        quality = []
        centroids_x = []
        centroids_y = []
        motion_x = []
        motion_y = []
        if '#time' in lc_df.columns:
            time = lc_df['#time'].to_numpy()
        if 'flux' in lc_df.columns:
            flux = lc_df['flux'].to_numpy()
        if 'flux_err' in lc_df.columns:
            flux_err = lc_df['flux_err'].to_numpy()
        if 'quality' in lc_df.columns:
            quality = lc_df['quality'].to_numpy()
        if 'centroid_x' in lc_df.columns:
            centroids_x = lc_df['centroid_x'].to_numpy()
        if 'centroid_y' in lc_df.columns:
            centroids_y = lc_df['centroid_y'].to_numpy()
        if 'motion_x' in lc_df.columns:
            motion_x = lc_df['motion_x'].to_numpy()
        if 'motion_y' in lc_df.columns:
            motion_y = lc_df['motion_y'].to_numpy()
        if 'background_flux' in lc_df.columns:
            background_flux = lc_df['background_flux'].to_numpy()
        lc_data = pd.DataFrame(columns=['time', 'flux', 'flux_err', 'background_flux', 'quality', 'centroids_x',
                                        'centroids_y', 'motion_x', 'motion_y'])
        lc_data['time'] = time
        lc_data['flux'] = flux
        lc_data['flux_err'] = flux_err
        if len(background_flux) > 0:
            lc_data['background_flux'] = background_flux
        if len(quality) > 0:
            lc_data['quality'] = quality
        if len(centroids_x) > 0:
            lc_data['centroids_x'] = centroids_x
            lc_data['centroids_y'] = centroids_y
            lc_data['motion_x'] = motion_x
            lc_data['motion_y'] = motion_y
        lc_data.dropna(subset=['time'], inplace=True)
        return lc_data

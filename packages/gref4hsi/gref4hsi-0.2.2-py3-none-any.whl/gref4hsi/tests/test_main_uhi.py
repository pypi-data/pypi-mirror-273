from collections import namedtuple
import configparser
import os
import sys

import numpy as np

# Detect OS and set FPs
if os.name == 'nt':
    # Windows OS
    base_fp = 'D:'
    home = 'C:/Users/haavasl'
elif os.name == 'posix':
    # This Unix-like systems inl. Mac and Linux
    base_fp = '/media/haavasl/Expansion'
    home = '/home/haavasl'


# Use this if working with the github repo to do quick changes to the module
module_path = os.path.join(home, 'VsCodeProjects/gref4hsi/')
if module_path not in sys.path:
    sys.path.append(module_path)

from gref4hsi.utils import parsing_utils, uhi_parsing_utils
from gref4hsi.scripts import georeference, orthorectification
from gref4hsi.utils import visualize
from gref4hsi.utils.config_utils import prepend_data_dir_to_relative_paths, customize_config

# D:\HyperspectralDataAll\UHI\2020-07-01-14-40-15-ArcticSeaIce-Ben-Lange
DATA_DIR = os.path.join(base_fp, "HyperspectralDataAll/UHI/2020-07-01-14-40-15-ArcticSeaIce-Ben-Lange/")

# The configuration file stores the settings for georeferencing
config_file_mission = os.path.join(DATA_DIR, 'configuration.ini')


config_path_template = os.path.join(home, 'VsCodeProjects/gref4hsi/data/config_examples/configuration_uhi.ini')

# Copies the template to config_file_mission and sets up the necessary directories
prepend_data_dir_to_relative_paths(config_path=config_path_template, DATA_DIR=DATA_DIR)

# Non-default settings
custom_config = {'General':
                    {'mission_dir': DATA_DIR,
                    'model_export_type': 'dem_file', # Infer seafloor structure from altimeter recordings
                    'max_ray_length': 5,
                    'lab_cal_dir': os.path.join(base_fp, 'HyperspectralDataAll/UHI/Lab_Calibration_Data/NP')}, # Max distance in meters from UHI to seafloor

                'Coordinate Reference Systems': 
                    {'proj_epsg' : 3395, # The projected CRS for orthorectified data (an arctic CRS)
                    'geocsc_epsg_export' : 4978, # 3D cartesian system for earth consistent with GPS frame (but inconsistent with eurasian techtonic plate)
                    'dem_epsg' : 3395, # (Optional) If you have a DEM this can be used
                    'pos_epsg_orig' : 4978}, # The CRS of the positioning data we deliver to the georeferencing

                'Relative Paths':
                    {'dem_folder': 'Input/GIS/'}, # Using altimeter, we generate one DEM per transect chunk
                
                'Absolute Paths':
                    {'geoid_path': os.path.join(home, "VsCodeProjects/gref4hsi/data/world/geoids/egm08_25.gtx")}, # Using altimeter, we generate one DEM per transect chunk

                'Orthorectification':
                    {'resample_rgb_only': True, # Good choice for speed
                    'resolutionhyperspectralmosaic': 0.01, # 1 cm
                    'raster_transform_method': 'north_east'},
                
                'HDF.raw_nav': {'altitude': 'raw/nav/altitude',
                    'rotation_reference_type' : 'eul_ZYX', # The vehicles orientations are used as Yaw, Pitch, Roll
                    'is_global_rot' : False, # The vehicles orientations are used as Yaw, Pitch, Roll
                    'eul_is_degrees' : True},

                'HDF.calibration': {'band2wavelength' : 'processed/radiance/calibration/spectral/band2Wavelength',
                                'darkframe' : 'processed/radiance/calibration/radiometric/darkFrame',
                                'radiometricframe' : 'processed/radiance/calibration/radiometric/radiometricFrame',
                                'fov' : 'processed/radiance/calibration/geometric/fieldOfView'},
                
                # Where to find the standard data for the cube. Note that is_calibrated implies whether data is already in correct format
                'HDF.hyperspectral': {'datacube' : 'processed/radiance/dataCube',
                                    'exposuretime' : 'processed/radiance/exposureTime',
                                    'timestamp' : 'processed/radiance/timestamp',
                                    'is_calibrated' : True},

                'HDF.rgb' :{'rgb_frames' : 'rawdata/rgb/rgbFrames',
                            'rgb_frames_timestamp' : 'rawdata/rgb/timestamp'}
                
}

# Customizes the config file
customize_config(config_path=config_file_mission, dict_custom=custom_config)

# Settings specific to the pre-processing of UHI data. At present they are hardcoded, but they could be integrated 
SettingsPreprocess = namedtuple('SettingsPreprocessing', ['dtype_datacube', 
                                                            'rotation_matrix_hsi_to_body',
                                                            'translation_body_to_hsi',
                                                            'rotation_matrix_alt_to_body',
                                                            'translation_alt_to_body',
                                                            'config_file_name',
                                                            'time_offset_sec',
                                                            'lon_lat_alt_origin',
                                                            'resolution_dem',
                                                            'agisoft_process'])

config_uhi_preprocess = SettingsPreprocess(dtype_datacube = np.float32,
                            # The fill value for empty cells (select values not occcuring in cube or ancillary data)
                            rotation_matrix_hsi_to_body = np.array([[0, 1, 0],
                                                                    [1, 0, 0],
                                                                    [0, 0, -1]]),
                            # Boolean being expressing whether to rectify only composite (true) or data cube and composite (false). True is fast.
                            translation_body_to_hsi = np.array([0, 0, 0]),
                            rotation_matrix_alt_to_body = np.array([[0, 1, 0],
                                                                    [1, 0, 0],
                                                                    [0, 0, -1]]),
                            # Boolean being expressing whether to rectify only composite (true) or data cube and composite (false). True is fast.
                            translation_alt_to_body = np.array([0.5, 0, 0]),
                            time_offset_sec =  22,
                            # Ben's tick s1 starts at 1593614097.992003 -> 22 s delay
                            # Ben's tick s2 starts at 1593614414.995001 -> 0 s delay

                            lon_lat_alt_origin =  np.array([1, 1, 0]),
                            # The beast sets up a fake coordinate system at 1 deg lon/lat.
                            config_file_name = 'configuration.ini',
                            resolution_dem = 0.2, # The resolution of the Altimeter-based DEM
                            agisoft_process  = False) # This is an option for photogrammetry-based processing in the case you have imagery





"""config = configparser.ConfigParser()
config.read(config_file)"""

def main():

    # The config stores all relevant configurations
    config = configparser.ConfigParser()
    config.read(config_file_mission)

    # The minimum for georeferencing is to parse 1) Mesh model and 2) The pose of the reference
    uhi_parsing_utils.uhi_beast(config=config, config_uhi=config_uhi_preprocess)
    
    config = parsing_utils.export_pose(config_file_mission)

    config = configparser.ConfigParser()

    config.read(config_file_mission)
    
    # Exports model
    parsing_utils.export_model(config_file_mission)

    # Visualize the data 3D photo model from RGB images and the time-resolved positions/orientations
    #visualize.show_mesh_camera(config)

    # Georeference the line scans of the hyperspectral imager. Utilizes parsed data
    georeference.main(config_file_mission, viz=False)

    orthorectification.main(config_file_mission)
    # Alternatively mode = 'calibrate'
    # georeference.main(config_file, mode='calibrate', is_calibrated=True)


if __name__ == "__main__":
    main()
source_gaia_info.csv includes
 - All columns of the sources from the main Gaia DR3 table.

In separate source folders:
 Data files:
   - <source_id>_obs_info_and_rv.csv
    	- date: observation date DD/MM/YYYY (UT)
    	- time: observation time HH:MM:SS (UT)
    	- jd: Julian day (days)
    	- epoch_id: integer identifiers of the spectra data
    	- file_name: name of the spectrum data file for the epoch_id
    	- rv: radial velocity in km/s
    	- rv_err: error on rv in km/s


   - <source_id>_<telescope>_<instrument>_<epoch_id>.csv:
      - epoch_id identifies the (spectral) observation of the <source_id> by a specific instrument.
      - wavelength: wavelength in Angstrom
      - flux: flux in arbitrary unit.

 
   - <source_id>_vpec_vs_gamma.npz: The compressed numpy data file containing the peculiar velocity (vpec) as a function of systemic radial velocity (gamma).
      - gamma: systemic radial velocity
      - vpec: median value of peculiar velocity at each gamma value
      - vpec_lo: the 16th percentile of the vpec at each gamma value
      - vpec_hi: the 84th percentile of the vpec at each gamma value


Demo figures:
 - <source_id>_<telescope>_<instrument>_<epoch_id>.pdf: a line plot of the spectrum in the corresponding .csv file, made by plot_spec.py.

 - <source_id>_rv_curve.pdf: this is a demo radial velocity vs. time plot, made by plot_rv_curve.py.

 - <source_id>_vpec_vs_gamma.pdf: A vpec vs. gamma line plot, made by plot_vpec_vs_gamma.py.
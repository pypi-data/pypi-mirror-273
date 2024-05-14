# solar-wind-archive
A Python package for accessing ACE solar wind data, both current and historical.

# Authors and Contributors
### **AUTHOR: Amelia R H Urquhart** 

# Installation
Installation through PyPI is recommended. Copy-paste the following line into your terminal:

`pip install solar_wind_archive`

After that, include the following line in your Python script, and you should be good to go.

`import solar_wind_archive.ace_rtsw as ace`
  
# How To Use
```python
import solar_wind_archive.ace_rtsw as ace

# Gets solar wind plasma density, speed, and temperature data from the past 24 hours
time, density, speed, temperature = ace.get_solar_wind_plasma()

# Gets interplanetary magnetic field data for the May 10, 2024 G5 geomagnetic storm
start_time = datetime(2024, 5, 10, 0, 0, tzinfo=timezone.utc)
end_time = datetime(2024, 5, 12, 0, 0, tzinfo=timezone.utc)

time, bx, by, bz, bt, lat, lon = ace.get_interplanetary_magnetic_field(start_time, end_time)

# Gets proton and electron flux for the Halloween solar storms of 2003
start_time = datetime(2003, 10, 26, 0, 0, tzinfo=timezone.utc)
end_time = datetime(2003, 11, 7, 0, 0, tzinfo=timezone.utc)

time, protons_over_10_mev, protons_over_30_mev = ace.get_high_energy_proton_flux(start_time, end_time)
time, elec_38_53, elec_175_314, pro_47_68, pro_115_195, pro_310_580, pro_761_1220, pro_1060_1900, aniso_ratio = ace.get_proton_electron_flux(start_time, end_time)
```
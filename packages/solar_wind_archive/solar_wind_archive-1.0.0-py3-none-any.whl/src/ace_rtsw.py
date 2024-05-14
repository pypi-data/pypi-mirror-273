from datetime import date, datetime, timedelta, timezone
import os
import pytz
from urllib.request import urlretrieve

def get_proton_electron_flux(start_time:datetime = None, end_time:datetime = None):
    """
    Retrieves the EPAM proton and electron flux for a given time range.

    Args:
        start_time:
            Start time of range
        end_time:
            End time of range

    Returns:
        A tuple of four lists.

        First list: Date/Time [UTC]
        Second list: Electron Flux 38-53 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Third list: Electron Flux 175-315 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Fourth list: Proton Flux 47-68 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Fifth list: Proton Flux 115-195 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Sixth list: Proton Flux 310-580 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Seventh list: Proton Flux 761-1220 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Eighth list: Proton Flux 1060-1900 keV [Units: particles cm^-2 sec^-1 sr^-1 MeV^-1]
        Ninth list: Anisotropy Index [Units: Dimensionless]
    """

    if start_time == None or end_time == None:
        start_time, end_time = _most_recent_24_hours()

    dates_in_range = _dates_in_range(start_time, end_time)

    files = []

    for date in dates_in_range:
        url = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/daily/{:04d}{:02d}{:02d}_ace_epam_5m.txt".format(date.year, date.month, date.day)
        filename = "ace_epam_{:04d}{:02d}{:02d}.txt".format(date.year, date.month, date.day)

        try:
            urlretrieve(url, filename)
        except Exception:
            continue

        files.append(filename)

    time = []
    elec_38_53 = []
    elec_175_315 = []
    pro_47_68 = []
    pro_115_195 = []
    pro_310_580 = []
    pro_761_1220 = []
    pro_1060_1900 = []
    aniso_ratio = []

    for file in files:
        with open(file) as f:
            lines = f.readlines()

            for line in lines:
                if "#" == line[0] or ":" == line[0]:
                    continue
                else:
                    tokens = line.split()

                    year = int(tokens[0])
                    month = int(tokens[1])
                    day = int(tokens[2])
                    hour_minute = tokens[3]

                    hour = int(hour_minute[0] + hour_minute[1])
                    minute = int(hour_minute[2] + hour_minute[3])

                    current_time = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

                    if current_time >= start_time and current_time <= end_time:
                        current_elec_38_53 = float(tokens[7])
                        current_elec_175_315 = float(tokens[8])
                        current_pro_47_68 = float(tokens[10])
                        current_pro_115_195 = float(tokens[11])
                        current_pro_310_580 = float(tokens[12])
                        current_pro_761_1220 = float(tokens[13])
                        current_pro_1060_1900 = float(tokens[14])
                        current_aniso_ratio = float(tokens[15])

                        if current_elec_38_53 == -100000.0:
                            current_elec_38_53 = float('nan')
                        if current_elec_175_315 == -100000.0:
                            current_elec_175_315 = float('nan')
                        if current_pro_47_68 == -100000.0:
                            current_pro_47_68 = float('nan')
                        if current_pro_115_195 == -100000.0:
                            current_pro_115_195 = float('nan')
                        if current_pro_310_580 == -100000.0:
                            current_pro_310_580 = float('nan')
                        if current_pro_761_1220 == -100000.0:
                            current_pro_761_1220 = float('nan')
                        if current_pro_1060_1900 == -100000.0:
                            current_pro_1060_1900 = float('nan')
                        if current_aniso_ratio == -1.0:
                            current_aniso_ratio = float('nan')

                        time.append(current_time)
                        elec_38_53.append(current_elec_38_53)
                        elec_175_315.append(current_elec_175_315)
                        pro_47_68.append(current_pro_47_68)
                        pro_115_195.append(current_pro_115_195)
                        pro_310_580.append(current_pro_310_580)
                        pro_761_1220.append(current_pro_761_1220)
                        pro_1060_1900.append(current_pro_1060_1900)
                        aniso_ratio.append(current_aniso_ratio)

    for file in files:
        os.remove(file)

    return time, elec_38_53, elec_175_315, pro_47_68, pro_115_195, pro_310_580, pro_761_1220, pro_1060_1900, aniso_ratio

def get_interplanetary_magnetic_field(start_time:datetime = None, end_time:datetime = None) -> tuple[list[datetime], list[float], list[float], list[float], list[float], list[float], list[float]]:
    """
    Retrieves the IMF magnitude and orientation for a given time range.

    Args:
        start_time:
            Start time of range
        end_time:
            End time of range

    Returns:
        A tuple of seven lists.

        First list: Date/Time [UTC]
        Second list: Bx (Earth-Sun Component) [Units: Nanoteslas]
        Third list: By (Sunset-Sunrise Component) [Units: Nanoteslas]
        Fourth list: Bz (North-South Component) [Units: Nanoteslas]
        Fifth list: Bt (Total Magnitude) [Units: Nanoteslas]
        Sixth list: Field Orientation Latitude [Units: Degrees]
        Seventh list: Field Orientation Latitude [Units: Degrees]
    """

    if start_time == None or end_time == None:
        start_time, end_time = _most_recent_24_hours()

    dates_in_range = _dates_in_range(start_time, end_time)

    files = []

    for date in dates_in_range:
        url = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/daily/{:04d}{:02d}{:02d}_ace_mag_1m.txt".format(date.year, date.month, date.day)
        filename = "ace_imf_{:04d}{:02d}{:02d}.txt".format(date.year, date.month, date.day)

        try:
            urlretrieve(url, filename)
        except Exception:
            continue

        files.append(filename)

    time = []
    bx = []
    by = []
    bz = []
    bt = []
    lat = []
    lon = []

    for file in files:
        with open(file) as f:
            lines = f.readlines()

            for line in lines:
                if "#" == line[0] or ":" == line[0]:
                    continue
                else:
                    tokens = line.split()

                    year = int(tokens[0])
                    month = int(tokens[1])
                    day = int(tokens[2])
                    hour_minute = tokens[3]

                    hour = int(hour_minute[0] + hour_minute[1])
                    minute = int(hour_minute[2] + hour_minute[3])

                    current_time = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

                    if current_time >= start_time and current_time <= end_time:
                        current_bx = float(tokens[7])
                        current_by = float(tokens[8])
                        current_bz = float(tokens[9])
                        current_bt = float(tokens[10])
                        current_lat = float(tokens[11])
                        current_lon = float(tokens[12])

                        if current_bx == -999.9:
                            current_bx = float('nan')
                        if current_by == -999.9:
                            current_by = float('nan')
                        if current_bz == -999.9:
                            current_bz = float('nan')
                        if current_bt == -999.9:
                            current_bt = float('nan')
                        if current_lat == -999.9:
                            current_lat = float('nan')
                        if current_lon == -999.9:
                            current_lon = float('nan')

                        time.append(current_time)
                        bx.append(current_bx)
                        by.append(current_by)
                        bz.append(current_bz)
                        bt.append(current_bt)
                        lat.append(current_lat)
                        lon.append(current_lon)

    for file in files:
        os.remove(file)

    return time, bx, by, bz, bt, lat, lon

def get_high_energy_proton_flux(start_time:datetime = None, end_time:datetime = None) -> tuple[list[datetime], list[float], list[float]]:
    """
    Retrieves the high energy proton flux for a given time range.

    Args:
        start_time:
            Start time of range
        end_time:
            End time of range

    Returns:
        A tuple of four lists.

        First list: Date/Time [UTC]
        Second list: Integral Proton Flux >10 MeV [Units: particles cm^-2 sec^-1 sr^-1]
        Third list: Integral Proton Flux >10 MeV [Units: particles cm^-2 sec^-1 sr^-1]
    """

    if start_time == None or end_time == None:
        start_time, end_time = _most_recent_24_hours()

    dates_in_range = _dates_in_range(start_time, end_time)

    files = []

    for date in dates_in_range:
        url = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/daily/{:04d}{:02d}{:02d}_ace_sis_5m.txt".format(date.year, date.month, date.day)
        filename = "ace_sis_{:04d}{:02d}{:02d}.txt".format(date.year, date.month, date.day)

        try:
            urlretrieve(url, filename)
        except Exception:
            continue

        files.append(filename)

    time = []
    protons_over_10_mev = []
    protons_over_30_mev = []

    for file in files:
        with open(file) as f:
            lines = f.readlines()

            for line in lines:
                if "#" == line[0] or ":" == line[0]:
                    continue
                else:
                    tokens = line.split()

                    year = int(tokens[0])
                    month = int(tokens[1])
                    day = int(tokens[2])
                    hour_minute = tokens[3]

                    hour = int(hour_minute[0] + hour_minute[1])
                    minute = int(hour_minute[2] + hour_minute[3])

                    current_time = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

                    if current_time >= start_time and current_time <= end_time:
                        current_pro_10 = float(tokens[7])
                        current_pro_30 = float(tokens[9])

                        if current_pro_10 == -100000.0:
                            current_pro_10 = float('nan')
                        if current_pro_30 == -100000.0:
                            current_pro_30 = float('nan')
  
                        time.append(current_time)
                        protons_over_10_mev.append(current_pro_10)
                        protons_over_30_mev.append(current_pro_30)

    for file in files:
        os.remove(file)

    return time, protons_over_10_mev, protons_over_30_mev

def get_solar_wind_plasma(start_time:datetime = None, end_time:datetime = None) -> tuple[list[datetime], list[float], list[float], list[float]]:
    """
    Retrieves the solar wind for a given time range.

    Args:
        start_time:
            Start time of range
        end_time:
            End time of range

    Returns:
        A tuple of four lists.

        First list: Date/Time [UTC]
        Second list: Proton Density [Units: particles cm^-3]
        Third list: Bulk Speed [Units: km/s]
        Fourth list: Ion Temperature [Units: Kelvins]
    """

    if start_time == None or end_time == None:
        start_time, end_time = _most_recent_24_hours()

    dates_in_range = _dates_in_range(start_time, end_time)

    files = []

    for date in dates_in_range:
        url = "https://sohoftp.nascom.nasa.gov/sdb/goes/ace/daily/{:04d}{:02d}{:02d}_ace_swepam_1m.txt".format(date.year, date.month, date.day)
        filename = "ace_solar_wind_{:04d}{:02d}{:02d}.txt".format(date.year, date.month, date.day)

        try:
            urlretrieve(url, filename)
        except Exception:
            continue

        files.append(filename)

    time = []
    density = []
    speed = []
    temperature = []

    for file in files:
        with open(file) as f:
            lines = f.readlines()

            for line in lines:
                if "#" == line[0] or ":" == line[0]:
                    continue
                else:
                    tokens = line.split()

                    year = int(tokens[0])
                    month = int(tokens[1])
                    day = int(tokens[2])
                    hour_minute = tokens[3]

                    hour = int(hour_minute[0] + hour_minute[1])
                    minute = int(hour_minute[2] + hour_minute[3])

                    current_time = datetime(year, month, day, hour, minute, tzinfo=timezone.utc)

                    if current_time >= start_time and current_time <= end_time:
                        current_density = float(tokens[7])
                        current_speed = float(tokens[8])
                        current_temperature = float(tokens[9])

                        if current_density == -9999.9:
                            current_density = float('nan')
                        if current_speed == -9999.9:
                            current_speed = float('nan')
                        if current_temperature == -100000.0:
                            current_temperature = float('nan')

                        time.append(current_time)
                        density.append(current_density)
                        speed.append(current_speed)
                        temperature.append(current_temperature)

    for file in files:
        os.remove(file)

    return time, density, speed, temperature
        
def _dates_in_range(start_time:datetime, end_time:datetime) -> list[date]:
    """
    Assembles a list of dates included in the datetime range

    Args:
        start_time:
            Start time of range
        end_time:
            End time of range

    Returns:
        A list of dates within the given range.
    """
    dates = []

    while start_time <= end_time:
        dates.append(start_time.date())
        start_time += timedelta(days=1)
        
    return dates

def _most_recent_24_hours() -> tuple[datetime, datetime]:
    """
    Retrieves two datetimes representing the past 24 hours

    Returns:
        A tuple of two datetimes.

        First item: datetime representing 24 hours ago
        Second item: datetime representing now
    """
    end_time = datetime.now().astimezone(pytz.UTC)
    start_time = end_time - timedelta(days=1)

    return start_time, end_time

## A few tests to make sure it's not crashing
if __name__ == "__main__":
    time, density, speed, temperature = get_solar_wind_plasma()
    time, bx, by, bz, bt, lat, lon = get_interplanetary_magnetic_field()
    time, protons_over_10_mev, protons_over_30_mev = get_high_energy_proton_flux()
    time, elec_38_53, elec_175_314, pro_47_68, pro_115_195, pro_310_580, pro_761_1220, pro_1060_1900, aniso_ratio = get_proton_electron_flux()

    start_time = datetime(2024, 5, 10, 0, 0, tzinfo=timezone.utc)
    end_time = datetime(2024, 5, 12, 0, 0, tzinfo=timezone.utc)

    time, bx, by, bz, bt, lat, lon = get_interplanetary_magnetic_field(start_time, end_time)
import psutil
from typing import Dict

"""
These helper functions are not intended to be called in any other place other than the provided class. 
The functions themselves arent even really necessary, but I thought it looked cleaner to do the data conversion
in some functions rather than inline in the class itself, and just decided to write functions for each
class variable.
"""


def get_cpu_count() -> int:
    return psutil.cpu_count(logical=False)


def get_cpu_usage() -> float:
    return psutil.cpu_percent(interval=1, percpu=False)


def get_cpu_frequency() -> Dict[str, float]:
    current = psutil.cpu_freq()[0]
    max_frequency = float(psutil.cpu_freq()[2])
    cpu_freq_dict = {
        "current_frequency": current / 1000,
        "max_frequency": max_frequency,
    }
    return cpu_freq_dict


def get_total_ram() -> float:
    mem = psutil.virtual_memory()
    return round((mem.total / 1073741824), 2)


def get_available_ram() -> float:
    mem = psutil.virtual_memory()
    return round((mem.available / 1073741824), 2)


def get_percentage_used_ram() -> float:
    mem = psutil.virtual_memory()
    return round(mem.percent, 2)


def get_total_disk_space() -> float:
    disk = psutil.disk_usage("/")
    return round((disk.total / 1073741824), 2)


def get_total_disk_free() -> float:
    disk = psutil.disk_usage("/")
    return round((disk.free / 1073741824), 2)


def get_total_disk_used() -> float:
    disk = psutil.disk_usage("/")
    return round((disk.total - disk.free) / 1073741824, 2)


def get_disk_percentage_used() -> float:
    disk = psutil.disk_usage("/")
    return disk.percent


def get_temperatures() -> dict:
    # Core temperature only available on linux machine
    """
    Get core temperature(s)
    :return: Dict of core temperatures if running on Linux. If other OS, returns and empty dictionary.
    """
    try:
        core_temp_list = psutil.sensors_temperatures(fahrenheit=True)["coretemp"]
        core_temp_dict = {}
        for core in core_temp_list:
            core_temp_dict[core.label] = core.current
        return core_temp_dict
    except KeyError:
        core_temp_dict = {}
        return core_temp_dict
    except AttributeError:
        core_temp_dict = {}
        return core_temp_dict


class Computer:
    """
    This class is used to easily evaluate the status of the computer. It returns a dictionary with the results
    of querying the status os the available computer components via psutils
    """

    @staticmethod
    def get_stats_dict() -> dict:
        stats_dict = {
            "cpu_count": get_cpu_count(),
            "cpu_usage": get_cpu_usage(),
            "cpu_frequency": get_cpu_frequency(),
            "core_temperatures": get_temperatures(),
            "ram_total": get_total_ram(),
            "ram_available": get_available_ram(),
            "ram_percentage": get_percentage_used_ram(),
            "disk_total": get_total_disk_space(),
            "disk_free": get_total_disk_free(),
            "disk_used": get_total_disk_used(),
            "disk_percentage": get_disk_percentage_used(),
        }
        return stats_dict

from utilities.stats import Computer, get_cpu_count, get_cpu_usage, get_cpu_frequency, get_total_ram, \
    get_available_ram, get_percentage_used_ram, get_total_disk_space, get_total_disk_free, get_total_disk_used, \
    get_disk_percentage_used, get_temperatures


def test_get_cpu_count():
    assert isinstance(get_cpu_count(), int)


def test_get_cpu_usage():
    assert isinstance(get_cpu_usage(), float)


def test_get_cpu_frequency():
    assert isinstance(get_cpu_frequency(), dict)
    for key in get_cpu_frequency().keys():
        assert isinstance(key, str)
    for value in get_cpu_frequency().values():
        assert isinstance(value, float)


def test_get_total_ram():
    assert isinstance(get_total_ram(), float)


def test_get_available_ram():
    assert isinstance(get_available_ram(), float)


def test_get_percentage_used_ram():
    assert isinstance(get_percentage_used_ram(), float)


def test_get_total_disk_space():
    assert isinstance(get_total_disk_space(), float)


def test_get_total_disk_free():
    assert isinstance(get_total_disk_free(), float)


def test_get_total_disk_used():
    assert isinstance(get_total_disk_used(), float)


def test_get_disk_percentage_used():
    assert isinstance(get_disk_percentage_used(), float)


def test_get_temperatures():
    assert isinstance(get_temperatures(), dict)


def test_computer_class():
    computer = Computer()
    assert isinstance(computer.get_stats_dict(), dict)

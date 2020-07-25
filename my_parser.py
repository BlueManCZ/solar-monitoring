import urllib3
import json

TIMEOUT = 1


def fetch_url(url):
    http = urllib3.PoolManager()
    try:
        resp = http.request('GET', url, timeout=TIMEOUT)
    except Exception as e:
        return False
    return resp.data.decode('utf-8')


def parse():
    site = fetch_url('10.0.0.28')

    if not site:
        return site

    voltages_tmp = site.split('U1= ')[1].split('V<br>')[0].replace('V U2= ', '+').split('+')
    u0 = float(voltages_tmp[0])
    u1 = float(voltages_tmp[1])
    panel_voltages = [round(u0-u1, 2), round(u0-u1, 2), round(u0-u1, 2), u1, u1]
    panel_currents = site.split('I= ')[1].split('A<br>Na')[0].replace('= ', '+').split('+')

    battery_voltages = site.split('Aku: U=')[1].split(', I=')[0].split('V')[:1]
    battery_currents = site.split(', I=')[1].split('A, ')[:1]
    battery_capacities = site.split(', I=')[1].split('A, ')[1].split('Ah')[:1]

    supply_voltages = site.split('Zdroj: U=')[1].split(', I=')[0].split('V')[:1]
    supply_currents = site.split(', I=')[2].split('A<br>')[:1]

    today_energy_global = float(site.split('Dnešní dodávka = <b>')[1].split('Wh')[0])
    today_energy_network = float(site.split('Do L ')[1].split('Wh')[0])
    today_power_max = float(site.split('dnes <b>')[1].split('W')[0])
    overall_power_max = float(site.split('Max výkon <b>')[1].split('W')[0])
    phase_converter_percentages = int(site.split('[')[1].split('%')[0])
    phase_power_supply = int(site.split('] ')[1].split(' <br>')[0].split(' ')[3])
    temperature = int(site.split('Do L')[1].split('°C')[0].split(' ')[2])

    data = {}

    panels = {'U': panel_voltages, 'I': panel_currents}
    data['panels'] = panels

    batteries = {'U': battery_voltages, 'I': battery_currents, 'C': battery_capacities}
    data['batteries'] = batteries

    supplies = {'U': supply_voltages, 'I': supply_currents}
    data['power_supplies'] = supplies

    system = {
        'TEG': today_energy_global,
        'TEN': today_energy_network,
        'TPM': today_power_max,
        'OPM': overall_power_max,
        'PCP': phase_converter_percentages,
        'PPS': phase_power_supply,
        'T': temperature
    }
    data['system'] = system

    json_data = json.dumps(data, indent=4)

    print(json_data)

    return data

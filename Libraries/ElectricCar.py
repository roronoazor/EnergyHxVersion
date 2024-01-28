from pprint import pprint
from .get_site_data import get_site_data_electric_car


class ElectricCar:

    def __init__(self, site_data, cost_data=None):
        super(ElectricCar, self).__init__()
        self.site_data = site_data
        self.site_name = next(iter(self.site_data))
        self.cost_data = cost_data
        #self.t_data = t_data
        #try:
        #    with open(os.path.abspath('../JSON files/wt_tip_speed_pow_coff.json')) as f:
        #        self.tip_speed_pow_coff = json.load(f)
        #except FileNotFoundError:
        #    with open(os.path.abspath('./JSON files/wt_tip_speed_pow_coff.json')) as f:
        #        self.tip_speed_pow_coff = json.load(f)

    def analyse(self):

        # perform analysis of data

        site_data = self.site_data.get(self.site_name)
        output_a = site_data.get("solar_power", 0) + site_data.get("wind_power", 0) + site_data.get("biomass_power", 0)
        output_b = (site_data.get('charger_slow_rating', 0)*site_data.get('slow_charger_numbers', 0)) + (site_data.get('charger_medium_rating', 0)*site_data.get("medium_charger_numbers", 0)) +(site_data.get('charger_fast_rating', 0)*site_data.get('fast_charger_numbers', 0))
        output_c = 0
        output_d = 0
        deficient_power = 0
        max_bess_capacity = site_data.get("max_bess_capacity", 0)

        if output_a <= output_b:
            deficient_power = abs(output_a-output_b)
            output_c = 0
            output_d = 0
        else:
            output_c = max_bess_capacity if (output_a - output_b) >= max_bess_capacity else (output_a - output_b)
            output_d = output_a - (output_b+max_bess_capacity)  if output_c > max_bess_capacity else 0

        result = dict()
        # round all values to 2 d.p
        result["output_a"] = round(output_a, 2)
        result["output_b"] = round(output_b, 2)
        result["output_c"] = round(output_c, 2)
        result["output_d"] = round(output_d, 2)
        result["deficient_power"] = round(deficient_power, 2)

        ################ compute cost data ##########################
        print("inside electric car -> ", self.cost_data)
        condenser_cost = float(self.cost_data.get("condenser_cost", 0))
        cooling_tower = float(self.cost_data.get("cooling_tower", 0))
        pump_cost = float(self.cost_data.get("pump_cost", 0))
        stack_cost = float(self.cost_data.get("stack_cost", 0))
        wind_turbine_cost = float(self.cost_data.get("wind_turbine_cost", 0))
        num_wind_turbine_cost = float(self.cost_data.get("num_wind_turbine_cost", 0))
        charging_rate_cost = float(self.cost_data.get("charging_rate_cost", 0))
        cost_time_s_charger = float(self.cost_data.get("cost_time_s_charger", 0))
        cost_time_m_charger = float(self.cost_data.get("cost_time_m_charger", 0))
        cost_time_f_charger = float(self.cost_data.get("cost_time_f_charger", 0))
        cost_tariff_rate = float(self.cost_data.get("cost_tariff_rate", 0))
        cost_time_2_grid = float(self.cost_data.get("cost_time_2_grid", 0))
        maintenance_cost = float(self.cost_data.get("maintenance_cost", 0))
        save_cost = self.cost_data.get("save_cost", False)
        cost_location = self.cost_data.get("cost_location")
        cost_of_land = float(self.cost_data.get("cost_of_land", 0))
        charger_name = self.cost_data.get("charger_name")
        cost_s_charger = float(self.cost_data.get("cost_s_charger", 0))
        cost_m_charger = float(self.cost_data.get("cost_m_charger", 0))
        cost_f_charger = float(self.cost_data.get("cost_f_charger", 0))
        cost_battery = float(self.cost_data.get("cost_battery", 0))
        cost_num_battery = float(self.cost_data.get("cost_num_battery", 0))
        solar_panel_name = self.cost_data.get("solar_panel_name")
        solar_panel_cost = float(self.cost_data.get("solar_panel_cost", 0))
        solar_panel_number = float(self.cost_data.get("solar_panel_number", 0))
        cost_of_generator = float(self.cost_data.get("generator_cost", 0))
        cost_of_steam_turbine = float(self.cost_data.get("steam_turbine_cost", 0))
        cost_of_combustor = float(self.cost_data.get("cost_combustor", 0))
        cost_of_boiler = float(self.cost_data.get("boiler_cost", 0))


        cost_of_all_chargers = ((cost_s_charger * site_data.get('slow_charger_numbers', 0))
                                + (cost_m_charger * site_data.get("medium_charger_numbers", 0))
                                + (cost_f_charger * site_data.get('fast_charger_numbers',0)))

        cost_of_all_batteries = (cost_battery * cost_num_battery)
        cost_of_solar_panels = (solar_panel_cost * solar_panel_number)
        cost_of_turbines = (wind_turbine_cost * num_wind_turbine_cost)
        m_cost = (stack_cost + pump_cost + cooling_tower + condenser_cost + cost_of_boiler + cost_of_generator + cost_of_steam_turbine + cost_of_combustor )

        E = cost_of_land + cost_of_all_chargers + cost_of_solar_panels + cost_of_turbines + cost_of_all_batteries + m_cost

        F = E + maintenance_cost

        G = charging_rate_cost + ((site_data.get('charger_slow_rating', 0) * site_data.get('slow_charger_numbers', 0) * cost_time_s_charger)
                                   + (site_data.get('charger_medium_rating', 0) * site_data.get("medium_charger_numbers", 0) * cost_time_m_charger)
                                  + (site_data.get('charger_fast_rating', 0) * site_data.get('fast_charger_numbers', 0)) *cost_time_f_charger)

        H = cost_tariff_rate * result.get("output_d", 0) * cost_time_2_grid

        I = G + H

        J = I - F


        cost_data = dict()
        cost_data["output_e"] = E
        cost_data["output_f"] = F
        cost_data["output_g"] = G
        cost_data["output_h"] = H
        cost_data["output_i"] = I
        cost_data["output_j"] = J

        result["cost_data"] = cost_data
        return result

# def wind_turbine_data(t_name, r_power, ci_wind_speed, co_wind_speed, r_diameter, h_height, units, b_length, no_blades):
#     t_data = dict()
#     t_data[t_name] = {}
#
#     t_data[t_name]['rated_power'] = r_power
#     t_data[t_name]['cut_in_wind_speed'] = ci_wind_speed
#     t_data[t_name]['cut_out_wind_speed'] = co_wind_speed
#     t_data[t_name]['rotor_diameter'] = r_diameter
#     t_data[t_name]['hub_height'] = h_height
#     t_data[t_name]['units'] = units
#     t_data[t_name]['blade_length'] = b_length
#     t_data[t_name]['no_blades'] = no_blades
#     return t_data



if __name__ == '__main__':
    site_data = get_site_data_electric_car('unilag', 1.2205, 27, 39, 4, 3.2, 4.3, 5.0, 10, 6.35, 11)
    electric_car = ElectricCar(site_data=site_data['unilag'], cost_data={})
    data = electric_car.analyse()
    pprint(data)

# defines the get site data methods for the various energy sources


def get_site_data_wind(site_name, a_density, temp, altitude, pressure, w_shape_param, velocity, w_scale_param, height, lat, long):
    site_data = dict()
    site_data[site_name] = {}

    site_data[site_name]['air_data'] = {}
    site_data[site_name]['air_data']['air_density'] = a_density
    site_data[site_name]['air_data']['temp'] = temp     # oC
    site_data[site_name]['air_data']['altitude'] = altitude    # m
    site_data[site_name]['air_data']['pressure'] = pressure    #

    site_data[site_name]['wind_dist_data'] = {}
    site_data[site_name]['wind_dist_data']['w_shape_param'] = w_shape_param
    site_data[site_name]['wind_dist_data']['velocity'] = velocity
    site_data[site_name]['wind_dist_data']['w_scale_param'] = w_scale_param
    site_data[site_name]['wind_dist_data']['height'] = height

    site_data[site_name]['location'] = {}
    site_data[site_name]['location']['lat'] = lat
    site_data[site_name]['location']['long'] = long
    return site_data


def get_site_data_solar(loc, lat, long, elv, site, no_wings, area, pitch, install_type):
    data_dict = dict()
    data_dict[loc] = {}
    data_dict[loc]['latitude'] = lat
    data_dict[loc]['longitude'] = long
    data_dict[loc]['elevation'] = elv
    data_dict[loc]['site'] = site
    data_dict[loc]['no_wings'] = no_wings
    data_dict[loc]['area'] = area
    data_dict[loc]['pitch'] = pitch
    data_dict[loc]['installation_type'] = install_type
    return data_dict


def get_site_data_electric_car(site_name, solar_power, biomass_power, wind_power, slow_charger_rating, medium_charger_rating, fast_charger_rating, number_of_slow_charger, number_of_medium_charger, number_of_fast_charger, max_biomass_capacity):
    site_data = dict()
    site_data[site_name] = {}

    site_data[site_name]['solar_power'] = solar_power  # solar power
    site_data[site_name]['biomass_power'] = biomass_power  # biomass power
    site_data[site_name]['wind_power'] = wind_power  # wind power
    site_data[site_name]['charger_slow_rating'] = slow_charger_rating  # charger slow rating
    site_data[site_name]['charger_medium_rating'] = medium_charger_rating  # charger medium rating
    site_data[site_name]['charger_fast_rating'] = fast_charger_rating  # charger fast rating
    site_data[site_name]['slow_charger_number'] = number_of_slow_charger
    site_data[site_name]['medium_charger_number'] = number_of_medium_charger
    site_data[site_name]['fast_charger_number'] = number_of_fast_charger
    site_data[site_name]['max_bess_capacity'] = max_biomass_capacity

    return site_data


def get_site_data_applicance_audit(app_name, p_rating, units, op_hours):
    app = dict()
    app[app_name] = {'power_rating': p_rating, 'units': units, 'operating_hours': op_hours}
    return app


def get_site_data_battery_design(m_v, a_v, alpha_s, c_rr, c_d, rho, A, v_v):
    data_dict = dict()
    # create a dictionary to hold the values needed for analyze function
    data_dict['m_v'] = m_v
    data_dict['a_v'] = a_v
    data_dict['alpha_s'] = alpha_s
    data_dict['c_rr'] = c_rr
    data_dict['c_d'] = c_d
    data_dict['rho'] = rho
    data_dict['A'] = A
    data_dict['v_v'] = v_v
    return data_dict


def get_site_data_cooling_load(name, room_area, weather_in_dry, weather_in_hum, weather_out_dry, weather_out_hum, level_activity,
                      type_space, heat_gained):
    data_dict = dict()
    data_dict[name] = {}
    data_dict[name]['room_area'] = room_area
    data_dict[name]['weather'] = {}
    data_dict[name]['weather']['indoor'] = {'dry_bulb': weather_in_dry, 'humidity': weather_in_hum}
    data_dict[name]['weather']['outdoor'] = {'dry_bulb': weather_out_dry, 'humidity': weather_out_hum}
    data_dict[name]['level_activity'] = level_activity
    data_dict[name]['type_space'] = type_space
    data_dict[name]['heat_gained'] = heat_gained
    return data_dict
from pprint import pprint
from .get_site_data import get_site_data_applicance_audit



class ApplianceAudit:
    et = 33.05

    def __init__(self, app_details):
        self.app_details = app_details

    def analyse(self, retrofit_app):
        analysed_dict = dict()
        for appliance in self.app_details:
            try:
                ec = (self.app_details[appliance]['units'] * self.app_details[appliance]['operating_hours'] *
                      self.app_details[appliance]['power_rating'] / 1000)
                retrofit_ec = retrofit_app[appliance]['units'] * retrofit_app[appliance]['operating_hours'] * \
                              retrofit_app[appliance]['power_rating'] / 1000
                es = ec - retrofit_ec
                bs = es * ApplianceAudit.et
                pay_back = retrofit_ec / es * 365
                r = es / ec
                pwf = 1 / ((1 + r) ** pay_back)
                lcc = retrofit_ec + (pwf * es * 365)
                analysed_dict[appliance] = {'EC': ec, 'EC retrofit': retrofit_ec, 'ES': es, 'BS': bs,
                                            'Pay Back': pay_back,
                                            'ROR': r, 'PWF': pwf, 'LCC': lcc}
            except Exception as e:
                print(type(e), str(e))

        return analysed_dict


if __name__ == '__main__':
    app_names = ['IPad', 'Heater', 'Fan']

    all_new_app = dict()
    new_app1 = get_site_data_applicance_audit('IPad', 2, 2, 5)
    all_new_app = {**all_new_app, **new_app1}
    new_app2 = get_site_data_applicance_audit('Heater', 3, 2, 1)
    all_new_app = {**all_new_app, **new_app2}
    new_app3 = get_site_data_applicance_audit('Fan', 7, 2, 12)
    all_new_app = {**all_new_app, **new_app3}
    a_audit = ApplianceAudit(all_new_app)

    all_new_app = {}
    new_app1 = get_site_data_applicance_audit('IPad', 1, 2, 5)
    all_new_app = {**all_new_app, **new_app1}
    new_app2 = get_site_data_applicance_audit('Heater', 2, 2, 1)
    all_new_app = {**all_new_app, **new_app2}
    new_app3 = get_site_data_applicance_audit('Fan', 5, 2, 12)
    all_new_app = {**all_new_app, **new_app3}

    result = a_audit.analyse(all_new_app)
    pprint(result)

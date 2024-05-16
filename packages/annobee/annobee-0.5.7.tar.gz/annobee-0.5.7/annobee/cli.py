import argparse
import requests
import json

class Annobee:
    def __init__(self, endpoint='http://localhost:5000/api/interpret'):
        self.endpoint = endpoint

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint

    def get_criteria(self, variant, genome_build='hg38'):
        response = requests.post(self.endpoint, json={
            'variant': variant,
            'genome_build': genome_build,
            'adjustments': {}
        })
        response_data = response.json()
        return response_data.get('INFO', {})

    def get_ps1(self, info):
        return info.get('PS')[0]

    def get_pm5(self, info):
        return info.get('PM')[4]

    def get_bp7(self, info):
        return info.get('BP')[6]

    def get_pvs1(self, info):
        return info.get('PVS1')

    def get_bp1(self, info):
        return info.get('BP')[0]

    def get_pp2(self, info):
        return info.get('PP')[1]

    def get_ps4(self, info):
        return info.get('PS')[3]

    def get_bs1(self, info):
        return info.get('BS')[0]

    def get_bs2(self, info):
        return info.get('BS')[1]

    def get_pm2(self, info):
        return info.get('PM')[1]

    def get_pm1(self, info):
        return info.get('PM')[0]

    def get_pp5(self, info):
        return info.get('PP')[4]

    def get_bp6(self, info):
        return info.get('BP')[5]

    def get_ba1(self, info):
        return info.get('BA1')

    def get_pp3(self, info):
        return info.get('PP')[2]

    def get_bp4(self, info):
        return info.get('BP')[3]

    def get_pm4(self, info):
        return info.get('PM')[3]

    def get_bp3(self, info):
        return info.get('BP')[2]

    def get_va_pathogenicity(self, info):
        return info.get('VA_PATHOGENICITY')

    def get_all(self, info):
        return {
            'PS1': self.get_ps1(info),
            'PM5': self.get_pm5(info),
            'BP7': self.get_bp7(info),
            'PVS1': self.get_pvs1(info),
            'BP1': self.get_bp1(info),
            'PP2': self.get_pp2(info),
            'PS4': self.get_ps4(info),
            'BS1': self.get_bs1(info),
            'BS2': self.get_bs2(info),
            'PM2': self.get_pm2(info),
            'PM1': self.get_pm1(info),
            'PP5': self.get_pp5(info),
            'BP6': self.get_bp6(info),
            'BA1': self.get_ba1(info),
            'PP3': self.get_pp3(info),
            'BP4': self.get_bp4(info),
            'PM4': self.get_pm4(info),
            'BP3': self.get_bp3(info),
            'VA_PATHOGENICITY': self.get_va_pathogenicity(info)
        }

def main():
    parser = argparse.ArgumentParser(description='Annovar SDK CLI')
    parser.add_argument('variant', type=str, help='Variant in the format chr-pos-ref-alt Example: 1-12345-A-G')
    parser.add_argument('-endpoint', type=str, default='http://localhost:5000/api/interpret', help='API endpoint to use')
    parser.add_argument('-ps1', action='store_true', help='Evaluate PS1 criteria')
    parser.add_argument('-pm5', action='store_true', help='Evaluate PM5 criteria')
    parser.add_argument('-bp7', action='store_true', help='Evaluate BP7 criteria')
    parser.add_argument('-pvs1', action='store_true', help='Evaluate PVS1 criteria')
    parser.add_argument('-bp1', action='store_true', help='Evaluate BP1 criteria')
    parser.add_argument('-pp2', action='store_true', help='Evaluate PP2 criteria')
    parser.add_argument('-ps4', action='store_true', help='Evaluate PS4 criteria')
    parser.add_argument('-bs1', action='store_true', help='Evaluate BS1 criteria')
    parser.add_argument('-bs2', action='store_true', help='Evaluate BS2 criteria')
    parser.add_argument('-pm2', action='store_true', help='Evaluate PM2 criteria')
    parser.add_argument('-pm1', action='store_true', help='Evaluate PM1 criteria')
    parser.add_argument('-pp5', action='store_true', help='Evaluate PP5 criteria')
    parser.add_argument('-bp6', action='store_true', help='Evaluate BP6 criteria')
    parser.add_argument('-ba1', action='store_true', help='Evaluate BA1 criteria')
    parser.add_argument('-pp3', action='store_true', help='Evaluate PP3 criteria')
    parser.add_argument('-bp4', action='store_true', help='Evaluate BP4 criteria')
    parser.add_argument('-pm4', action='store_true', help='Evaluate PM4 criteria')
    parser.add_argument('-bp3', action='store_true', help='Evaluate BP3 criteria')
    parser.add_argument('-all', action='store_true', help='Evaluate all criteria')

    args = parser.parse_args()

    annobee = Annobee(endpoint=args.endpoint)
    variant_info = annobee.get_criteria(args.variant)

    results = {}
    if args.all:
        results = annobee.get_all(variant_info)
    else:
        if args.ps1:
            results['PS1'] = annobee.get_ps1(variant_info)
        if args.pm5:
            results['PM5'] = annobee.get_pm5(variant_info)
        if args.bp7:
            results['BP7'] = annobee.get_bp7(variant_info)
        if args.pvs1:
            results['PVS1'] = annobee.get_pvs1(variant_info)
        if args.bp1:
            results['BP1'] = annobee.get_bp1(variant_info)
        if args.pp2:
            results['PP2'] = annobee.get_pp2(variant_info)
        if args.ps4:
            results['PS4'] = annobee.get_ps4(variant_info)
        if args.bs1:
            results['BS1'] = annobee.get_bs1(variant_info)
        if args.bs2:
            results['BS2'] = annobee.get_bs2(variant_info)
        if args.pm2:
            results['PM2'] = annobee.get_pm2(variant_info)
        if args.pm1:
            results['PM1'] = annobee.get_pm1(variant_info)
        if args.pp5:
            results['PP5'] = annobee.get_pp5(variant_info)
        if args.bp6:
            results['BP6'] = annobee.get_bp6(variant_info)
        if args.ba1:
            results['BA1'] = annobee.get_ba1(variant_info)
        if args.pp3:
            results['PP3'] = annobee.get_pp3(variant_info)
        if args.bp4:
            results['BP4'] = annobee.get_bp4(variant_info)
        if args.pm4:
            results['PM4'] = annobee.get_pm4(variant_info)
        if args.bp3:
            results['BP3'] = annobee.get_bp3(variant_info)
    
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

import argparse
import requests
import json

API_URL = 'http://localhost:5000/api/interpret'

def get_criteria(variant, genome_build='hg38'):
    response = requests.post(API_URL, json={
        'variant': variant,
        'genome_build': genome_build,
        'adjustments': {}
    })
    response_data = response.json()
    return response_data.get('INFO', {})

def get_ps1(info):
    return info.get('PS')[0]

def get_pm5(info):
    return info.get('PM')[4]

def get_bp7(info):
    return info.get('BP')[6]

def get_pvs1(info):
    return info.get('PVS1')

def get_bp1(info):
    return info.get('BP')[0]

def get_pp2(info):
    return info.get('PP')[1]

def get_ps4(info):
    return info.get('PS')[3]

def get_bs1(info):
    return info.get('BS')[0]

def get_bs2(info):
    return info.get('BS')[1]

def get_pm2(info):
    return info.get('PM')[1]

def get_pm1(info):
    return info.get('PM')[0]

def get_pp5(info):
    return info.get('PP')[4]

def get_bp6(info):
    return info.get('BP')[5]

def get_ba1(info):
    return info.get('BA1')

def get_pp3(info):
    return info.get('PP')[2]

def get_bp4(info):
    return info.get('BP')[3]

def get_pm4(info):
    return info.get('PM')[3]

def get_bp3(info):
    return info.get('BP')[2]

def get_va_pathogenicity(info):
    return info.get('VA_PATHOGENICITY')

def get_all(info):
    return {
        'PS1': get_ps1(info),
        'PM5': get_pm5(info),
        'BP7': get_bp7(info),
        'PVS1': get_pvs1(info),
        'BP1': get_bp1(info),
        'PP2': get_pp2(info),
        'PS4': get_ps4(info),
        'BS1': get_bs1(info),
        'BS2': get_bs2(info),
        'PM2': get_pm2(info),
        'PM1': get_pm1(info),
        'PP5': get_pp5(info),
        'BP6': get_bp6(info),
        'BA1': get_ba1(info),
        'PP3': get_pp3(info),
        'BP4': get_bp4(info),
        'PM4': get_pm4(info),
        'BP3': get_bp3(info),
        'VA_PATHOGENICITY': get_va_pathogenicity(info)
    }

def main():
    parser = argparse.ArgumentParser(description='Annovar SDK CLI')
    parser.add_argument('variant', type=str, help='Variant in the format chr-pos-ref-alt Example: 1-12345-A-G')
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

    variant_info = get_criteria(args.variant)

    results = {}
    if args.all:
        results = get_all(variant_info)
    else:
        if args.ps1:
            results['PS1'] = get_ps1(variant_info)
        if args.pm5:
            results['PM5'] = get_pm5(variant_info)
        if args.bp7:
            results['BP7'] = get_bp7(variant_info)
        if args.pvs1:
            results['PVS1'] = get_pvs1(variant_info)
        if args.bp1:
            results['BP1'] = get_bp1(variant_info)
        if args.pp2:
            results['PP2'] = get_pp2(variant_info)
        if args.ps4:
            results['PS4'] = get_ps4(variant_info)
        if args.bs1:
            results['BS1'] = get_bs1(variant_info)
        if args.bs2:
            results['BS2'] = get_bs2(variant_info)
        if args.pm2:
            results['PM2'] = get_pm2(variant_info)
        if args.pm1:
            results['PM1'] = get_pm1(variant_info)
        if args.pp5:
            results['PP5'] = get_pp5(variant_info)
        if args.bp6:
            results['BP6'] = get_bp6(variant_info)
        if args.ba1:
            results['BA1'] = get_ba1(variant_info)
        if args.pp3:
            results['PP3'] = get_pp3(variant_info)
        if args.bp4:
            results['BP4'] = get_bp4(variant_info)
        if args.pm4:
            results['PM4'] = get_pm4(variant_info)
        if args.bp3:
            results['BP3'] = get_bp3(variant_info)
    
    print(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()

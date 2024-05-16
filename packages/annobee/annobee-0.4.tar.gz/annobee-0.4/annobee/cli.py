import argparse
import requests
import json
from annobee.variant import Variant
from annobee.criterias import Criteria

API_URL = 'http://localhost:5000/api/interpret'

def get_criteria(variant, criteria_name):
    response = requests.post(API_URL, json={
        'variant': variant,
        'genome_build': 'hg38',
        'adjustments': {}
    })
    return response.json().get(criteria_name)

def get_ps1(variant):
    return get_criteria(variant, 'PS1')

def get_pm5(variant):
    return get_criteria(variant, 'PM5')

def get_bp7(variant):
    return get_criteria(variant, 'BP7')

def get_pvs1(variant):
    return get_criteria(variant, 'PVS1')

def get_bp1(variant):
    return get_criteria(variant, 'BP1')

def get_pp2(variant):
    return get_criteria(variant, 'PP2')

def get_ps4(variant):
    return get_criteria(variant, 'PS4')

def get_bs1(variant):
    return get_criteria(variant, 'BS1')

def get_bs2(variant):
    return get_criteria(variant, 'BS2')

def get_pm2(variant):
    return get_criteria(variant, 'PM2')

def get_pm1(variant):
    return get_criteria(variant, 'PM1')

def get_pp5(variant):
    return get_criteria(variant, 'PP5')

def get_bp6(variant):
    return get_criteria(variant, 'BP6')

def get_ba1(variant):
    return get_criteria(variant, 'BA1')

def get_pp3(variant):
    return get_criteria(variant, 'PP3')

def get_bp4(variant):
    return get_criteria(variant, 'BP4')

def get_pm4(variant):
    return get_criteria(variant, 'PM4')

def get_bp3(variant):
    return get_criteria(variant, 'BP3')

def main():
    parser = argparse.ArgumentParser(description='Annovar SDK CLI')
    parser.add_argument('variant', type=str, help='Variant in the format chr-pos-ref-alt')
    # Define the criteria options
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

    chrom, pos, ref, alt = args.variant.split('-')
    pos = int(pos)  # Ensure the position is an integer
    criteria = Criteria()

    results = {}
    if args.all or args.ps1:
        results['PS1'] = get_ps1(args.variant)
    if args.all or args.pm5:
        results['PM5'] = get_pm5(args.variant)
    if args.all or args.bp7:
        results['BP7'] = get_bp7(args.variant)
    if args.all or args.pvs1:
        results['PVS1'] = get_pvs1(args.variant)
    if args.all or args.bp1:
        results['BP1'] = get_bp1(args.variant)
    if args.all or args.pp2:
        results['PP2'] = get_pp2(args.variant)
    if args.all or args.ps4:
        results['PS4'] = get_ps4(args.variant)
    if args.all or args.bs1:
        results['BS1'] = get_bs1(args.variant)
    if args.all or args.bs2:
        results['BS2'] = get_bs2(args.variant)
    if args.all or args.pm2:
        results['PM2'] = get_pm2(args.variant)
    if args.all or args.pm1:
        results['PM1'] = get_pm1(args.variant)
    if args.all or args.pp5:
        results['PP5'] = get_pp5(args.variant)
    if args.all or args.bp6:
        results['BP6'] = get_bp6(args.variant)
    if args.all or args.ba1:
        results['BA1'] = get_ba1(args.variant)
    if args.all or args.pp3:
        results['PP3'] = get_pp3(args.variant)
    if args.all or args.bp4:
        results['BP4'] = get_bp4(args.variant)
    if args.all or args.pm4:
        results['PM4'] = get_pm4(args.variant)
    if args.all or args.bp3:
        results['BP3'] = get_bp3(args.variant)
    if args.all:
        # Assuming `criteria.interpret` processes all criteria and returns a dictionary
        results.update(criteria.interpret(chrom, pos, ref, alt))
    
    print(results)

if __name__ == '__main__':
    main()

# annobee_sdk/main.py

import argparse
from variant import Variant
from criterias import Criteria


def main():
    parser = argparse.ArgumentParser(description='Annovar SDK CLI')
    parser.add_argument('variant', type=str, help='Variant in the format chr-pos-ref-alt')
    
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
        results['PS1'] = criteria.set_PS1(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pm5:
        results['PM5'] = criteria.set_PM5(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bp7:
        results['BP7'] = criteria.set_BP7(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pvs1:
        results['PVS1'] = criteria.set_PVS1(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bp1:
        results['BP1'] = criteria.set_BP1(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pp2:
        results['PP2'] = criteria.set_PP2(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.ps4:
        results['PS4'] = criteria.set_PS4(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bs1:
        results['BS1'] = criteria.set_BS1(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bs2:
        results['BS2'] = criteria.set_BS2(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pm2:
        results['PM2'] = criteria.set_PM2(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pm1:
        results['PM1'] = criteria.set_PM1(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pp5:
        results['PP5'] = criteria.set_PP5(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bp6:
        results['BP6'] = criteria.set_BP6(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.ba1:
        results['BA1'] = criteria.set_BA1(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pp3:
        results['PP3'] = criteria.set_PP3(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bp4:
        results['BP4'] = criteria.set_BP4(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.pm4:
        results['PM4'] = criteria.set_PM4(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))
    if args.all or args.bp3:
        results['BP3'] = criteria.set_BP3(Variant(chr=chrom, pos=pos, ref=ref, alt=alt))

    if args.all:
        results.update(criteria.interpret(chrom, pos, ref, alt))
    
    print(results)

if __name__ == '__main__':
    main()

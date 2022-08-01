import csv
from datetime import datetime, timezone, timedelta


# -- MeteringPoints ----------------------------------------------------------

production_gsrn = []
consumption_gsrn = []
meteringpoints = []

with open('dummy_solar_production.csv', newline='') as f1:
    for gsrn in set(row['id'] for row in csv.DictReader(f1)):
        meteringpoints.append({
            'gsrn': f'X-test-{gsrn}',
            'sector': 'DK1',
            'type': 'production',
            'postcode': '8000',
            'technology_code': 'T010000',
            'fuel_code': 'F01040100',
        })

with open('dummy_consumption.csv', newline='') as f2:
    for gsrn in set(row['id'] for row in csv.DictReader(f2)):
        meteringpoints.append({
            'gsrn': f'X-test-{gsrn}',
            'sector': 'DK1',
            'type': 'consumption',
            'postcode': '8000',
        })

with open('meteringpoints.csv', 'w', newline='') as f3:
    writer = csv.DictWriter(f3, fieldnames=(
        'gsrn',
        'type',
        'sector',
        'technology_code',
        'fuel_code',
        'street_code',
        'street_name',
        'building_number',
        'city_name',
        'postcode',
        'municipality_code'
    ))

    writer.writeheader()

    for meteringpoint in sorted(meteringpoints, key=lambda m: m['gsrn']):
        writer.writerow(meteringpoint)


# -- Measurements ------------------------------------------------------------


with open('measurements.csv', 'w', newline='') as f3:
    writer = csv.DictWriter(f3, fieldnames=(
        'gsrn',
        'begin',
        'end',
        'amount'
    ))

    writer.writeheader()

    with open('dummy_solar_production.csv', newline='') as f4:
        for row in csv.DictReader(f4):
            begin = datetime \
                .fromisoformat(row['time']) \
                .replace(tzinfo=timezone.utc)

            end = begin + timedelta(hours=1)

            writer.writerow({
                'gsrn': f'X-test-{row["id"]}',
                'begin': str(begin),
                'end': str(end),
                'amount': int(float(row['production']) * 1000),
            })

    with open('dummy_consumption.csv', newline='') as f4:
        for row in csv.DictReader(f4):
            begin = datetime \
                .fromisoformat(row['time']) \
                .replace(tzinfo=timezone.utc)

            end = begin + timedelta(hours=1)

            writer.writerow({
                'gsrn': f'X-test-{row["id"]}',
                'begin': str(begin),
                'end': str(end),
                'amount': int(float(row['consumption']) * 1000),
            })

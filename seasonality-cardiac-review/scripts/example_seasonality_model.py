#!/usr/bin/env python3
"""Example phenotype-level seasonality test for cardiac MRI data.

Expected columns in input CSV:
- phenotype
- scan_date (YYYY-MM-DD)
- age
- sex
- bsa
- acquisition_year
- scanner_id
- value

Optional:
- subject_id
- site_id
"""

import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def main(path: str):
    df = pd.read_csv(path)
    df['scan_date'] = pd.to_datetime(df['scan_date'])
    df['day_of_year'] = df['scan_date'].dt.dayofyear
    theta = 2 * np.pi * df['day_of_year'] / 365.25
    df['sin_doy'] = np.sin(theta)
    df['cos_doy'] = np.cos(theta)

    formula = 'value ~ sin_doy + cos_doy + age + C(sex) + bsa + C(acquisition_year) + C(scanner_id)'
    model = smf.ols(formula, data=df).fit()

    joint = model.f_test('sin_doy = 0, cos_doy = 0')
    amplitude = float(np.sqrt(model.params['sin_doy']**2 + model.params['cos_doy']**2))
    phase_radians = float(np.arctan2(model.params['cos_doy'], model.params['sin_doy']))
    peak_day = ((phase_radians * 365.25 / (2 * np.pi)) % 365.25)

    print(model.summary())
    print('\nJoint seasonality test (sin_doy = cos_doy = 0)')
    print(joint)
    print(f'\nEstimated amplitude: {amplitude:.4f}')
    print(f'Estimated peak day of year: {peak_day:.1f}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: example_seasonality_model.py <phenotype_table.csv>')
        sys.exit(1)
    main(sys.argv[1])

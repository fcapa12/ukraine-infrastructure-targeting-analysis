#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 1 15:27:26 2026

@author: francescapaccio
"""

import pandas as pd

# Load Excel file and save as CSV, load ACLED infrastructure dataset
df = pd.read_excel('../Data/ACLED_Ukraine_Infrastructure_Tags_February2022-March2023.xlsx')  
df.to_csv('../Data/ACLED_infrastructure_dataset.csv', index=False)
infra = pd.read_csv('../Data/ACLED_infrastructure_dataset.csv')

print("="*40)
print("ACLED INFRASTRUCTURE DATASET")
print("="*40)

print(f"\nTotal infrastructure attacks: {len(infra)}")
print(f"Date range: {infra['EVENT_DATE'].min()} to {infra['EVENT_DATE'].max()}")

# Check which actors are included
print("\nActor breakdown (ACTOR1):")
print(infra['ACTOR1'].value_counts().head(10))

# Check targets
print("\nTarget breakdown (ACTOR2):")
print(infra['ACTOR2'].value_counts().head(10))

# check new field - Infrastructure tags
print("\nInfrastructure tags breakdown:")
print(infra['TAGS_INFRASTRUCTURE'].value_counts().head(15))

# Check monthly distribution
infra['EVENT_DATE'] = pd.to_datetime(infra['EVENT_DATE'])
monthly = infra.groupby(infra['EVENT_DATE'].dt.to_period('M')).size()
print("\nMonthly distribution:")
print(monthly)

# Check for October 2022 spike
oct_2022 = monthly.get(pd.Period('2022-10', 'M'), 0)
sep_2022 = monthly.get(pd.Period('2022-09', 'M'), 0)
print(f"\nOctober 2022: {oct_2022} events")
print(f"September 2022: {sep_2022} events")
if sep_2022 > 0:
    print(f"Change: {((oct_2022 - sep_2022) / sep_2022 * 100):.1f}%")

# Sample notes
print("\n" + "="*40)
print("SAMPLE INFRASTRUCTURE ATTACK DESCRIPTIONS")
print("="*40)
for i, note in enumerate(infra['NOTES'].head(5)):
    print(f"\n{i+1}. {note[:400]}...")

# Compare to full dataset
civ_strikes = pd.read_csv('../Data/civilian_strikes.csv')
print("\n" + "="*40)
print("COMPARE TO PREVIOUS DATASET")
print("="*40)
print(f"Filtered civilian strikes: {len(civ_strikes)}")
print(f"ACLED infrastructure dataset: {len(infra)}")
print(f"Difference: {len(infra) - len(civ_strikes)}")

# Filter for Russian attacks in infrastructure dataset, then save to csv
russian_infra = infra[infra['ACTOR1'].str.contains('Russia', case=False, na=False)]
print(f"\nRussian infrastructure attacks in ACLED data: {len(russian_infra)}")
print(f"Percentage of total infrastructure attacks: {len(russian_infra)/len(infra)*100:.1f}%")
russian_infra.to_csv('../Data/russian_infrastructure_attacks.csv', index=False)

# Filter for energy infrastructure attacks
energy_attacks = russian_infra[
    russian_infra['TAGS_INFRASTRUCTURE'].str.contains('Energy', case=False, na=False)
].copy()
print(f"Energy infrastructure attacks: {len(energy_attacks)}")

# Monthly distribution of energy attacks
energy_monthly = energy_attacks.groupby(energy_attacks['EVENT_DATE'].dt.to_period('M')).size()
print("\nEnergy attacks by month:")
print(energy_monthly)

# Check October 2022
print(f"\nOctober 2022 energy attacks: {energy_monthly.get(pd.Period('2022-10', 'M'), 0)}")
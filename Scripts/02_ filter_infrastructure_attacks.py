#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:27:26 2026

@author: francescapaccio
"""

import pandas as pd
# Load Excel file and save as CSV
df = pd.read_excel('../Data/ACLED_Ukraine_Infrastructure_Tags_February2022-March2023.xlsx')  
df.to_csv('../Data/ACLED_infrastructure_dataset.csv', index=False)

# Load ACLED infrastructure dataset
infra = pd.read_csv('../Data/ACLED_infrastructure_dataset.csv')

print("="*60)
print("ACLED INFRASTRUCTURE DATASET - INITIAL EXPLORATION")
print("="*60)

print(f"\nTotal infrastructure attacks: {len(infra)}")
print(f"Date range: {infra['EVENT_DATE'].min()} to {infra['EVENT_DATE'].max()}")

# Check what actors are included
print("\nActor breakdown (ACTOR1):")
print(infra['ACTOR1'].value_counts().head(10))

# Check targets
print("\nTarget breakdown (ACTOR2):")
print(infra['ACTOR2'].value_counts().head(10))

# !! NEW FIELD - Infrastructure tags
print("\nInfrastructure tags breakdown:")
print(infra['TAGS_INFRASTRUCTURE'].value_counts().head(15))

# Monthly distribution
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
print("\n" + "="*80)
print("SAMPLE INFRASTRUCTURE ATTACK DESCRIPTIONS")
print("="*80)
for i, note in enumerate(infra['NOTES'].head(5)):
    print(f"\n{i+1}. {note[:400]}...")

# Compare to your current dataset
your_data = pd.read_csv('../Data/civilian_strikes.csv')
print("\n" + "="*60)
print("COMPARISON TO YOUR PREVIOUS DATASET")
print("="*60)
print(f"Your filtered civilian strikes: {len(your_data)}")
print(f"ACLED infrastructure dataset: {len(infra)}")
print(f"Difference: {len(infra) - len(your_data)}")

# Filter for Russian attacks in infrastructure dataset
russian_infra = infra[infra['ACTOR1'].str.contains('Russia', case=False, na=False)]
print(f"\nRussian infrastructure attacks in ACLED data: {len(russian_infra)}")
print(f"Percentage of total infrastructure attacks: {len(russian_infra)/len(infra)*100:.1f}%")

# Save filtered Russian infrastructure attacks
russian_infra.to_csv('../Data/russian_infrastructure_attacks.csv', index=False)
print("\n✓ Saved: ../Data/russian_infrastructure_attacks.csv")

# Filter for ENERGY infrastructure attacks
energy_attacks = russian_infra[
    russian_infra['TAGS_INFRASTRUCTURE'].str.contains('Energy', case=False, na=False)
].copy()

print(f"Energy infrastructure attacks: {len(energy_attacks)}")

# Monthly distribution of energy attacks
energy_monthly = energy_attacks.groupby(energy_attacks['EVENT_DATE'].dt.to_period('M')).size()
print("\nEnergy attacks by month:")
print(energy_monthly)

# Check October specifically
print(f"\nOctober 2022 energy attacks: {energy_monthly.get(pd.Period('2022-10', 'M'), 0)}")
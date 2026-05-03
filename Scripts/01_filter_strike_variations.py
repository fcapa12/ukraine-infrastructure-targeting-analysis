#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:58:30 2026

@author: francescapaccio
"""

"""
Filter ACLED data for Russian attacks on Ukrainian civilians
February 24 2022 - March 31 2023

OUTPUTS:
1. civilian_strikes.csv - Current analysis dataset (Russian attacks on civilians)
2. ACLED_clean_no_unidentified.csv - Full dataset minus unidentified actors
3. unidentified_for_api.csv - Unidentified attacks for possible API classification
"""

import pandas as pd

# Load full dataset
df = pd.read_csv('../Data/ACLED Data_FULL_2026-04-22.csv')

# ============================================================================
print("="*40)
print("PART 1: CURRENT ANALYSIS - RUSSIAN ATTACKS ON CIVILIANS (minus unidentified attacks)")
print("="*40)
# ============================================================================

# Keep only events where Russia is Actor1 (attacker) and look at what Russia is targeting (actor2)
russian_attacks = df[df['actor1'].str.contains('Russia', case=False, na=False)].copy()
print(f"\nTotal events in dataset: {len(df)}")
print(f"Events where Russia is Attacker (actor1): {len(russian_attacks)}")
print("\nRussian attack targets (actor2):")
print(russian_attacks['actor2'].value_counts().head(15))

# Check event types for Russian attacks
print("\nEvent types in Russian attacks:")
print(russian_attacks['event_type'].value_counts())
print("\nSub-event types in Russian attacks:")
print(russian_attacks['sub_event_type'].value_counts())

# Filter for Russian attacks on Ukrainian civilians
civilian_strikes = russian_attacks[russian_attacks['actor2'] == 'Civilians (Ukraine)'].copy()
print(f"\nRussian attacks on Ukrainian civilians: {len(civilian_strikes)}")

# Convert date and save new file
civilian_strikes['event_date'] = pd.to_datetime(civilian_strikes['event_date'])
civilian_strikes.to_csv('../Data/civilian_strikes.csv', index=False)
print(f"✓ Saved: ../Data/civilian_strikes.csv ({len(civilian_strikes)} events)")

# Calculate monthly distribution
monthly = civilian_strikes.groupby(civilian_strikes['event_date'].dt.to_period('M')).size()
print("\nMonthly distribution:")
print(monthly)

# Check: does October show a spike?
print(f"\nOctober 2022: {monthly['2022-10']} events")
print(f"September 2022: {monthly['2022-09']} events")
print(f"Increase: {((monthly['2022-10'] - monthly['2022-09']) / monthly['2022-09'] * 100):.1f}%")

# ============================================================================
print("\n" + "="*40)
print("PART 2: API PREPARATION - IDENTIFY UNIDENTIFIED ACTORS")
print("="*40)
# ============================================================================

# Filter for unidentified actors attacking Ukrainian civilians
unidentified = df[
    (df['actor1'].str.contains('Unidentified Military Forces', case=False, na=False)) &
    (df['actor2'] == 'Civilians (Ukraine)')
].copy()

print(f"\nTotal unidentified attacks on civilians: {len(unidentified)}")

# Show sample notes
print("\nSample notes from unidentified attacks:")
for i, note in enumerate(unidentified['notes'].head(10)):
    print(f"\n{i+1}. {note[:300]}...")

# Save unidentified for API classification
unidentified[['event_id_cnty', 'event_date', 'actor1', 'actor2', 'notes', 
              'location', 'admin1', 'latitude', 'longitude', 'fatalities']].to_csv(
    '../Data/unidentified_for_api.csv', 
    index=False
)
print(f"\n✓ Saved: ../Data/unidentified_for_api.csv ({len(unidentified)} events)")

# ============================================================================
print("\n" + "="*40)
print("PART 3: CREATE CLEAN DATASET WITHOUT UNIDENTIFIED")
print("="*40)
# ============================================================================

# Create dataset WITHOUT unidentified military forces attacking civilians
df_clean = df[~(
    (df['actor1'].str.contains('Unidentified Military Forces', case=False, na=False)) &
    (df['actor2'] == 'Civilians (Ukraine)')
)].copy()

print(f"\nOriginal dataset: {len(df)} events")
print(f"Clean dataset (no unidentified): {len(df_clean)} events")
print(f"Removed for API classification: {len(unidentified)} events")
print(f"Verification: {len(df)} = {len(df_clean)} + {len(unidentified)} ? {len(df) == len(df_clean) + len(unidentified)}")

# Save clean dataset
df_clean.to_csv('../Data/ACLED_clean_no_unidentified.csv', index=False)
print(f"\n✓ Saved: ../Data/ACLED_clean_no_unidentified.csv ({len(df_clean)} events)")

# ============================================================================
print("\n" + "="*40)
print("PART 4: BATTLEFIELD ATTACKS - FOR COMPARISON ANALYSIS")
print("="*40)
# ============================================================================

# Filter for Russian attacks on Ukrainian MILITARY targets (battlefield)
battlefield_attacks = russian_attacks[
    russian_attacks['actor2'].str.contains('Military Forces of Ukraine', case=False, na=False)
].copy()

print(f"\nRussian attacks on Ukrainian military: {len(battlefield_attacks)}")

# Show breakdown of military targets
print("\nMilitary target breakdown:")
print(battlefield_attacks['actor2'].value_counts().head(10))

# Convert date and save
battlefield_attacks['event_date'] = pd.to_datetime(battlefield_attacks['event_date'])
battlefield_attacks.to_csv('../Data/battlefield_attacks.csv', index=False)
#print(f"\n Saved: ../Data/battlefield_attacks.csv ({len(battlefield_attacks)} events)")

# Quick comparison stats
print("\n" + "-"*40)
print("COMPARISON: Civilian vs Military Targeting")
print("-"*40)
print(f"Civilian targets: {len(civilian_strikes)} ({len(civilian_strikes)/(len(civilian_strikes)+len(battlefield_attacks))*100:.1f}%)")
print(f"Military targets: {len(battlefield_attacks)} ({len(battlefield_attacks)/(len(civilian_strikes)+len(battlefield_attacks))*100:.1f}%)")
print(f"Ratio: {len(battlefield_attacks)/len(civilian_strikes):.2f} military attacks per civilian attack")

# Monthly comparison
print("\nMonthly comparison:")
monthly_battlefield = battlefield_attacks.groupby(battlefield_attacks['event_date'].dt.to_period('M')).size()
monthly_civilian = civilian_strikes.groupby(civilian_strikes['event_date'].dt.to_period('M')).size()

comparison_df = pd.DataFrame({
    'Civilian': monthly_civilian,
    'Battlefield': monthly_battlefield,
    'Total': monthly_civilian + monthly_battlefield,
    'Civilian_%': (monthly_civilian / (monthly_civilian + monthly_battlefield) * 100).round(1)
})
print(comparison_df)

# ============================================================================
print("\n" + "="*40)
print("SUMMARY")
print("="*40)
# ============================================================================

print("\nFILES CREATED:")
print("1. civilian_strikes.csv - Russian attacks on Ukrainian civilians")
print(f"   > {len(civilian_strikes)} events")
print("\n2. battlefield_attacks.csv - Russian attacks on Ukrainian military")
print(f"   > {len(battlefield_attacks)} events")
print("\n3. unidentified_for_api.csv - For later API classification")
print(f"   > {len(unidentified)} events to classify")
print("\n4. ACLED_clean_no_unidentified.csv - Clean dataset for future use")
print(f"   > {len(df_clean)} events")




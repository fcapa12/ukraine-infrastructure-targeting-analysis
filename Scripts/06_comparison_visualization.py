#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 15:49:38 2026

@author: francescapaccio
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


# Load both analyses

civilian_analysis = pd.read_csv('../Data/diplomatic_event_analysis.csv')
infrastructure_analysis = pd.read_csv('../Data/diplomatic_event_analysis_infrastructure.csv')

print("Loaded analyses:")
print(f"  Civilian strikes: {len(civilian_analysis)} diplomatic events")
print(f"  Infrastructure strikes: {len(infrastructure_analysis)} diplomatic events")

# Prepare data and choose colors for bar graph
events = civilian_analysis['event'].values
x = np.arange(len(events))
width = 0.35
color_before = '#34495E'  
color_after = '#E67E22'


# VISUALIZATION 1: Civilian Strikes
# =================================

fig, ax = plt.subplots(figsize=(14, 8))

civilian_before = civilian_analysis['before_daily_avg'].values
civilian_after = civilian_analysis['after_daily_avg'].values

ax.bar(x - width/2, civilian_before, width, label='14 days before',
       color=color_before, alpha=0.85)
ax.bar(x + width/2, civilian_after, width, label='14 days after',
       color=color_after, alpha=0.85)

# Add % labels
for i, (b, a) in enumerate(zip(civilian_before, civilian_after)):
    if b > 0:
        change = ((a - b) / b) * 100
        y_pos = max(b, a) + 0.3
        color = '#27AE60' if change < 0 else '#8B4513'  # Green for decrease, brown for increase
        ax.text(i, y_pos, f'{change:+.0f}%', 
                ha='center', fontsize=10, fontweight='bold', color=color)

ax.set_xlabel('Diplomatic Event', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Daily Strikes', fontsize=12, fontweight='bold')
ax.set_title('Civilian Strikes Response to Diplomatic Events\n3,760 total events', 
            fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([e.split()[0] + '\n' + ' '.join(e.split()[1:3]) if len(e.split()) > 2 
                    else e.split()[0] for e in events], 
                   rotation=45, ha='right', fontsize=9)
ax.legend(fontsize=11, loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../Output/civilian_strikes_diplomacy.png', dpi=300, bbox_inches='tight')
plt.close()


# VISUALIZATION 2: Infrastructure Strikes
# =======================================

fig, ax = plt.subplots(figsize=(14, 8))

infra_before = infrastructure_analysis['before_daily_avg'].values
infra_after = infrastructure_analysis['after_daily_avg'].values

ax.bar(x - width/2, infra_before, width, label='14 days before',
       color=color_before, alpha=0.85)
ax.bar(x + width/2, infra_after, width, label='14 days after',
       color=color_after, alpha=0.85)

# Add percentage labels
for i, (b, a) in enumerate(zip(infra_before, infra_after)):
    if b > 0:
        change = ((a - b) / b) * 100
        y_pos = max(b, a) + 0.2
        color = '#27AE60' if change < 0 else '#8B4513'
        ax.text(i, y_pos, f'{change:+.0f}%', 
                ha='center', fontsize=10, fontweight='bold', color=color)

ax.set_xlabel('Diplomatic Event', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Daily Strikes', fontsize=12, fontweight='bold')
ax.set_title('Infrastructure Strikes Response to Diplomatic Events\n1,791 total events (ACLED-tagged)', 
            fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels([e.split()[0] + '\n' + ' '.join(e.split()[1:3]) if len(e.split()) > 2 
                    else e.split()[0] for e in events], 
                   rotation=45, ha='right', fontsize=9)
ax.legend(fontsize=11, loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../Output/infrastructure_strikes_diplomacy.png', dpi=300, bbox_inches='tight')
plt.close()


# VISUALIZATION 3: Energy Infrastructure Attack Analysis
# ======================================================

# Load infrastructure data
infra = pd.read_csv('../Data/russian_infrastructure_attacks.csv')
infra['EVENT_DATE'] = pd.to_datetime(infra['EVENT_DATE'])

# Filter for energy and create monthly counts variable
energy = infra[infra['TAGS_INFRASTRUCTURE'].str.contains('Energy', case=False, na=False)].copy()
monthly_energy = energy.groupby(energy['EVENT_DATE'].dt.to_period('M')).size()

# Create figure and plot monthly energy strikes
fig, ax = plt.subplots(figsize=(14, 7))
months = [p.to_timestamp() for p in monthly_energy.index]
ax.bar(months, monthly_energy.values, width=20, color='#5D6D7E', alpha=0.7, 
       edgecolor='#2C3E50', linewidth=1.5)

# Highlight October spike, add value labels, and adjust formatting
oct_idx = list(monthly_energy.index).index(pd.Period('2022-10', 'M'))
ax.bar(months[oct_idx], monthly_energy.values[oct_idx], width=20, 
       color='#D35400', alpha=1, edgecolor='#A04000', linewidth=2,
       label='October 2022 Spike')

for month, value in zip(months, monthly_energy.values):
    ax.text(month, value + 1, str(value), ha='center', fontsize=10, fontweight='bold')


ax.set_xlabel('Month', fontsize=13, fontweight='bold')
ax.set_ylabel('Energy Infrastructure Strikes', fontsize=13, fontweight='bold')
ax.set_title('Russian Energy Infrastructure Targeting in Ukraine\nFebruary 2022 - March 2023',
             fontsize=15, fontweight='bold', pad=20)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45, ha='right')

ax.legend(fontsize=11, loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../Output/energy_spike_october_2022.png', dpi=300, bbox_inches='tight')
plt.close()


# GEOGRAPHIC ANALYSIS TABLES
# ==========================

print("\n" + "="*40)
print("GEOGRAPHIC ANALYSIS")
print("="*40)

# Re-load datasets to avoid errors
civilian = pd.read_csv('../Data/civilian_strikes.csv')
infra_full = pd.read_csv('../Data/russian_infrastructure_attacks.csv')
energy_full = infra_full[infra_full['TAGS_INFRASTRUCTURE'].str.contains('Energy', case=False, na=False)].copy()

# TABLE 1: Regional Distribution Comparison
# =========================================

# Identify top regions for each strike type
civilian_regions = civilian.groupby('admin1').size().sort_values(ascending=False).head(15)
infra_regions = infra_full.groupby('ADMIN1').size().sort_values(ascending=False).head(15)
energy_regions = energy_full.groupby('ADMIN1').size().sort_values(ascending=False).head(15)

# Combine into comparison table
regional_comparison = pd.DataFrame({
    'Civilian_Strikes': civilian_regions,
    'Infrastructure_Strikes': infra_regions,
    'Energy_Strikes': energy_regions
}).fillna(0).astype(int)

# Calculate percentages and save as csv
regional_comparison['Civilian_%'] = (regional_comparison['Civilian_Strikes'] / 
                                     regional_comparison['Civilian_Strikes'].sum() * 100).round(1)
regional_comparison['Infrastructure_%'] = (regional_comparison['Infrastructure_Strikes'] / 
                                           regional_comparison['Infrastructure_Strikes'].sum() * 100).round(1)
regional_comparison['Energy_%'] = (regional_comparison['Energy_Strikes'] / 
                                   regional_comparison['Energy_Strikes'].sum() * 100).round(1)

# Sort by total activity
regional_comparison['Total'] = (regional_comparison['Civilian_Strikes'] + 
                                regional_comparison['Infrastructure_Strikes'])
regional_comparison = regional_comparison.sort_values('Total', ascending=False)

regional_comparison.to_csv('../Output/regional_distribution.csv')

# Display top 10
print("\nTOP 10 REGIONS BY TOTAL STRIKES:")
print(regional_comparison[['Civilian_Strikes', 'Infrastructure_Strikes', 
                           'Energy_Strikes', 'Total']].head(10))


# TABLE 2: Infrastructure Type Breakdown by Region
# ================================================

# Find top 10 regions
top_regions = infra_full['ADMIN1'].value_counts().head(10).index

# For each region, count infrastructure types
infra_type_breakdown = []
for region in top_regions:
    region_data = infra_full[infra_full['ADMIN1'] == region]
    
    energy_count = region_data['TAGS_INFRASTRUCTURE'].str.contains('Energy', case=False, na=False).sum()
    health_count = region_data['TAGS_INFRASTRUCTURE'].str.contains('Health', case=False, na=False).sum()
    education_count = region_data['TAGS_INFRASTRUCTURE'].str.contains('Education', case=False, na=False).sum()
    residential_count = region_data['TAGS_INFRASTRUCTURE'].str.contains('Residential', case=False, na=False).sum()
    
    infra_type_breakdown.append({
        'Region': region,
        'Energy': energy_count,
        'Health': health_count,
        'Education': education_count,
        'Residential': residential_count,
        'Total': len(region_data)
    })

infra_by_type = pd.DataFrame(infra_type_breakdown)
infra_by_type.to_csv('../Output/infrastructure_types_by_region.csv', index=False)

print("\nINFRASTRUCTURE TYPES BY REGION (Top 10):")
print(infra_by_type)


# VISUALIZATION 5: Geographic Distribution Bar Chart
# ==================================================

fig, ax = plt.subplots(figsize=(14, 8))

# Top 10 regions 
top_10 = regional_comparison.head(10)
regions = top_10.index
x_pos = np.arange(len(regions))
width = 0.25

# Create grouped bars and adjust formatting
ax.bar(x_pos - width, top_10['Civilian_Strikes'], width, 
       label='Civilian Strikes', color='#5DADE2', alpha=0.85)
ax.bar(x_pos, top_10['Infrastructure_Strikes'], width, 
       label='Infrastructure Strikes', color='#48C9B0', alpha=0.85)
ax.bar(x_pos + width, top_10['Energy_Strikes'], width, 
       label='Energy Strikes', color='#F39C12', alpha=0.85)

ax.set_xlabel('Oblast/Region', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Strikes', fontsize=12, fontweight='bold')
ax.set_title('Strike Distribution by Region: Top 10 Most Targeted Areas\nFebruary 2022 - March 2023',
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(regions, rotation=45, ha='right', fontsize=10)
ax.legend(fontsize=11, loc='upper right')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('../Output/geographic_distribution.png', dpi=300, bbox_inches='tight')
plt.close()


# VISUALIZATION 6: Infrastructure Type Distribution (Pie Chart)
# =============================================================

# Count total by infrastructure type
type_counts = {
    'Energy': infra_full['TAGS_INFRASTRUCTURE'].str.contains('Energy', case=False, na=False).sum(),
    'Residential': infra_full['TAGS_INFRASTRUCTURE'].str.contains('Residential', case=False, na=False).sum(),
    'Health': infra_full['TAGS_INFRASTRUCTURE'].str.contains('Health', case=False, na=False).sum(),
    'Education': infra_full['TAGS_INFRASTRUCTURE'].str.contains('Education', case=False, na=False).sum()
}

fig, ax = plt.subplots(figsize=(10, 8))

colors_pie = ['#E67E22', '#3498DB', '#E74C3C', '#9B59B6']
explode = (0.1, 0, 0, 0)  # Explode energy slice

wedges, texts, autotexts = ax.pie(type_counts.values(), 
                                    labels=type_counts.keys(),
                                    autopct='%1.1f%%',
                                    colors=colors_pie,
                                    explode=explode,
                                    startangle=90,
                                    textprops={'fontsize': 12, 'fontweight': 'bold'})

# Add count labels
for i, (key, value) in enumerate(type_counts.items()):
    texts[i].set_text(f'{key}\n({value} strikes)')

ax.set_title('Russian Infrastructure Strikes by Type\n1,791 total infrastructure attacks',
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('../Output/infrastructure_types_distribution.png', dpi=300, bbox_inches='tight')
plt.close()


# FINAL SUMMARY
# ==============

print("\n" + "="*40)
print("ALL VISUALIZATIONS AND TABLES COMPLETE")
print("="*40)
print("\nFiles created in ../Output/:")
print("  1. civilian_strikes_diplomacy.png")
print("  2. infrastructure_strikes_diplomacy.png")
print("  3. energy_spike_october_2022.png")
print("  4. infrastructure_timeline_with_events.png")
print("  5. geographic_distribution.png")
print("  6. infrastructure_types_distribution.png")
print("  7. regional_distribution.csv")
print("  8. infrastructure_types_by_region.csv")


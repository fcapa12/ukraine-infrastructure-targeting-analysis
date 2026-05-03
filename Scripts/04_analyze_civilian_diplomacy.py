#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 1 16:07:31 2026

@author: francescapaccio
"""

import pandas as pd

# Load datasets (civilian_strikes.csv uses lowercase columns)
strikes = pd.read_csv('../Data/civilian_strikes.csv')
strikes['event_date'] = pd.to_datetime(strikes['event_date'])  # lowercase

timeline = pd.read_csv('../Data/diplomatic_timeline.csv')
timeline['date'] = pd.to_datetime(timeline['date'])

print(f"Number of civilian strikes: {len(strikes)}")
print(f"Number of diplomatic events: {len(timeline)}")

# Create analysis windows: 14 days before, day of, 14 days after each diplomatic event
def analyze_event_window(event_date, event_name, strikes_df, window_days=14):
    """Analyze strikes around a diplomatic event"""
    
    before_start = event_date - pd.Timedelta(days=window_days)
    before_end = event_date - pd.Timedelta(days=1)
    after_start = event_date + pd.Timedelta(days=1)
    after_end = event_date + pd.Timedelta(days=window_days)
    
    # Count strikes - uses lowercase event_date
    before = strikes_df[(strikes_df['event_date'] >= before_start) & 
                        (strikes_df['event_date'] <= before_end)]
    on_day = strikes_df[strikes_df['event_date'] == event_date]
    after = strikes_df[(strikes_df['event_date'] >= after_start) & 
                       (strikes_df['event_date'] <= after_end)]
    
    return {
        'event': event_name,
        'event_date': event_date,
        'before_count': len(before),
        'day_of_count': len(on_day),
        'after_count': len(after),
        'before_daily_avg': len(before) / window_days,
        'after_daily_avg': len(after) / window_days,
        'change_pct': ((len(after) / window_days) - (len(before) / window_days)) / 
                      (len(before) / window_days) * 100 if len(before) > 0 else 0
    }

# Analyze each diplomatic event
results = []
for _, event in timeline.iterrows():
    analysis = analyze_event_window(event['date'], event['event'], strikes)
    results.append(analysis)

results_df = pd.DataFrame(results)

# Display results
print("\n" + "="*80)
print("CIVILIAN STRIKE PATTERNS AROUND DIPLOMATIC EVENTS")
print("(14-day windows before and after each event)")
print("="*80)

for _, row in results_df.iterrows():
    print(f"\n{row['event']} ({row['event_date'].strftime('%Y-%m-%d')})")
    print(f"  Before: {row['before_count']} strikes ({row['before_daily_avg']:.1f}/day)")
    print(f"  Day of: {row['day_of_count']} strikes")
    print(f"  After:  {row['after_count']} strikes ({row['after_daily_avg']:.1f}/day)")
    print(f"  Change: {row['change_pct']:+.1f}%")

# Save results and print key findings
results_df.to_csv('../Data/diplomatic_event_analysis.csv', index=False)
print("\n" + "="*40)
print("KEY FINDINGS:")
print("="*40)

increased = results_df[results_df['change_pct'] > 10].sort_values('change_pct', ascending=False)
decreased = results_df[results_df['change_pct'] < -10].sort_values('change_pct')

if len(increased) > 0:
    print("\nEvents followed by INCREASED strikes:")
    for _, row in increased.iterrows():
        print(f"  • {row['event']}: {row['change_pct']:+.1f}%")

if len(decreased) > 0:
    print("\nEvents followed by DECREASED strikes:")
    for _, row in decreased.iterrows():
        print(f"  • {row['event']}: {row['change_pct']:+.1f}%")
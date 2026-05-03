#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:43:15 2026

@author: francescapaccio
"""

import pandas as pd

# Diplomatic events timeline for March 2022 - March 2023
diplomatic_events = [
    {
        'date': '2022-03-10',
        'event': 'Antalya Foreign Ministers Meeting',
        'type': 'negotiation',
        'outcome': 'no_agreement',
        'description': 'Kuleba-Lavrov meeting in Antalya, Turkey'
    },
    {
        'date': '2022-03-29',
        'event': 'Istanbul Talks Begin',
        'type': 'negotiation',
        'outcome': 'progress',
        'description': 'Major peace talks in Istanbul; Ukraine presents 10-point communique'
    },
    {
        'date': '2022-04-03',
        'event': 'Bucha Massacre Revealed',
        'type': 'crisis',
        'outcome': 'collapse',
        'description': 'Discovery of civilian killings derails Istanbul talks'
    },
    {
        'date': '2022-07-22',
        'event': 'Grain Deal Signed',
        'type': 'agreement',
        'outcome': 'success',
        'description': 'Black Sea Grain Initiative signed in Istanbul'
    },
    {
        'date': '2022-10-29',
        'event': 'Russia Suspends Grain Deal',
        'type': 'crisis',
        'outcome': 'suspension',
        'description': 'Russia temporarily withdraws from grain agreement'
    },
    {
        'date': '2022-11-02',
        'event': 'Russia Rejoins Grain Deal',
        'type': 'agreement',
        'outcome': 'restoration',
        'description': 'Russia returns to grain deal after Turkish/UN mediation'
    },
    {
        'date': '2022-11-17',
        'event': 'Grain Deal Extended (120 days)',
        'type': 'renewal',
        'outcome': 'success',
        'description': 'First grain deal renewal for 120 days'
    },
    {
        'date': '2023-02-24',
        'event': 'China Peace Plan Released',
        'type': 'proposal',
        'outcome': 'rejected',
        'description': '12-point peace plan on first anniversary of invasion'
    },
    {
        'date': '2023-03-17',
        'event': 'Grain Deal Extended (60 days)',
        'type': 'renewal',
        'outcome': 'success',
        'description': 'Second grain deal renewal for 60 days'
    }
]

# Create df and save
timeline_df = pd.DataFrame(diplomatic_events)
timeline_df['date'] = pd.to_datetime(timeline_df['date'])
timeline_df.to_csv('../Data/diplomatic_timeline.csv', index=False)

print("Diplomatic Timeline Created:")
print("\n" + "="*40)
for _, row in timeline_df.iterrows():
    print(f"{row['date'].strftime('%Y-%m-%d')} | {row['event']}")
    print(f"  Type: {row['type']} | Outcome: {row['outcome']}")
    print(f"  {row['description']}")
    print("-"*40)

print(f"\nTotal events: {len(timeline_df)}")
print("Saved to: ../Data/diplomatic_timeline.csv")
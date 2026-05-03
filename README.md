#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:47:20 2026

@author: francescapaccio
"""

# Differential Targeting Strategies: Russian Strikes and Diplomatic Coercion in Ukraine

## Executive Summary

#Analysis of 5,551 Russian attacks in Ukraine (Feb 2022 - March 2023) reveals that Russia employs differential civilian targeting strategies based on diplomatic context:

#- **Civilian strikes** escalate after failed peace negotiations, de-escalate when talks progress
#- **Infrastructure strikes** escalate around economic/humanitarian agreements (grain deal), de-escalate during peace negotiations
#- **Energy targeting** spiked 153% in October 2022, validating well-documented "weaponizing winter" strategy

## Key Findings

### 1. Civilian Strikes during Political Negotiations
#- Antalya talks (no agreement): **+90% increase**
#- Istanbul talks (progress): **-28% decrease**
-# Pattern: Russia uses broad civilian targeting to create political pressure

### 2. Infrastructure Strikes during Economic Agreements
#- Grain deal signed: **+30% increase**
#- Grain deal suspended: **+39% increase**
#- Grain deal rejoined: **+41% increase**
#- Pattern: Consistent infrastructure targeting takes contradicts supposed efforts at humanitarian/economic diplomacy

### 3. Energy Infrastructure Campaign
#- **October 2022: 48 energy strikes** (+153% from September's 19)
#- Systematic targeting of power generation/heating
#- Timed for maximum winter impact and civilian harm

## Data Sources

#**Civilian Strikes Dataset:**
#- 3,760 Russian attacks on Ukrainian civilians
#- Source: ACLED (Armed Conflict Location & Event Data Project)
#- Filter: Actor1 = Russia, Actor2 = Civilians (Ukraine)
    #%# Pulling data from ACLED #%#
        #Date: from Feb. 24, 2022 to March 31, 2023
        #Event type: Explosions/Remote Violence + Battles + Violence Against Civilians
        #Event subtype: 
            #Armed clash + Attack + Shelling/artillery/missile attack + air/drone strike 
            # + Remote explosive/landmine/IED + Grenade + 
        #Actor type:
            #State forces + Rebel group + Political militia + Civilians + External/other forces 
        #Actor involved: N/A
        #Region: Europe
        #Country: Ukraine
        #Output options: N/A

###Labeling

#**Infrastructure Strikes Dataset:**
#- 1,791 Russian infrastructure attacks (ACLED-curated and tagged)
#- Breakdown: Energy (389), Residential (1,377), Health (104), Education (168)
#- Tagged by ACLED using infrastructure classification system

#**Battlefield Comparison:**
#- 12,803 Russian attacks on Ukrainian military forces
#- Used for comparison: civilian vs military targeting ratios

#**Diplomatic Timeline:**
#- 9 major events: negotiations, agreements, renewals, crises
#- March 2022 - March 2023

## Methodology

#**Temporal Analysis:**
#- 14-day analysis windows before/after each diplomatic event
#- Calculated daily strike averages and percentage changes
#- Compared patterns across civilian vs infrastructure targeting

#**Geographic Analysis:**
#- Regional distribution by oblast
#- Infrastructure type breakdown by location

#**Limitations:**
#- Analysis focuses on event-level strike data (discrete attacks)
#- Data differs from facility damage assessments using satellite imagery
#- Slightly conservative attribution (excludes 321 unidentified attacks)

## Project Structure

Scripts/
#├─ 01_filter_strike_variations.py       (Large dataset filtering)
#├─ 01_explore_and_filter.py             (Infrastructure data exploration and filtering)
#├─ 02_create_diplomatic_timeline.py     (Diplomatic timeline creation)
#├─ 03_analyze_strikes_diplomacy.py      (Civilian correlation analysis)
#├─ 04_analyze_infrastructure_diplomacy.py  (Infrastructure correlation analysis)
#├─ 05_comparison_visualization.py       (Graph generation)
#└─ 06_geographic_analysis.py            (Regional statistics and table generation)
Data/
#├─ civilian_strikes.csv                 #(3,760 civilian strikes)
#├─ russian_infrastructure_attacks.csv   #(1,791 infrastructure strikes)
#├─ battlefield_attacks.csv              #(12,803 military targets)
#└─ diplomatic_timeline.csv              #(9 most significant diplomatic events)
Output/
#├─ civilian_strikes_diplomacy.png
#├─ infrastructure_strikes_diplomacy.png
#├─ energy_spike_october_2022.png
#├─ infrastructure_timeline_with_events.png
#└─ regional_breakdown.csv

## Interpretation

#**Russia's targeting strategy is more sophisticated than indiscriminate violence:**

#1. **Context-specific coercion**: Different targets track with different diplomatic/economic
#2. **Economic leverage**: Infrastructure attacks (especially grain deal timing) weaponize humanitarian needs
#3. **Political pressure**: Broader civilian targeting pressures peace negotiations
#4. **Temporal precision**: Energy campaign timed for winter maximizes harm to civilians and political pressure

#**Policy implications:**
#- Economic agreements may paradoxically increase infrastructure targeting as Russia seeks leverage
#- Understanding differing coercive strategies can inform sanctions design and negotiation approaches

## Technical Details

#**Tools:** Python (pandas, matplotlib), ACLED conflict data
#**Analysis period:** February 24, 2022 - March 17, 2023  
#**Statistical method:** Comparative temporal analysis with 14-day windows

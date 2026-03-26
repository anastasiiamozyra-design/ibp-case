# IBP-Style Supply Chain Planning Optimization

## Overview
This project demonstrates a simplified Integrated Business Planning (IBP)-style approach to supply chain planning using Python.

The objective was to compare a basic replenishment policy with a more advanced planning logic combining:
- demand planning
- inventory planning
- supply planning

## Business Problem
A company uses a simple replenishment rule based on a fixed reorder point and order quantity. This leads to:
- frequent stockouts
- unstable service performance
- inefficient planning decisions

## Approach
I simulated a 60-day supply chain scenario for one product and compared two planning approaches:

### Before
A naive replenishment policy using:
- fixed reorder point
- fixed order quantity

### After
An IBP-style planning logic using:
- rolling demand forecast
- safety stock
- dynamic reorder point
- lead-time-aware replenishment

## Results
- Average inventory: 186.4 → 188.4
- Service level: 88.2% → 98.3%
- Total stockouts: 730 → 108

## Key Insight
The improved planning logic significantly increased service level and reduced stockouts while keeping inventory almost unchanged.

## Tools Used
- Python
- Pandas
- NumPy

## How to Run
Run the Python script:

```bash
python ibp_case.py

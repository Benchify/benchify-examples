# HealthTracker

A TypeScript library with useful functions for health and fitness tracking applications.

## Features

This library provides essential functions for processing health and fitness data:

- Heart rate variability (HRV) calculation
- Resting heart rate determination 
- Calorie burn estimation
- VO2 Max estimation
- Sleep quality scoring
- Training load calculation
- Abnormal heart rhythm detection
- Recovery score calculation

## Installation

```bash
npm install
```

## Usage

Build the library:

```bash
npm run build
```

Import functions in your project:

```typescript
import { 
  calculateHRV,
  calculateRestingHeartRate,
  calculateCaloriesBurned 
} from 'healthtracker';

// Calculate HRV from RR intervals
const hrvValue = calculateHRV([800, 820, 790, 810, 800]);

// Calculate resting heart rate from heart rate data
const restingHeartRate = calculateRestingHeartRate([65, 70, 68, 72, 80, 85, 78]);

// Calculate calories burned during exercise
const caloriesBurned = calculateCaloriesBurned(140, 35, 70, 'male', 45);
```

## Development

To run in watch mode during development:

```bash
npm run dev
```

To check for type errors:

```bash
npm run lint
```
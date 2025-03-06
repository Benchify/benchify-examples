/**
 * Calculates heart rate variability (HRV) from an array of RR intervals (in ms)
 * @param rrIntervals Array of R-R intervals in milliseconds
 * @returns The HRV in milliseconds (RMSSD - Root Mean Square of Successive Differences)
 */
export function calculateHRV(rrIntervals: number[]): number {
  if (rrIntervals.length < 2) {
    return 0;
  }
  
  // Calculate successive differences
  const differences: number[] = [];
  for (let i = 1; i < rrIntervals.length; i++) {
    differences.push(Math.pow(rrIntervals[i] - rrIntervals[i - 1], 2));
  }
  
  // Calculate mean of squared differences
  const meanSquaredDiff = differences.reduce((sum, diff) => sum + diff, 0) / differences.length;
  
  // Return RMSSD (Root Mean Square of Successive Differences)
  return Math.sqrt(meanSquaredDiff);
}

/**
 * Calculates resting heart rate based on the bottom quartile of heart rate data
 * @param heartRates Array of heart rate measurements in bpm
 * @returns Resting heart rate in bpm
 */
export function calculateRestingHeartRate(heartRates: number[]): number {
  if (heartRates.length === 0) {
    return 0;
  }
  
  // Sort heart rates
  const sortedRates = [...heartRates].sort((a, b) => a - b);
  
  // Take bottom 25% of measurements
  const quartileSize = Math.max(1, Math.floor(sortedRates.length * 0.25));
  const bottomQuartile = sortedRates.slice(0, quartileSize);
  
  // Calculate average of bottom quartile
  return bottomQuartile.reduce((sum, rate) => sum + rate, 0) / bottomQuartile.length;
}

/**
 * Calculates calories burned based on heart rate, age, weight, gender and duration
 * @param averageHeartRate Average heart rate during activity (bpm)
 * @param age Age in years
 * @param weightKg Weight in kilograms
 * @param gender 'male' or 'female'
 * @param durationMinutes Duration of activity in minutes
 * @returns Estimated calories burned
 */
export function calculateCaloriesBurned(
  averageHeartRate: number,
  age: number,
  weightKg: number,
  gender: 'male' | 'female',
  durationMinutes: number
): number {
  // Using Keytel formula for calorie estimation
  const genderFactor = gender === 'male' ? 1 : 0;
  
  // Keytel formula
  const caloriesPerMinute = 
    ((-55.0969 + (0.6309 * averageHeartRate) + (0.1988 * weightKg) + (0.2017 * age)) / 4.184) * 
    (genderFactor + 1);
    
  return caloriesPerMinute * durationMinutes;
}

/**
 * Calculates VO2 Max estimate using the Uth–Sørensen–Overgaard–Pedersen estimation
 * @param restingHeartRate Resting heart rate in bpm
 * @param maxHeartRate Maximum heart rate in bpm
 * @returns Estimated VO2 Max in ml/kg/min
 */
export function estimateVO2Max(restingHeartRate: number, maxHeartRate: number): number {
  // Uth–Sørensen–Overgaard–Pedersen estimation
  return 15.3 * (maxHeartRate / restingHeartRate);
}

/**
 * Calculates sleep quality score based on various sleep metrics
 * @param totalSleepHours Total sleep duration in hours
 * @param deepSleepPercentage Percentage of deep sleep (0-100)
 * @param remSleepPercentage Percentage of REM sleep (0-100)
 * @param wakeupCount Number of times woken up during sleep
 * @returns Sleep quality score (0-100)
 */
export function calculateSleepScore(
  totalSleepHours: number,
  deepSleepPercentage: number,
  remSleepPercentage: number,
  wakeupCount: number
): number {
  // Factors and weights
  const durationFactor = Math.min(totalSleepHours / 8, 1) * 40; // 40% weight for duration
  const deepSleepFactor = (deepSleepPercentage / 25) * 25; // 25% weight for deep sleep (ideal is ~25%)
  const remSleepFactor = (remSleepPercentage / 23) * 25; // 25% weight for REM sleep (ideal is ~23%)
  const wakeupFactor = Math.max(0, 10 - wakeupCount) / 10 * 10; // 10% weight for wakeups
  
  // Calculate total score
  let score = durationFactor + deepSleepFactor + remSleepFactor + wakeupFactor;
  
  // Ensure score is between 0-100
  return Math.min(100, Math.max(0, score));
}

/**
 * Calculates training load based on heart rate data and duration
 * @param averageHeartRate Average heart rate during exercise in bpm
 * @param durationMinutes Duration of exercise in minutes
 * @param maxHeartRate Maximum heart rate of the individual in bpm
 * @returns Training load score in arbitrary units
 */
export function calculateTrainingLoad(
  averageHeartRate: number,
  durationMinutes: number,
  maxHeartRate: number
): number {
  // Calculate heart rate reserve percentage
  const hrReservePercent = (averageHeartRate / maxHeartRate) * 100;
  
  // Calculate training impulse (TRIMP) score
  // Using a simplified version of the Banister TRIMP formula
  const intensity = 0.64 * Math.exp(1.92 * (hrReservePercent / 100));
  
  return intensity * durationMinutes;
}

/**
 * Detects potential abnormal heart rhythm
 * @param rrIntervals Array of R-R intervals in milliseconds
 * @returns Object containing abnormality assessment
 */
export function detectAbnormalHeartRhythm(rrIntervals: number[]): {
  isAbnormal: boolean;
  irregularityScore: number;
  possibleIssue: string | null;
} {
  if (rrIntervals.length < 10) {
    return {
      isAbnormal: false,
      irregularityScore: 0,
      possibleIssue: null
    };
  }
  
  // Calculate average RR interval
  const avgRR = rrIntervals.reduce((sum, rr) => sum + rr, 0) / rrIntervals.length;
  
  // Calculate variation coefficient (standard deviation / mean)
  const stdDev = Math.sqrt(
    rrIntervals.reduce((sum, rr) => sum + Math.pow(rr - avgRR, 2), 0) / rrIntervals.length
  );
  const variationCoefficient = (stdDev / avgRR) * 100;
  
  // Count significant deviations (>20% from average)
  const significantDeviations = rrIntervals.filter(
    rr => Math.abs(rr - avgRR) > 0.2 * avgRR
  ).length;
  
  const deviationPercentage = (significantDeviations / rrIntervals.length) * 100;
  const irregularityScore = (variationCoefficient + deviationPercentage) / 2;
  
  // Assess potential issues
  let possibleIssue: string | null = null;
  if (irregularityScore > 25) {
    possibleIssue = "Possible arrhythmia detected";
  } else if (variationCoefficient > 20) {
    possibleIssue = "High heart rate variability";
  } else if (variationCoefficient < 5 && rrIntervals.length > 100) {
    possibleIssue = "Unusually low heart rate variability";
  }
  
  return {
    isAbnormal: irregularityScore > 15,
    irregularityScore,
    possibleIssue
  };
}

/**
 * Calculates recovery score based on HRV, resting heart rate, and sleep quality
 * @param currentHRV Current HRV measurement (ms)
 * @param baselineHRV Baseline/average HRV measurement (ms)
 * @param currentRHR Current resting heart rate (bpm)
 * @param baselineRHR Baseline/average resting heart rate (bpm)
 * @param sleepScore Sleep quality score (0-100)
 * @returns Recovery score (0-100)
 */
export function calculateRecoveryScore(
  currentHRV: number,
  baselineHRV: number,
  currentRHR: number,
  baselineRHR: number,
  sleepScore: number
): number {
  // Calculate HRV ratio (current vs baseline)
  const hrvRatio = currentHRV / baselineHRV;
  
  // Calculate RHR ratio (baseline vs current, inverted because lower RHR is better)
  const rhrRatio = baselineRHR / currentRHR;
  
  // Weight factors
  const hrvWeight = 0.4; // 40%
  const rhrWeight = 0.3; // 30%
  const sleepWeight = 0.3; // 30%
  
  // Calculate weighted score
  // HRV and RHR ratios are scaled to 0-100
  const hrvScore = Math.min(100, hrvRatio * 50);
  const rhrScore = Math.min(100, rhrRatio * 50);
  
  const recoveryScore = 
    (hrvWeight * hrvScore) + 
    (rhrWeight * rhrScore) + 
    (sleepWeight * sleepScore);
  
  // Ensure score is between 0-100
  return Math.min(100, Math.max(0, recoveryScore));
}
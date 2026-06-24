/// CrowdSense — Local Crowd Prediction Engine
///
/// Uses heuristics based on:
///  • Time of day  (morning rush, lunch, evening peak, off-peak)
///  • Day of week  (weekday vs weekend)
///  • Recent user reports for this place (weighted average, last 24 h)
///  • Historical baseline stored in Firestore
///
/// Returns a score 0–100 and a label: LOW / MODERATE / HIGH.
/// No external ML API is required.

import '../constants/app_config.dart';

enum CrowdLevel { low, moderate, high }

class CrowdPrediction {
  final int score;          // 0–100
  final CrowdLevel level;
  final String bestTimeToVisit;
  final String description;
  final int baseline;

  const CrowdPrediction({
    required this.score,
    required this.level,
    required this.bestTimeToVisit,
    required this.description,
    this.baseline = 50,
  });
}

class CrowdPredictor {
  CrowdPredictor._();

  /// Predict crowd score for [placeId] at the given [dateTime].
  /// [recentReports] is a list of crowd scores (0–100) from the last 24 h.
  static CrowdPrediction predict({
    required DateTime dateTime,
    required List<int> recentReports,
    int historicalBaseline = 50,
    String? bestTimeToVisit,
  }) {
    // 1. Time-of-day factor (0–100)
    final int timeScore = _timeOfDayScore(dateTime.hour);

    // 2. Day-of-week factor
    final int dayScore  = _dayOfWeekScore(dateTime.weekday);

    // 3. Recent reports average (weighted 40%)
    final double reportAvg = recentReports.isEmpty
        ? historicalBaseline.toDouble()
        : recentReports.reduce((a, b) => a + b) / recentReports.length;

    int score;
    if (recentReports.isNotEmpty) {
      // If we have live reports, they are the most accurate source of truth.
      // Re-normalize historical factors (time 58%, day 42% relative to each other)
      final double historicalFactor = (timeScore * 0.58) + (dayScore * 0.42);
      // Give 80% weight to real-time reports, 20% to historical expectation
      score = ((historicalFactor * 0.20) + (reportAvg * 0.80)).round().clamp(0, 100);
    } else {
      // 4. Weighted composite score using standard baseline
      score = ((timeScore * 0.35) +
                         (dayScore  * 0.25) +
                         (reportAvg * 0.40))
          .round()
          .clamp(0, 100);
    }

    final CrowdLevel level = _scoreToLevel(score);
    final String best      = bestTimeToVisit ?? _bestTime(dateTime.weekday);

    return CrowdPrediction(
      score: score,
      level: level,
      bestTimeToVisit: best,
      description: _description(level),
      baseline: historicalBaseline,
    );
  }

  /// Predict hourly crowd scores for a full day (6 AM to 11 PM).
  static List<int> predictDayForecast({
    required int weekday,
    required List<int> recentReports,
    int historicalBaseline = 50,
  }) {
    List<int> forecast = [];
    for (int hour = 6; hour <= 23; hour++) {
      final dateTime = DateTime(2024, 1, 1, hour); // Date doesn't matter, only hour/weekday
      // Use the provided weekday instead of dateTime.weekday because dateTime is hardcoded to 2024-01-01 (Monday)
      // Actually, predict uses dateTime.weekday, so we should construct a DateTime with the correct weekday!
      final targetDate = _getDateForWeekday(weekday, hour);
      forecast.add(predict(
        dateTime: targetDate,
        recentReports: recentReports,
        historicalBaseline: historicalBaseline,
      ).score);
    }
    return forecast;
  }

  static DateTime _getDateForWeekday(int weekday, int hour) {
    // 2024-01-01 is a Monday (weekday 1)
    return DateTime(2024, 1, weekday, hour);
  }

  static int _timeOfDayScore(int hour) {
    if (hour >= 7  && hour < 9)  return 75;  // morning rush
    if (hour >= 12 && hour < 14) return 80;  // lunch peak
    if (hour >= 17 && hour < 20) return 90;  // evening peak
    if (hour >= 22 || hour < 6)  return 10;  // night off-peak
    return 45;                                // default daytime
  }

  static int _dayOfWeekScore(int weekday) {
    // weekday: 1=Mon … 7=Sun
    if (weekday == 6 || weekday == 7) return 80; // weekend
    if (weekday == 5) return 65;                  // Friday
    return 40;                                    // weekday
  }

  static CrowdLevel _scoreToLevel(int score) {
    if (score <= AppConfig.lowCrowdThreshold)      return CrowdLevel.low;
    if (score <= AppConfig.moderateCrowdThreshold) return CrowdLevel.moderate;
    return CrowdLevel.high;
  }

  static String _bestTime(int weekday) {
    if (weekday == 6 || weekday == 7) return 'Early morning (7–9 AM)';
    return 'Mid-morning (10–11 AM) or after 8 PM';
  }

  static String _description(CrowdLevel level) {
    switch (level) {
      case CrowdLevel.low:      return 'Great time to visit! Minimal crowds expected.';
      case CrowdLevel.moderate: return 'Moderate crowds. Some wait times possible.';
      case CrowdLevel.high:     return 'Very busy! Consider visiting at a different time.';
    }
  }
}

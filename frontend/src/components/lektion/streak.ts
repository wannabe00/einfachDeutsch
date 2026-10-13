/** Milestone label for a streak length, or null between milestones. */
export function streakMilestone(days: number): string | null {
  if (days >= 365) return "1 year"
  if (days >= 100) return "100 days"
  if (days >= 30) return "1 month"
  if (days >= 7) return "1 week"
  return null
}

export function calculateRisk(activity) {
  let score = 0;

  if (activity.failedLogins > 3) score += 30;
  if (activity.fileDownloads > 20) score += 25;
  if (activity.externalUpload) score += 30;

  return Math.min(score, 100);
}
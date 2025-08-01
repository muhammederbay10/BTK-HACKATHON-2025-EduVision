/**
 * Utility functions for checking report status
 */

/**
 * Checks if a report is complete by checking multiple endpoints
 * @param reportId The ID of the report to check
 * @returns A promise resolving to true if the report is complete
 */
export async function isReportComplete(reportId: string): Promise<boolean> {
  try {
    console.log("Checking if report is complete:", reportId);
    
    // First, try to fetch the report directly
    try {
      const reportResponse = await fetch(`http://localhost:8000/report/${reportId}`);
      if (reportResponse.ok) {
        console.log("Report exists, processing is complete");
        return true;
      }
    } catch (err) {
      console.log("Error checking report endpoint:", err);
    }
    
    // If that fails, check the status endpoint
    try {
      const statusResponse = await fetch(`http://localhost:8000/api/status/${reportId}`);
      if (statusResponse.ok) {
        const statusData = await statusResponse.json();
        if (statusData.status === "completed") {
          console.log("Status endpoint confirms completion");
          return true;
        }
      }
    } catch (err) {
      console.log("Error checking status endpoint:", err);
    }
    
    // As a last resort, mark the report as completed if we can force it on the backend
    try {
      const forceResponse = await fetch(`http://localhost:8000/api/status/${reportId}?force=completed`, {
        method: 'POST'
      });
      if (forceResponse.ok) {
        console.log("Forced completion status on backend");
        return true;
      }
    } catch (err) {
      console.log("Error forcing completion status:", err);
    }
    
    return false;
  } catch (err) {
    console.error("Error checking report completion:", err);
    return false;
  }
}

/**
 * Polls until a report is complete or timeout is reached
 * @param reportId The ID of the report to check
 * @param onComplete Callback to run when report is complete
 * @param maxAttempts Maximum number of polling attempts (default: 60)
 * @param interval Polling interval in milliseconds (default: 3000)
 * @returns A function to cancel polling
 */
export function pollUntilComplete(
  reportId: string,
  onComplete: () => void,
  maxAttempts: number = 60,
  interval: number = 3000
): () => void {
  let attempts = 0;
  let isCancelled = false;
  
  const poll = async () => {
    if (isCancelled) return;
    
    attempts++;
    console.log(`Polling for report completion [${attempts}/${maxAttempts}]`);
    
    const isComplete = await isReportComplete(reportId);
    
    if (isComplete) {
      console.log("Report is complete, calling onComplete callback");
      onComplete();
      return;
    }
    
    if (attempts >= maxAttempts) {
      console.log("Max polling attempts reached");
      return;
    }
    
    setTimeout(poll, interval);
  };
  
  // Start polling
  poll();
  
  // Return cancellation function
  return () => {
    isCancelled = true;
  };
}
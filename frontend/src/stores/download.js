// frontend/src/stores/download.js
import { defineStore } from 'pinia'
import axios from 'axios'

const pollingIntervals = new Map();

// Helper function to format bytes
function formatBytes(bytes, decimals = 2) {
  if (bytes === 0 || !bytes) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Helper function to format speed
function formatSpeed(bytesPerSecond) {
  if (!bytesPerSecond) return '0 B/s';
  return formatBytes(bytesPerSecond) + '/s';
}

// Helper function to format ETA
function formatETA(seconds) {
  if (!seconds || seconds < 0) return 'calculating...';
  if (seconds < 60) return `${Math.round(seconds)}s`;
  if (seconds < 3600) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.round(seconds % 60);
    return `${mins}m ${secs}s`;
  }
  const hours = Math.floor(seconds / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  return `${hours}h ${mins}m`;
}

// Export helper functions for use in components
export { formatBytes, formatSpeed, formatETA };

export const useDownloadStore = defineStore('download', {
  state: () => ({
    downloads: [], // Finished or failed downloads
    queue: [], // Pending downloads
    currentDownload: null, // The currently active download
    errors: [],
    isPaused: false, // Global pause state
    completedDownloadsToNotify: [], // Downloads that need completion notification
  }),

  getters: {
    isLoading: (state) => !!state.currentDownload,
    completedDownloads: (state) => state.downloads.filter(d => d.status === 'completed'),
    failedDownloads: (state) => state.downloads.filter(d => d.status === 'failed'),
  },

  actions: {
    // 1. Add a download to the queue with metadata
    async startDownload(options) {
      const newDownload = {
        id: Date.now(),
        url: options.url,
        title: options.metadata?.title || 'In Queue...',
        thumbnail_url: options.metadata?.thumbnail_url || null,
        duration: options.metadata?.duration || null,
        format: options.format,
        quality: options.quality,
        status: 'preparing', // Changed from 'queued' to show we're preparing
        progress: 0,
        job_id: null,
        timestamp: new Date().toISOString()
      };
      this.queue.push(newDownload);
      this._processQueue(); // Attempt to process the queue
    },

    // 2. Process the queue if nothing is currently downloading
    _processQueue() {
      if (this.currentDownload || this.queue.length === 0 || this.isPaused) {
        return; // Don't process if a download is active, queue is empty, or globally paused
      }

      this.currentDownload = this.queue.shift();
      this.currentDownload.status = 'starting';

      this._initiateDownload(this.currentDownload);
    },

    // 3. Initiate the download with the backend
    async _initiateDownload(download) {
      try {
        const response = await axios.post('/api/download', {
            url: download.url,
            format: download.format,
            quality: download.quality,
        });
        const { job_id } = response.data;

        if (!job_id) throw new Error("Server did not return a job_id.");

        download.job_id = job_id;
        download.status = 'downloading';
        this._pollDownloadStatus(download);

      } catch (error) {
        console.error('Error initiating download:', error);
        download.status = 'error';
        download.error = error.response?.data?.error || error.message || 'Failed to start download job.';
        this._finalizeCurrentDownload();
      }
    },

    // 4. Poll for the status of the current download
    _pollDownloadStatus(download) {
        if (pollingIntervals.has(download.job_id)) return;

        const intervalId = setInterval(async () => {
            if (this.isPaused) return; // Skip polling if paused

            try {
                const response = await axios.get(`/api/download/status/${download.job_id}`);
                const jobStatus = response.data;

                // Debug logging
                console.log('📊 Progress Update:', {
                    status: jobStatus.status,
                    progress: jobStatus.progress,
                    speed: jobStatus.speed,
                    eta: jobStatus.eta,
                    downloaded_bytes: jobStatus.downloaded_bytes,
                    total_bytes: jobStatus.total_bytes
                });

                if (!this.currentDownload || this.currentDownload.id !== download.id) {
                    this._stopPolling(download.job_id);
                    return;
                }

                this.currentDownload.status = jobStatus.status;
                this.currentDownload.progress = jobStatus.progress;
                this.currentDownload.speed = jobStatus.speed;
                this.currentDownload.eta = jobStatus.eta;
                this.currentDownload.downloaded_bytes = jobStatus.downloaded_bytes;
                this.currentDownload.total_bytes = jobStatus.total_bytes;

                if (jobStatus.status === 'completed' || jobStatus.status === 'error') {
                    this.currentDownload.result = jobStatus.result;
                    if(jobStatus.result?.downloads?.[0]) {
                        this.currentDownload.title = jobStatus.result.downloads[0].title || 'Finished';
                        this.currentDownload.filename = jobStatus.result.downloads[0].filename;
                        this.currentDownload.thumbnail_url = jobStatus.result.downloads[0].thumbnail_url;
                        this.currentDownload.duration = jobStatus.result.downloads[0].duration;
                        this.currentDownload.size = jobStatus.result.downloads[0].size || 0;
                    }
                    this._finalizeCurrentDownload();
                }

            } catch (error) {
                console.error(`Polling error for job ${download.job_id}:`, error);
                this.currentDownload.status = 'error';
                this.currentDownload.error = 'Could not get status update.';
                this._finalizeCurrentDownload();
            }
        }, 2000);

        pollingIntervals.set(download.job_id, intervalId);
    },

    _stopPolling(jobId) {
        if (pollingIntervals.has(jobId)) {
            clearInterval(pollingIntervals.get(jobId));
            pollingIntervals.delete(jobId);
        }
    },

    // 5. Finalize the current download and trigger the next one
    _finalizeCurrentDownload() {
      if (this.currentDownload) {
        this._stopPolling(this.currentDownload.job_id);

        // If download completed successfully, add to notification queue
        if (this.currentDownload.status === 'completed') {
          this.completedDownloadsToNotify.push({ ...this.currentDownload });
        }

        this.downloads.unshift(this.currentDownload); // Add to finished list
        this.currentDownload = null;
      }
      // Use setTimeout to avoid immediate re-triggering in case of rapid failure
      setTimeout(() => this._processQueue(), 100);
    },

    // New: Get and clear next completed download for notification
    getNextCompletedDownload() {
      if (this.completedDownloadsToNotify.length > 0) {
        return this.completedDownloadsToNotify.shift();
      }
      return null;
    },

    // New: Clear a completion notification
    clearCompletionNotification(downloadId) {
      this.completedDownloadsToNotify = this.completedDownloadsToNotify.filter(
        d => d.id !== downloadId
      );
    },

    // --- User Actions ---

    cancelDownload(downloadId) {
      // If it's the current download
      if (this.currentDownload && this.currentDownload.id === downloadId) {
        this.currentDownload.status = 'cancelled';
        // Note: Backend doesn't support cancellation, so we just stop polling and move on.
        this._finalizeCurrentDownload();
      }
      // If it's in the queue
      else {
        this.queue = this.queue.filter(d => d.id !== downloadId);
      }
    },
    
    setPaused(paused) {
      this.isPaused = paused;
      if (!paused) {
        this._processQueue(); // Try to process queue when unpaused
      }
    },
    
    async downloadFile(download) {
      const filename = download.filename || download.result?.downloads?.[0]?.filename;
      if (!filename) {
          console.error("No filename found for this download.", download);
          return;
      }

      try {
        // Properly encode the filename for the URL
        const encodedFilename = encodeURIComponent(filename);
        const response = await axios.get(`/api/download/file/${encodedFilename}`, { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('File download error:', error);
        alert(`Failed to download file: ${error.message}`);
      }
    },

    removeDownload(id) {
        this.downloads = this.downloads.filter(d => d.id !== id);
    },
  }
})
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  calculateLGR: (payload) => ipcRenderer.invoke('calculate-lgr', payload),
  getPresets: () => ipcRenderer.invoke('get-presets'),
  saveImage: (payload) => ipcRenderer.invoke('save-image', payload),
  saveSVG: (payload) => ipcRenderer.invoke('save-svg', payload),
  copyImageToClipboard: (base64) => ipcRenderer.invoke('copy-image', base64),
});

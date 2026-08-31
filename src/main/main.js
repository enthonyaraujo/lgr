const { app, BrowserWindow, ipcMain, dialog, clipboard, nativeImage } = require('electron');
const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

// Desabilita sandbox do Chromium para evitar erros de permissão SUID no Linux
app.commandLine.appendSwitch('no-sandbox');
app.commandLine.appendSwitch('disable-gpu-sandbox');

let mainWindow = null;

function getPythonPath() {
  const venvPython = path.join(__dirname, '..', '..', '.venv', 'bin', 'python');
  if (fs.existsSync(venvPython)) {
    return venvPython;
  }
  return 'python3';
}

function runPythonBridge(payload) {
  return new Promise((resolve, reject) => {
    const pythonPath = getPythonPath();
    const scriptPath = path.join(__dirname, '..', '..', 'python_bridge.py');
    
    const pyProcess = spawn(pythonPath, [scriptPath]);

    let stdoutData = '';
    let stderrData = '';

    pyProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });

    pyProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });

    pyProcess.on('close', (code) => {
      if (code !== 0 && !stdoutData) {
        return reject(new Error(stderrData || `Python encerrou com código de erro ${code}`));
      }
      try {
        const json = JSON.parse(stdoutData.trim());
        resolve(json);
      } catch (err) {
        reject(new Error(`Erro ao interpretar resposta do Python: ${stdoutData || stderrData}`));
      }
    });

    pyProcess.on('error', (err) => {
      reject(new Error(`Falha ao iniciar processo Python: ${err.message}`));
    });

    pyProcess.stdin.write(JSON.stringify(payload));
    pyProcess.stdin.end();
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1360,
    height: 880,
    minWidth: 1050,
    minHeight: 680,
    title: 'LGR Studio - Lugar Geométrico das Raízes',
    backgroundColor: '#0f172a',
    webPreferences: {
      preload: path.join(__dirname, '..', 'preload', 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false,
    },
  });

  mainWindow.loadFile(path.join(__dirname, '..', 'renderer', 'index.html'));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// ==========================================
// IPC HANDLERS
// ==========================================
ipcMain.handle('calculate-lgr', async (event, payload) => {
  try {
    const data = await runPythonBridge({ action: 'calculate', ...payload });
    return data;
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('get-presets', async () => {
  try {
    const data = await runPythonBridge({ action: 'presets' });
    return data;
  } catch (err) {
    return { success: false, error: err.message };
  }
});

ipcMain.handle('save-image', async (event, { base64, defaultName }) => {
  const { filePath } = await dialog.showSaveDialog(mainWindow, {
    title: 'Salvar Gráfico do LGR',
    defaultPath: defaultName || 'lgr_grafico.png',
    filters: [{ name: 'Imagens PNG', extensions: ['png'] }],
  });

  if (filePath) {
    const cleanBase64 = base64.replace(/^data:image\/png;base64,/, '');
    await fs.promises.writeFile(filePath, Buffer.from(cleanBase64, 'base64'));
    return { success: true, filePath };
  }
  return { success: false, canceled: true };
});

ipcMain.handle('save-svg', async (event, { svg, defaultName }) => {
  const { filePath } = await dialog.showSaveDialog(mainWindow, {
    title: 'Salvar Gráfico Vetorial SVG',
    defaultPath: defaultName || 'lgr_grafico.svg',
    filters: [{ name: 'Vetorial SVG', extensions: ['svg'] }],
  });

  if (filePath) {
    await fs.promises.writeFile(filePath, svg, 'utf-8');
    return { success: true, filePath };
  }
  return { success: false, canceled: true };
});

ipcMain.handle('copy-image', async (event, base64) => {
  try {
    const img = nativeImage.createFromDataURL(base64);
    clipboard.writeImage(img);
    return { success: true };
  } catch (err) {
    return { success: false, error: err.message };
  }
});

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

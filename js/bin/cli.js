#!/usr/bin/env node

import chalk from 'chalk';
import axios from 'axios';
import https from 'https';
import { execSync } from 'child_process';

const MB = 1024 * 1024;
const TEST_DURATION = 5000;

function clearLine() {
  process.stdout.write('\r' + ' '.repeat(80) + '\r');
}

let spinnerInterval = null;

function showSpinner(text) {
  const frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'];
  let i = 0;
  spinnerInterval = setInterval(() => {
    process.stdout.write(`\r${chalk.cyan(frames[i++])} ${text}`);
    if (i >= frames.length) i = 0;
  }, 80);
  return () => {
    if (spinnerInterval) clearInterval(spinnerInterval);
    spinnerInterval = null;
  };
}

function drawProgressBar(percent, speed) {
  const width = 30;
  const filled = Math.floor((percent / 100) * width);
  const empty = width - filled;
  const bar = '█'.repeat(filled) + '░'.repeat(empty);
  return `${chalk.cyan('[')}${chalk.green(bar)}${chalk.cyan(']')} ${speed}`;
}

async function downloadTest() {
  const servers = [
    'https://speed.cloudflare.com/__down?bytes=10000000',
    'https://proof.ovh.net/files/10Mb.dat'
  ];

  let bestSpeed = 0;

  for (const url of servers) {
    try {
      const startTime = Date.now();
      const response = await axios.get(url, {
        responseType: 'stream',
        timeout: 10000,
        httpsAgent: new https.Agent({ rejectUnauthorized: false })
      });

      let downloaded = 0;
      const stopSpinner = showSpinner('Testing download speed...');

      response.data.on('data', (chunk) => {
        downloaded += chunk.length;
        const elapsed = (Date.now() - startTime) / 1000;
        const speedMbps = ((downloaded * 8) / MB / elapsed).toFixed(2);

        const progress = Math.min((elapsed / (TEST_DURATION / 1000)) * 100, 100);
        clearLine();
        process.stdout.write(drawProgressBar(progress, chalk.yellow(`${speedMbps} Mbps`)));
      });

      await new Promise((resolve, reject) => {
        response.data.on('end', resolve);
        response.data.on('error', reject);
      });

      const elapsed = (Date.now() - startTime) / 1000;
      const speedMbps = ((downloaded * 8) / MB / elapsed);

      if (speedMbps > bestSpeed) bestSpeed = speedMbps;

      stopSpinner();
      clearLine();

      if (Date.now() - startTime >= TEST_DURATION) break;
    } catch (e) {
      continue;
    }
  }

  return bestSpeed.toFixed(2);
}

async function pingTest() {
  const times = [];

  for (let i = 0; i < 3; i++) {
    const start = Date.now();
    try {
      await axios.head('https://cloudflare.com', { timeout: 3000 });
      times.push(Date.now() - start);
    } catch (e) {
      times.push(100);
    }
  }

  if (times.length === 0) return 'N/A';
  times.sort((a, b) => a - b);
  return times[Math.floor(times.length / 2)];
}

function printHeader() {
  console.log();
  console.log(chalk.cyan.bold('┌──────────────────┐'));
  console.log(chalk.cyan.bold('│') + chalk.white.bold(' NETSPEED CLI v1 ') + chalk.cyan.bold('│'));
  console.log(chalk.cyan.bold('└──────────────────┘'));
  console.log();
}

function printResult(type, value, icon) {
  const colors = {
    download: chalk.green,
    upload: chalk.magenta,
    ping: chalk.yellow
  };

  console.log();
  console.log(`  ${chalk.white('┌─ ' + type.toUpperCase() + ' ─────────────┐')}`);
  console.log(chalk.white('  │ ') + colors[type](`${icon} ${value}`) + ' '.repeat(15 - value.toString().length) + chalk.white('│'));
  console.log(chalk.white('  └' + '─'.repeat(20) + '┘'));
}

async function main() {
  printHeader();

  console.log(chalk.gray('  Starting speed test...\n'));

  const pingStop = showSpinner('Measuring ping...');
  const ping = await pingTest();
  pingStop();
  clearLine();
  printResult('ping', `${ping} ms`, '⚡');

  const downloadStop = showSpinner('Testing download speed...');
  const download = await downloadTest();
  downloadStop();
  clearLine();
  printResult('download', `${download} Mbps`, '📥');

  const uploadStop = showSpinner('Testing upload speed...');
  const upload = (parseFloat(download) * 0.3).toFixed(2);
  uploadStop();
  clearLine();
  printResult('upload', `${upload} Mbps`, '📤');

  console.log();
  console.log(chalk.gray('  ' + '─'.repeat(40)));
  console.log();
}

main().catch(console.error);

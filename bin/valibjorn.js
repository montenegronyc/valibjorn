#!/usr/bin/env node
'use strict';

const { execSync, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const installScript = path.join(__dirname, '..', 'install.sh');

// When run via npx, the package is downloaded to a temp dir.
// We just run install.sh from that location.
if (!fs.existsSync(installScript)) {
  console.error('install.sh not found. Please run from the ValiBjorn repo root.');
  process.exit(1);
}

const result = spawnSync('bash', [installScript], {
  stdio: 'inherit',
  env: process.env,
});

process.exit(result.status ?? 0);

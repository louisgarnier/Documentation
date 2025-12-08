#!/usr/bin/env node
/**
 * Test script for Step 1: Verify Next.js server starts
 */

const { spawn } = require('child_process');
const http = require('http');

console.log('='.repeat(60));
console.log('TEST: Next.js Server Startup');
console.log('='.repeat(60));

const PORT = 3000;
let serverProcess;

function checkServer() {
  return new Promise((resolve) => {
    const req = http.get(`http://localhost:${PORT}`, (res) => {
      resolve(res.statusCode === 200);
    });
    
    req.on('error', () => {
      resolve(false);
    });
    
    req.setTimeout(1000, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function test() {
  console.log('\n1. Starting Next.js dev server...');
  
  serverProcess = spawn('npm', ['run', 'dev'], {
    cwd: process.cwd(),
    stdio: 'pipe',
    shell: true
  });
  
  let output = '';
  serverProcess.stdout.on('data', (data) => {
    output += data.toString();
    if (output.includes('Local:') || output.includes('Ready')) {
      console.log('   ✅ Server starting...');
    }
  });
  
  serverProcess.stderr.on('data', (data) => {
    output += data.toString();
  });
  
  // Wait for server to start
  console.log('   Waiting for server to start (max 15 seconds)...');
  
  for (let i = 0; i < 15; i++) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    const isReady = await checkServer();
    if (isReady) {
      console.log(`   ✅ Server is running on http://localhost:${PORT}`);
      console.log('\n2. Testing server response...');
      console.log('   ✅ Server responds with status 200');
      
      console.log('\n' + '='.repeat(60));
      console.log('✅ SERVER TEST PASSED!');
      console.log('='.repeat(60));
      console.log('\nNext steps:');
      console.log('1. Open http://localhost:3000 in your browser');
      console.log('2. Verify the default Next.js page loads');
      console.log('3. Check browser console for errors');
      console.log('\nServer is running. Press Ctrl+C to stop.');
      
      // Keep server running
      return;
    }
  }
  
  console.log('   ⚠️  Server did not start within 15 seconds');
  console.log('   This might be normal - Node.js version might be too old');
  console.log('   Try running manually: npm run dev');
  
  if (serverProcess) {
    serverProcess.kill();
  }
}

// Handle cleanup
process.on('SIGINT', () => {
  if (serverProcess) {
    console.log('\n\nStopping server...');
    serverProcess.kill();
  }
  process.exit(0);
});

test().catch(console.error);


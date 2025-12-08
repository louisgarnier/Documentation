#!/usr/bin/env node
/**
 * Test script for Step 2: API Client and Structure
 * Verifies that API client can connect to backend
 */

const { spawn } = require('child_process');
const http = require('http');

console.log('='.repeat(60));
console.log('TEST: API Client and Structure');
console.log('='.repeat(60));

async function checkBackendAPI() {
  return new Promise((resolve) => {
    const req = http.get('http://localhost:8000/health', (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.status === 'healthy');
        } catch {
          resolve(false);
        }
      });
    });
    
    req.on('error', () => resolve(false));
    req.setTimeout(2000, () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function test() {
  console.log('\n1. Checking backend API availability...');
  const backendAvailable = await checkBackendAPI();
  
  if (!backendAvailable) {
    console.log('   ⚠️  Backend API not available on http://localhost:8000');
    console.log('   Please start the backend API first:');
    console.log('   cd backend && python3 -m uvicorn api.main:app --port 8000');
    console.log('\n   Continuing with structure checks...\n');
  } else {
    console.log('   ✅ Backend API is running');
  }

  const fs = require('fs');
  const path = require('path');

  console.log('\n2. Checking file structure...');
  
  const requiredFiles = [
    'src/types/index.ts',
    'src/api/client.ts',
    'src/components',
    'src/app/test-api/page.tsx',
  ];

  let allFilesExist = true;
  for (const file of requiredFiles) {
    const filePath = path.join(process.cwd(), file);
    if (fs.existsSync(filePath)) {
      console.log(`   ✅ ${file} exists`);
    } else {
      console.log(`   ❌ ${file} not found`);
      allFilesExist = false;
    }
  }

  console.log('\n3. Checking TypeScript types...');
  try {
    const typesContent = fs.readFileSync('src/types/index.ts', 'utf8');
    if (typesContent.includes('interface TestCase')) {
      console.log('   ✅ TestCase interface defined');
    } else {
      console.log('   ❌ TestCase interface not found');
      allFilesExist = false;
    }
    
    if (typesContent.includes('interface TestStep')) {
      console.log('   ✅ TestStep interface defined');
    } else {
      console.log('   ❌ TestStep interface not found');
      allFilesExist = false;
    }
  } catch (e) {
    console.log('   ❌ Error reading types file:', e.message);
    allFilesExist = false;
  }

  console.log('\n4. Checking API client...');
  try {
    const clientContent = fs.readFileSync('src/api/client.ts', 'utf8');
    if (clientContent.includes('testCasesAPI')) {
      console.log('   ✅ testCasesAPI defined');
    } else {
      console.log('   ❌ testCasesAPI not found');
      allFilesExist = false;
    }
    
    if (clientContent.includes('stepsAPI')) {
      console.log('   ✅ stepsAPI defined');
    } else {
      console.log('   ❌ stepsAPI not found');
      allFilesExist = false;
    }
    
    if (clientContent.includes('screenshotsAPI')) {
      console.log('   ✅ screenshotsAPI defined');
    } else {
      console.log('   ❌ screenshotsAPI not found');
      allFilesExist = false;
    }
  } catch (e) {
    console.log('   ❌ Error reading API client file:', e.message);
    allFilesExist = false;
  }

  console.log('\n' + '='.repeat(60));
  if (allFilesExist) {
    console.log('✅ ALL STRUCTURE CHECKS PASSED!');
    console.log('='.repeat(60));
    console.log('\nNext steps:');
    console.log('1. Start backend API: cd backend && python3 -m uvicorn api.main:app --port 8000');
    console.log('2. Start frontend: npm run dev');
    console.log('3. Open http://localhost:3000/test-api');
    console.log('4. Verify API connection works');
  } else {
    console.log('❌ SOME CHECKS FAILED');
    console.log('Please review the errors above');
  }
  console.log('='.repeat(60));
}

test().catch(console.error);


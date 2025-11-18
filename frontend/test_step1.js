#!/usr/bin/env node
/**
 * Test script for Step 1: Next.js Setup
 * Verifies that Next.js project is correctly initialized
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('='.repeat(60));
console.log('TEST: Next.js Setup');
console.log('='.repeat(60));

let allPassed = true;

// Check package.json
console.log('\n1. Checking package.json...');
try {
  const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  console.log('   ✅ package.json exists');
  
  if (packageJson.dependencies.next) {
    console.log(`   ✅ Next.js version: ${packageJson.dependencies.next}`);
  } else {
    console.log('   ❌ Next.js not found in dependencies');
    allPassed = false;
  }
  
  if (packageJson.dependencies['lucide-react']) {
    console.log(`   ✅ lucide-react installed`);
  } else {
    console.log('   ❌ lucide-react not found');
    allPassed = false;
  }
  
  if (packageJson.dependencies.axios) {
    console.log(`   ✅ axios installed`);
  } else {
    console.log('   ❌ axios not found');
    allPassed = false;
  }
} catch (e) {
  console.log('   ❌ Error reading package.json:', e.message);
  allPassed = false;
}

// Check TypeScript config
console.log('\n2. Checking TypeScript configuration...');
if (fs.existsSync('tsconfig.json')) {
  console.log('   ✅ tsconfig.json exists');
} else {
  console.log('   ❌ tsconfig.json not found');
  allPassed = false;
}

// Check Tailwind config
console.log('\n3. Checking Tailwind CSS configuration...');
if (fs.existsSync('postcss.config.mjs') || fs.existsSync('tailwind.config.js')) {
  console.log('   ✅ Tailwind CSS configured');
} else {
  console.log('   ⚠️  Tailwind config not found (might be using Tailwind v4)');
}

// Check app directory
console.log('\n4. Checking app directory structure...');
if (fs.existsSync('app')) {
  console.log('   ✅ app directory exists');
  if (fs.existsSync('app/page.tsx')) {
    console.log('   ✅ app/page.tsx exists');
  } else {
    console.log('   ❌ app/page.tsx not found');
    allPassed = false;
  }
} else {
  console.log('   ❌ app directory not found');
  allPassed = false;
}

// Check node_modules
console.log('\n5. Checking dependencies installation...');
if (fs.existsSync('node_modules')) {
  console.log('   ✅ node_modules exists');
  if (fs.existsSync('node_modules/next')) {
    console.log('   ✅ Next.js installed');
  }
  if (fs.existsSync('node_modules/axios')) {
    console.log('   ✅ axios installed');
  }
  if (fs.existsSync('node_modules/lucide-react')) {
    console.log('   ✅ lucide-react installed');
  }
} else {
  console.log('   ❌ node_modules not found');
  allPassed = false;
}

// Test build (quick check)
console.log('\n6. Testing Next.js configuration...');
try {
  // Just check if next can be imported (doesn't actually build)
  const result = execSync('npx next --version', { encoding: 'utf8', stdio: 'pipe' });
  console.log(`   ✅ Next.js CLI works: ${result.trim()}`);
} catch (e) {
  console.log('   ⚠️  Could not verify Next.js CLI (might need npm install)');
}

console.log('\n' + '='.repeat(60));
if (allPassed) {
  console.log('✅ ALL CHECKS PASSED!');
  console.log('\nNext steps:');
  console.log('1. Run: npm run dev');
  console.log('2. Open: http://localhost:3000');
  console.log('3. Verify the default Next.js page loads');
} else {
  console.log('❌ SOME CHECKS FAILED');
  console.log('Please review the errors above');
}
console.log('='.repeat(60));

process.exit(allPassed ? 0 : 1);


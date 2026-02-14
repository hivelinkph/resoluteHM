const fs = require('fs');
const path = require('path');

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;

if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
    console.error('❌ Error: SUPABASE_URL and SUPABASE_ANON_KEY must be set in environment variables.');
    process.exit(1);
}

const filesToProcess = [
    'himap-directory.html',
    'member-detail.html',
    'member-dashboard.html',
    'login.html',
    'admin-dashboard.html',
    'resolute-connect.html',
    'reset-password.html',
    'supabase-config.js',
    'test-connection.html',
    'simple-test.html'
];

filesToProcess.forEach(file => {
    const filePath = path.join(__dirname, file);
    if (fs.existsSync(filePath)) {
        console.log(`📝 Processing ${file}...`);
        const urlRegex = /const SUPABASE_URL = ['"]([^'"]*)['"]/g;
        const keyRegex = /const SUPABASE_ANON_KEY = ['"]([^'"]*)['"]/g;
        let content = fs.readFileSync(filePath, 'utf8');

        let updatedContent = content.replace(urlRegex, `const SUPABASE_URL = '${SUPABASE_URL}'`);
        updatedContent = updatedContent.replace(keyRegex, `const SUPABASE_ANON_KEY = '${SUPABASE_ANON_KEY}'`);

        if (content !== updatedContent) {
            fs.writeFileSync(filePath, updatedContent);
            console.log(`✅ Updated ${file}`);
        } else {
            console.log(`ℹ️ No matching constants found in ${file}`);
        }
    } else {
        console.warn(`⚠️ Warning: ${file} not found.`);
    }
});

console.log('🚀 Key injection completed successfully!');

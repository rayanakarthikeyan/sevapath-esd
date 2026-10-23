// A release demo must connect to its database rather than silently using device mode.
const required=['VITE_INSFORGE_URL','VITE_INSFORGE_ANON_KEY'];
const missing=required.filter(name=>!process.env[name]?.trim());
if(missing.length){console.error(`Deployment blocked: configure ${missing.join(', ')} in GitHub repository secrets.`);process.exitCode=1;}
else {
  try {
    const url=new URL(process.env.VITE_INSFORGE_URL);
    if(url.protocol!=='https:'||url.username||url.password)throw new Error('Use an HTTPS backend URL without embedded credentials.');
    console.log('Deployment configuration is present. Use only the public anonymous key, never an administrator key.');
  } catch(error){console.error(`Deployment blocked: ${error.message}`);process.exitCode=1;}
}

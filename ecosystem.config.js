module.exports = {
  apps: [
    {
      name: 'tc-editor-backend',
      script: './start.sh',
      interpreter: '/bin/bash',
      cwd: '/home/ubuntu/TC-Editor-Backend/backend',
      env: {
        "FLASK_ENV": "production"
      }
    }
  ]
};
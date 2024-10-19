module.exports = {
  apps: [
    {
      name: 'tc-editor-backend',
      script: './start.sh',
      interpreter: 'none',
      cwd: '/home/ubuntu/TC-Editor-Backend/backend',
      env: {
        "FLASK_ENV": "production"
      }
    }
  ]
};
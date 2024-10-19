module.exports = {
    apps: [
      {
        name: 'tc-editor-backend',
        script: 'gunicorn',
        args: 'app:app --bind 0.0.0.0:8000 --workers 3',
        interpreter: 'none', // Tells PM2 not to use Node.js
        cwd: '/home/ubuntu/TC-Editor-Backend/backend',
        env: {
          // Environment variables
        }
      }
    ]
  };
  
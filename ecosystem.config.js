module.exports = {
    apps: [
      {
        name: 'tc-editor-backend',
        script: '/home/ubuntu/venv/bin/gunicorn',
        args: 'app:app --bind 0.0.0.0:8000 --workers 3',
        interpreter: 'none', // Tells PM2 not to use Node.js
        cwd: '/home/ubuntu/TC-Editor-Backend/backend',
        env: {
          "FLASK_ENV": "production"
        }
      }
    ]
  };
  
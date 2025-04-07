#!/bin/bash

cd /home/ubuntu/Project_AdvPythonGitLinux

echo "Pull des dernières données..."
git pull origin main

if [ $? -eq 0 ]; then
  echo "Données à jour. Relance du dashboard..."
  pkill -f "dashboard/app.py"
  source venv/bin/activate
  nohup python dashboard/app.py > dashboard.log 2>&1 &
else
  echo "Git pull a échoué."
fi

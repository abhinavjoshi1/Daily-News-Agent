#!/bin/bash
cd ~/crewai

# Move digest from news_agent/digests to root digests
mv ~/crewai/news_agent/digests/*.md ~/crewai/digests/ 2>/dev/null

# Push to GitHub
git add digests/
git commit -m "Digest $(date +%d_%m_%y)"
git push origin main

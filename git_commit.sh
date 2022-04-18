#!/usr/bin/bash

git add -A
echo

git status
echo

read -p "Enter commit message: " commit_message
echo

git commit -m \"$commit_message\"

echo "git pull"
echo ""
git push
echo

read -p "Continue to push commit? (^C to cancel)"
echo

git push
echo


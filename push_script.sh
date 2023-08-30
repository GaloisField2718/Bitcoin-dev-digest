#!/bin/bash

git pull;
git add .;
git commit -m "Daily updates";
git push > ./logs/out.txt 2> ./logs/err.txt;


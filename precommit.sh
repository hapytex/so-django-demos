#!/bin/bash

bash black.sh
sort requirements.txt > requirements2.txt
mv -f requirements2.txt requirements.txt
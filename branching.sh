#!/bin/bash

if [ "$#" -lt 1 ]; then
  echo "Specify a StackOverflow id"
  exit 1
fi

soid="$1"
git commit -am 'pre-branching'
git checkout -b "so/$soid"

curl "https://api.stackexchange.com/2.3/questions/$1?order=desc&sort=activity&site=stackoverflow&filter=!nNPvSNP4(R" | jq --raw-output '.items[0].body_markdown' - > question.md
git add question.md

echo -e "# [Question](https://stackoverflow.com/questions/$1/)\n\n" > README.md
cat question.md >> README.md
echo -e "# Answer\n\n" >> README.md

git add README.md


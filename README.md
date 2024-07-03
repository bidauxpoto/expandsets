This repo is part of the BIoinformatics and Data-Analysis POwer TOols collection: [BiDaUxPoTo](https://github.com/bidauxpoto)

Given a COLUMN with different entities separated by a specific string the program expands them into multiple rows. If more than 1 COLUMN is specified, the cartesian product of the two sets is returned.

# Installation
```
conda install -c molinerislab expandsets
```

# Usage
```
cat input.tsv | expandsets 1 > output.tsv
```

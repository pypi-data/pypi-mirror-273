# ghfc-utils

set of small tools designed to help automatize simple task locally or on Pasteur's cluster.

**ghfc-reannotate** for the postprocessing of slivar files including filtering and geneset reannotation.

## Installation

```
pip install git+https://{token_username}:{generated_token}@gitlab.pasteur.fr/ghfc/ghfc-utils.git
```

when on maestro:
```
module load Python/3.9.18
pip install --user git+https://maestro_tok_FC:rSUDdAJWZutsZTJseJ3V@gitlab.pasteur.fr/ghfc/ghfc-utils.git
```

## slivar reannotator

A tool to filter and reannotate slivar files according to various parameters and genesets. The goal is to produce a more generic kind of slivar files and to use this for the user to run their own filtering.

```
usage: ghfc-reannotate [-h] configuration slivar output

positional arguments:
  configuration         config file
  slivar                slivar file to reannotate
  output                annotated slivar file

optional arguments:
  -h, --help            show this help message and exit
  --chunksize CHUNKSIZE
                        size of the chunks read from the input (default 100000)
```

- This tools read the slivar file before decomposing the impacts by transcripts. 
- It then filters all line using, in this order following the config file parameters:
    1. the geneset (based on the ENSG, mind the GRCh37/GRCh38 differences in ENSG)
    2. the impact / impact-categories
    3. if missense are kept, filtering them on their impact (using scores such as the mpc or the cadd)
    4. the gnomad frequency
- the variant/transcript are then sorted according to criteria given by the user in the config file from the most important to the least important
- for each sample, variant and gene (ENSG) the first transcript (most important given the config criteria) is kept.

### yaml config file

This section is listing the accepted options in the config file, but example files are provided. 
- (optional) **geneset-file**: path to the file containing the list of ENSG for out geneset of interest
- **ordering-priority**: the list (ordered) of criteria to use to rank the importance of the transcripts to output
- **impact-categories-filter**: the impact categories to keep during the filtering. The categories are defined in this package in [impacts.yaml](ghfc_utils/resources/impacts.yaml).
- **impact-filter**: the impacts to keep during the filtering process. the name of the impacts are visible in [impacts.yaml](ghfc_utils/resources/impacts.yaml).
- (optional) **missense-filter**: this section will define how the missense variant are further filtered
    - first a subcategory is used for the score used, e.g. **mpc**, **cadd**
    - for each subcategory, 3 fields are expected:
        - **field**: the name of the slivar column containing the value
        - **min**: the minimal value to keep (included)
        - **max**: the maximal value to keep (excluded)
    - in addition to the subcategories, a **condition** field is expected to specify *how* the subcategories are used. Possible values are:
        - cadd_if_no_mpc: use the mpc and when not available (-1) uses the cadd
        - cadd_and_mpc
        - cadd_or_mpc
        - mpc_only
        - cadd_only
- (optional) **gnomad-filter**: to filter further on an included gnomAD column. 3 fields are expected here:
    - **field**: the name of the slivar column containing the gnomad value to filter on
    - **min**: the minimal value to keep (included)
    - **max**: the maximal value to keep (included)
- (optional) **pext-filter**: to annotate each transcript and filter them using a pext file:
    - **file**: path to the pext file to use
    - **field**: nme of the outputed column
    - **min**: the minimal value to keep (included). can put -1 to annotate and not filter on it.

Finally, some more global slivar parameters that are not likely to change a lot:
- **slivar-field-name**: the name of the slivar column that contains the list of all vep impacts per transcripts
- **slivar-field-decomposed**: the list of each field when they are decomposed. some of those fields are expected with the following names:
    - *impact*
    - *ENSG*
    - *canonical*: the vep columns containing "YES" for the canonical transcripts
    - *loftee*: the loftee "LoF" column


### pext file

The pext is a bed file with the following columns (order important, there must be some header):
```
chr	start	end	max_brain	ensg	symbol
```
Need to have the genome version to match the data (GRCh37/38 and using the chr or not in the chromosome names)


### TODO
- offer to prefix geneset columns?
- offer to keep some of the original columns (impact/transcript)
- possibility to run on stdin / stdout?
- refining DP and AB
- needs for automated submission on the cluster? (means user has permission to use it)
- possibility to automate splitting in chunks and merging back?

## slivar *de novo* ML

Moving the machine learning validator for *de novo* variants to this tool.

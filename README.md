# American Society of Hematology Annual Meeting abstract database and analysis

This repository contains code for scraping the ASH annual meeting abstracts, 
from the first date they were online (2004) to the present, and an initial analysis of this data.

It was inspired by an abstract describing the initial [work](https://doi.org/10.1182/blood-2019-130053) by Andrés Gómez-De León, MD *et al*.

Their work was [published](https://pubmed.ncbi.nlm.nih.gov/?term=33909458) in manuscript form in JCO Global Oncology in 2021.
Dr. Gómez-De León and his team manually examined 4871 abstracts from the 2018 Annual Meeting. 

The main unique contribution of the present work is to include 
all abstracts from all meetings whose abstracts are available on the ASH website,
and provide a pipeline for maintaining an up-to-date database going forward.

An additional hope is to make automated analysis available as a free service to other researchers,
BYOD (Bring Your Own Data).

## Acknowledgements

Dr. Gómez-De León: Thank you for your generosity in sharing ideas and excitement!

I am also indebted to [Simon Willison](https://simonwillison.net/) for [inspiration](https://youtu.be/Lig2gxPEZPo), [examples](https://datasette.io/examples), and [beautiful](https://github.com/simonw/datasette) [software](https://github.com/simonw/sqlite-utils). 

Much thanks also to [Deta](https://www.deta.sh/) for providing database hosting, and to [GitHub](https://github.com/) for automation and data storage. I use Deta's [Base](https://docs.deta.sh/docs/base/about/) service as a data exchange, [GitHub Actions](https://github.com/features/actions) for automation, and [this GitHub repository ](https://github.com/cbeauhilton/ash-db) for more durable data storage.

# American Society of Hematology Annual Meeting abstract database and analysis

![2021-09-12-102956_1920x1080_scrot](https://user-images.githubusercontent.com/34774299/132993443-3584de79-69e5-434c-ab5e-bfcc4c43e260.png)

A small sample of abstracts with the topic "leukemia." The [real website](https://ash-abstracts.vercel.app/abstracts/abstracts) is interactive.

---

This repository contains code for scraping the ASH annual meeting abstracts, 
from the first date they were online (2004) to the present, and an initial analysis of this data.

An interactive map of some of the data is available 
[here](https://ash-abstracts.vercel.app/abstracts/abstracts). 
Since there are a large number of examples the map may not load quickly.
Consider instead exploring a facet of the data, 
such as [this one](https://ash-abstracts.vercel.app/abstracts/abstracts?_facet_array=topics&topics__arraycontains=leukemia) (screenshot above) for abstracts tagged with "leukemia" (scroll down that page to see the map).

It was inspired by an abstract describing the initial [work](https://doi.org/10.1182/blood-2019-130053) 
by Andrés Gómez-De León, MD *et al*. 
Their work was [published](https://pubmed.ncbi.nlm.nih.gov/?term=33909458)
in manuscript form in JCO Global Oncology in 2021.
Dr. Gómez-De León and his team manually examined 4871 abstracts from the 2018 Annual Meeting. 

The main unique contribution of the present work is to include 
all abstracts from all meetings whose abstracts are available on the ASH website,
and provide a pipeline for maintaining an up-to-date database going forward.

An additional hope is to make automated analysis available 
as a free service to other researchers,
BYOD (Bring Your Own Data).

## Contributing

I am happy to accept contributions and criticism.

[Email me](http://www.beauhilton.com/contact.html),
or, better yet,
open an issue by creating a [free GitHub account](https://github.com/join) 
and clicking on the ["Issues" tab](https://github.com/cbeauhilton/ash-abstracts/issues) above.
I keep a running conversation with myself and task list there as well, 
feel free to jump in.

## Acknowledgements

Dr. Gómez-De León: Thank you for your generosity in sharing ideas and excitement!

I am indebted to [Simon Willison](https://simonwillison.net/) 
for [inspiration](https://youtu.be/Lig2gxPEZPo), 
 [examples](https://datasette.io/examples),
 and [beautiful](https://github.com/simonw/datasette) 
 [software](https://github.com/simonw/sqlite-utils). 

Much thanks [Vercel](https://ash-abstracts.vercel.app/base/abstracts_base) 
for easy application deployment 
and [GitHub](https://github.com/) for automation and data storage. 
I use [Vercel](https://vercel.com/) for data exploration, showing maps, and as a personal API, 
[GitHub Actions](https://github.com/features/actions) for automation,
and [this GitHub repository ](https://github.com/cbeauhilton/ash-files) to store flat files (JSON).

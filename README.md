# dataset-pescaria

## formatted/
|arquivo|descrição|origem|
|:-:|:-:|:-:|
|[brasilia.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/brasilia.csv.tar.bz2?ref_type=heads)|urls de phishing relacionadas a fraudes bancárias|grégio|
|[common-crawl.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/common-crawl.csv.tar.bz2?ref_type=heads)|extraído do [Common Crawl](https://commoncrawl.org/) e filtrado com o [Google Safe Browsing](https://developers.google.com/safe-browsing)|https://commoncrawl.org/|
|[dmoz.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/dmoz.csv.tar.bz2?ref_type=heads)|urls legítimas extraídas do [DMOZ](dmoz.org) (Open Directory Project)|[HOEK, Lisa. Web classification using DMOZ. Radboud University, 2021](https://www.cs.ru.nl/bachelors-theses/2021/Lisa_Hoek___1009553___Web_classification_using_DMOZ.pdf)|
|[misp.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/misp.csv.tar.bz2?ref_type=heads)|urls de phishing submetidas no [MISP Threat Sharing](https://misp.c3sl.ufpr.br/users/login) do C3SL|[C3SL MISP Threat Sharing](https://misp.c3sl.ufpr.br/users/login)|

|arquivo|legítimo|unlabeled|phishing|idioma|período|
|:-:|:-:|:-:|:-:|:-:|:-:|
|[brasilia.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/brasilia.csv.tar.bz2?ref_type=heads)|-|-|259632|br|2013-2021|
|[common-crawl.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/common-crawl.csv.tar.bz2?ref_type=heads)|-|49806485|7695|br|2013-2025|
|[dmoz.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/dmoz.csv.tar.bz2?ref_type=heads)|3573026|-|-|en|1998-2017|
|[misp.csv.tar.bz2](https://gitlab.c3sl.ufpr.br/phfr24/dataset-pescaria/-/blob/master/misp.csv.tar.bz2?ref_type=heads)|-|-|1269926|br|2013-2025|
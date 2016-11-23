dbpedia-data
-----
Contains all the code to build the starting points of our project. A visualization of the process and the needed / generated files can be found in the dataPipeline.pdf. The link-data is currently ignored and only the person-data is build.

- **data_raw:** Should contain the raw DBpedia data sets and the dataset JProf. Dr. Wagner provided. Only includes small lists used for profession/nationality matching etc. The other datasets need to be downloaded manually.
  - DBpedia sets that are necessary:
   - instance_types_transitive_en.ttl (~4.25 GB)
   - mappingbased_literals_en.ttl (~2.02 GB)
   - mappingbased_objects_en.ttl (~2.34 GB)
   - genders_en.ttl (~416 KB)
   - wikipedia_links_en.ttl (~6.14 GB)
   - article_categories_en.ttl (~3.21 GB)
  - JProf. Dr. Wagner's dataset needs to be named: person_data_claudia.csv
  

- **data_extracted:** Will contain all the interim results (should be **empty** in the git-repo)
- **final_datasets:** Contains the compressed extracted data sets. (~17.6 MB, uncompressed: ~120 MB)

Currently **build_everything.py** builds the 5 desired datasets. The properties that are used in the data sets can be changed in the **prop_selection.txt**.


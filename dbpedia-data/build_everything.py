from write_personlist_by_type import write_personlist_by_type
from write_inflit_cont_person import write_inflit_cont_person
from write_infobj_cont_person import write_infobj_cont_person
from write_infobj_needing_lookup import write_infobj_needing_lookup
from write_inflit_cont_infobj import write_inflit_cont_infobj
from normalize_infobj_to_inflits import normalize_infobj_to_inflits
from join_inflits import join_inflits
from preselect_properties import preselect_properties
from build_person_dataset import build_person_dataset
#from write_links_cont_person import write_links_cont_person
from write_gender_cont_person import write_gender_cont_person
from write_cat_cont_person import write_cat_cont_person
#from write_type_cont_person import write_type_cont_person
from write_wikilinks_cont_person import write_wikilinks_cont_person
from improve_person_dataset_cat import improve_person_dataset_cat
from improve_person_dataset_claudia import improve_person_dataset_claudia
from build_profession_datasets import build_profession_datasets

print('Finished Importing!')

print('-------------------------------------------')
print('Executing: write_personlist_by_type')
write_personlist_by_type()

print('-------------------------------------------')
print('Executing: write_inflit_cont_person')
write_inflit_cont_person()

print('-------------------------------------------')
print('Executing: write_cat_cont_person')
write_cat_cont_person()

print('-------------------------------------------')
print('Executing: write_infobj_cont_person')
write_infobj_cont_person()

print('-------------------------------------------')
print('Executing: write_infobj_needing_lookup')
write_infobj_needing_lookup()

print('-------------------------------------------')
print('Executing: write_inflit_cont_infobj')
write_inflit_cont_infobj()

print('-------------------------------------------')
print('Executing: normalize_infobj_to_inflits')
normalize_infobj_to_inflits()

print('-------------------------------------------')
print('Executing: join_inflits')
join_inflits()

print('-------------------------------------------')
print('Executing: preselect_properties')
preselect_properties()

print('-------------------------------------------')
print('Executing: write_gender_cont_person')
write_gender_cont_person()

print('-------------------------------------------')
print('Executing: write_wikilinks_cont_person')
write_wikilinks_cont_person()

print('-------------------------------------------')
print('Executing: build_person_dataset')
build_person_dataset()

print('-------------------------------------------')
print('Executing: improve_person_dataset_cat')
improve_person_dataset_cat()

print('-------------------------------------------')
print('Executing: improve_person_dataset_claudia')
improve_person_dataset_claudia()

print('-------------------------------------------')
print('Executing: build_profession_datasets')
build_profession_datasets()
# asw

This is a space to keep track of particular projects and work that I have undertaken whilst on placement at AS Watson (ASW). 

## academies

The academies and `intro_to_git.md` were co-created or refreshed by the other [intern](https://github.com/q1any1tan) and myself to help new interns learn the ropes. If any mistakes are spotted please feel free to update them accordingly.

## showcases

The showcases are examples of work that I created during my year at ASW. Any credentials or details have been changed for security reasons, but the rest of the code remains unchanged.

### high-skincare-model

This was a model that I created to help one of the Business Units (BUs) target the Skincare category more effectively with communications by attempting to identify members who had purchased "low" amounts in the category that were more likely to spend more in the future based on transactional data. It would flag these potential members and upload them to our database, for the local BU to access and use their expertise in CRM to target these members and hopefully convert more sales than a traditional category-wide communication. 

The model would predict on all the members in the category once a month, on a rolling 12-month basis, so members could drop in and out of being a high skincare member. Every year or so the model will be checked with a confusion matrix and some other key metrics and retrained if necessary.


### lifestyle-model

This was a group of models all working in conjunction to put the many different countries of a BU into a cohesive segmentation. Initially, the largest BU had a segmentation which was a clustering-based algorithm that they were pleased with, and wanted similar segments across all the other countries too. However, this was difficult to achieve as each country has different profiles of shoppers, so if we applied another clustering algorithm we wouldn't necessary end up with the same segments. 

Therefore, we decided to implement a regression algorithm that was trained on the segments of the original BU and would predict on each of the remaining BUs. We had to tweak this technique depending on the profile of shoppers for each BU, so we ended up with 3 slightly different regression models to cover all the options, so with the original clustering algorithm there are 4 separate models in use for this segmentation, covering millions of members.

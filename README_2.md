# Adding a new SNOMED CT Value Set

A "Value Set", in SNOMED CT parlance is currently defined as a 446609009 | Simple type reference set |, which "allows a set of components to be specified for inclusion or exclusion for a specified purpose. This type of reference set represents an "extensional definition" of a subset of SNOMED CT components. Thus it can be used to fully enumerate a subset of concepts, descriptions or relationships." More information on simple reference sets can be found in the [SNOMED CT Technical Implementation Guide](http://ihtsdo.org/fileadmin/user_upload/doc/download/doc_TechnicalImplementationGuide_Current-en-US_INT_20150131.pdf?ok) in section **5.6.2.3 Simple Reference Set**

The first step in creating a new value set is to identify the value set itself.  This involves the following steps:

1. Create a new concept identifier
2. Create at least two descriptions:
  1. A Fully Specified Name
  2. A Synonym
3. (optional) Create a definition
3. Add a relationship entry that states that the concept is a reference set
4. Add at least two language entries that identify the newly created synonym as the Preferred name in US and GB English

As an example,  to create the CIMI Link Meaning Refset, one would add the following entries:


#### RF2 Concept Table
| id | effectiveTime | active | moduleId | definitionStatusId |
| --- | --- | --- | --- | --- |
| 21000160106 | 20150131 | 1 | 11000160102 | 900000000000074008 |

The entry above declares that concept id **21000160106** is:

1. Active
2. Owned by the CIMI Module
3. Has a definition status of [900000000000074008 | Primitive](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000074008?bypass=1)

#### RF2 Description Table
| id | effectiveTime | active | moduleId | conceptId | languageCode | typeId | term | caseSignificanceId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31000160112 | 20150131 | 1 | 11000160102 | 21000160106 | en | 900000000000013009 | CIMI Link Meaning Refset | 900000000000020002 |
| 41000160117 | 20150131 | 1 | 11000160102 | 21000160106 | en | 900000000000003001 | CIMI Link Meaning Refset (foundation metadata concept) | 900000000000020002 |
| 51000160119 | 20150131 | 1 | 11000160102 | 21000160106 | en | 900000000000550004 | A subset of concepts that describe the meaning of a link. | 900000000000020002 |

The entries above define three identifiers for **21000160106**, both owned by the CIMI Module and both active.  Note that the description identifiers are also assigned from the CIMI namespace

1. 31000160112 -- "CIMI Link Meaning Refset (foundation metadata concept)", the [FSN](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000003001?bypass=1) for the concept
2. 41000160117 -- "CIMI Link Meaning Refset", a [Synonym](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000013009?bypass=1) for the concept.  The Language Refset (described below) determines which synonyms are preferred in which languages
3. 51000160119 -- "A subset of concepts ...", a *[Definition](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000550004?bypass=1)* (textual description) of the concept.

####  RF2 Stated Relationship Table
| id | effectiveTime | active | moduleId | sourceId | destinationId | relationshipGroup | typeId | characteristicTypeId | modifierId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 21000160123 | 20150131 | 1 | 11000160102 | 21000160106 | 446609009 | 0 | 116680003 | 900000000000010007 | 900000000000451002 |


The Stated Relationship Table entry declares that Concept **21000160106** [is a](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/116680003?bypass=1) [Simple type reference set](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/446609009?bypass=1).

#### RF2 Language Refset
| id | effectiveTime | active | moduleId | refsetId | referencedComponentId | acceptabilityId | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 301736bc-c7d2-4585-8f09-65ca76e983df | 20150131 | 1 | 11000160102 | 900000000000509007 | 31000160112 | 900000000000548007 |
| 750bd314-6585-4bb5-989a-dacccc99147e | 20150131 | 1 | 11000160102 | 900000000000508004 | 31000160112 | 900000000000548007 |

The two entries above describe the **31000160112** entry in the RF2 Description Table is the [Preferred Name](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000548007?bypass=1) in both the [US English](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000509007?bypass=1) and the [Great Britain English](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000508004?bypass=1) languages.


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

The simplest way to create the reference set is to execute the following command in the RF2RestClient directory:

`> python concept -u http://localhost:8081/rf2/ -n "CIMI Link Meaning Refset" -d "A subset of concepts that describe the meaning of a link." -p srs -e 20150131`
`    Concept 31000160108 successfully created`
`    Changeset: b65416ae-89e1-4033-893c-a89d5fe17932 committed`

The above command would add the following entries (note that we aren't showing the changeset and locked columns for simplicity)(note also that if no changeset is supplied, the `concept` function creates and commits a temporary changeset)

#### RF2 Concept Table
| id | effectiveTime | active | moduleId | definitionStatusId |
| --- | --- | --- | --- | --- |
| 31000160108 | 20150131 | 1 | 11000160102 | 900000000000074008 |

The entry above declares that concept id **31000160108** is:

1. Active
2. Owned by the CIMI Module
3. Has a definition status of [900000000000074008 | Primitive](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000074008?bypass=1)

#### RF2 Description Table
| id | effectiveTime | active | moduleId | conceptId | languageCode | typeId | term | caseSignificanceId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 31000160112 | 20150131 | 1 | 11000160102 | 31000160108 | en | 900000000000013009 | CIMI Link Meaning Refset | 900000000000020002 |
| 41000160117 | 20150131 | 1 | 11000160102 | 31000160108 | en | 900000000000003001 | CIMI Link Meaning Refset (foundation metadata concept) | 900000000000020002 |
| 51000160119 | 20150131 | 1 | 11000160102 | 31000160108 | en | 900000000000550004 | A subset of concepts that describe the meaning of a link. | 900000000000020002 |

The entries above define three identifiers for **31000160108**, both owned by the CIMI Module and both active.  Note that the description identifiers are also assigned from the CIMI namespace

1. 31000160112 -- "CIMI Link Meaning Refset (foundation metadata concept)", the [FSN](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000003001?bypass=1) for the concept
2. 41000160117 -- "CIMI Link Meaning Refset", a [Synonym](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000013009?bypass=1) for the concept.  The Language Refset (described below) determines which synonyms are preferred in which languages
3. 51000160119 -- "A subset of concepts ...", a *[Definition](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000550004?bypass=1)* (textual description) of the concept.

####  RF2 Stated Relationship Table
| id | effectiveTime | active | moduleId | sourceId | destinationId | relationshipGroup | typeId | characteristicTypeId | modifierId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 21000160123 | 20150131 | 1 | 11000160102 | 31000160108 | 446609009 | 0 | 116680003 | 900000000000010007 | 900000000000451002 |


The Stated Relationship Table entry declares that Concept **31000160108** [is a](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/116680003?bypass=1) [Simple type reference set](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/446609009?bypass=1).

#### RF2 Language Refset
| id | effectiveTime | active | moduleId | refsetId | referencedComponentId | acceptabilityId | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 301736bc-c7d2-4585-8f09-65ca76e983df | 20150131 | 1 | 11000160102 | 900000000000509007 | 41000160117 | 900000000000548007 |
| 750bd314-6585-4bb5-989a-dacccc99147e | 20150131 | 1 | 11000160102 | 900000000000508004 | 41000160117 | 900000000000548007 |

The two entries above describe the **41000160117** entry in the RF2 Description Table is the [Preferred Name](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000548007?bypass=1) in both the [US English](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000509007?bypass=1) and the [Great Britain English](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000508004?bypass=1) languages.


# Adding  concepts to a SNOMED CT Value Set
We will use the CIMI Null Flavour Refset as an example, as it has both existing concepts and new ones. Starting with tab 4 - Null Flavour Refset, we:

1. Create a new changeset (details on this can be found at...):
	   *  `python changeset a -u http://localhost:8081/rf2 -n "NullFlavors" -d "Adding null flavor refset" -o CIMI -e 20150131`
	   *  `New changeset created: fb8f4221-968f-4309-be92-cf3c166a0895 (NullFlavors)`
2. Add the new concepts as needed, using the change set identifier returned above
	* `python concept -u http://localhost:8081/rf2 -n "no information" -p 410514004 -e 20150131 -c NullFlavors`
	*  `Concept 41000160101 successfully created`
	* `python concept -u http://localhost:8081/rf2 -n "masked" -p 410514004 -e 20150131 -c NullFlavors`
	*  `Concept 51000160103 successfully created`
3. Create the target refset:
	* `python concept -u http://localhost:8081/rf2 -n "CIMI Null Flavour Refset" -p srs -e 20150131 -c NullFlavors -d "A subset of concepts that indicate the reason that data is missing."`
	* `Concept 61000160100 successfully created`
4. Add the set of concepts to the Value Set:
	* `python simplerefset a  -u http://localhost:8081/rf2 -r 61000160100 -cs NullFlavors -c 41000160101 51000160103 261665006 385432009 -e 20150131`
	* `Concept(s) added to refset
5. Commit the resulting change set:
      * `python changeset c -u http://localhost:8081/rf2 -n NullFlavors`
	* `Change set successfully committed`

# Dumping a Collection of Changes
Change sets can be exported to RF2 format files:
*  `python changeset d -u http://localhost:8081/rf2 -n NullFlavors --target NF`
*  `Changeset caff122a-4402-4a63-8a24-2853cb701d8a saved in NullFlavors.zip`

The NullFlavors.zip file contains the following directories:

* NF
    * RF2Release
        * Snapshot
            * Refset
                *  Language
                    * der2_cRefsetLanguageSnapshot_INT_20150824.txt  -- RF2 Language Refset
                * Metadata
                    * der2_sssiiRefset_ChangesetSnapshot_INT_20150824.txt - RF2 Changeset Refset (Mayo extension)
             * Terminology
                    * sct2_Concept_Snapshot_INT_20150824.txt -- Concept File
                    * sct2_Description_Snapshot_INT_20150824.txt -- Description File
                    * sct2_Relationship_Snapshot_INT_20150824.txt -- Relationship File
                    * sct2_StatedRelationship_Snapshot_INT_20150824.txt -- Stated Relationship File

                    
Note that the above files are different from the standard RF2 release:

1. `der2_sssiiRefset_ChangesetSnapshot_INT`` does not exist in the standard RF2 Release
2. All of the exported files have two additional columns:
     * `changeset`  -- the uuid of the changeset that created the row in the file
     * `locked`  -- "1" means that the changeset has not been commited. 
3. The Language Refset has an additional column, `conceptId`, which provides a direct link to the associated concept.

If necessary, it would be a relatively straight-forward task to add a parameter to the dump program to remove the additional identifiers... we just haven't had a need to do it as of yet.



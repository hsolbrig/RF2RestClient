SNOMED CT Value Sets
===================


## Modules and Namespaces

Every SNOMED CT Extension is assigned a *namespace*.  A complete list of namespaces can be found [here](http://www.ihtsdo.org/resource/resource/200).

The CIMI Namespace is **1000160**.

## Concept Identifier Format
Each namespace references a set of 10,000,000 possible SNOMED CT identifiers, whose format is:
**iiiiiiii nnnnnn pp c**

where:
|   ID        |      Description                | Digits   |
| --------: |  ---                 | :------: |
|  c        | Verhoeff check digit |    1     |
|  pp       | Partition identifier |    2     |
|  nnnnnn   | Namespace identifier |    7     |
|  iiiiiiii | Concept identifier   |  1-9     |

### SNOMED CT Partition Identifiers
"Short Format" identifies SCT identifiers in the primary SNOMED Namespace -- those with no namespace identifier.  "Long Format" is the format that we are using
| PartitionId | Description |
| ----------- | ----------- |
|  00         | A Short Format Concept   |
|  01         | A Short Format Description |
|  02         | A Short Format Relationship |
|  10         | A Long Format Concept |
|  11         | A Long Format Description |
|  12         | A Long Format Relationsip |

More details on identifiers can be found in the [SNOMED CT Technical Implementation Guide](http://ihtsdo.org/fileadmin/user_upload/doc/download/doc_TechnicalImplementationGuide_Current-en-US_INT_20150131.pdf) starting at p87 - 4.3.2.2 SCTID Representation.

### Module Identifiers

A SNOMED CT module scopes the ownership / assignment of SNOMED CT identifiers.  Once assigned, identifiers remain constant, no matter whether they are managed/owned by the CIMI organization, the SNOMED CT US Extension or SNOMED CT International.  As ownership is transferred, however, the module identifier within the various files is updated.


The CIMI Module identifier is **11000160102 | CIMIModule (core metadata concept)**.  It is defined using the following entries:

#### RF2 Concept Table
| id | effectiveTime | active | moduleId | definitionStatusId |
| --- | --- | --- | --- | --- |
| 11000160102 | 20150107 | 1 | 11000160102 | 900000000000074008 |

The entry above declares that concept id **11000160102** is:

1. Active
2. Owned by the CIMI Module
3. Has a definition status of [900000000000074008 | Primitive](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000074008?bypass=1)

#### RF2 Description Table
| id | effectiveTime | active | moduleId | conceptId | languageCode | typeId | term | caseSignificanceId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11000160118 | 20150107 | 1 | 11000160102 | 11000160102 | en | 900000000000003001 | CIMIModule (core metadata concept) | 900000000000448009 | 
| 21000160110 | 20150107 | 1 | 11000160102 | 11000160102 | en | 900000000000013009 | CIMIModule | 900000000000448009 | 

The entries above define two identifiers for **11000160102**, both owned *by* the CIMI Module and both active.  Note that the description identifiers are also assigned from the CIMI namespace

1. 11000160118 -- "CIMIModule (core metadata concept", the [FSN](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000003001?bypass=1) for the concept
2. 21000160110 -- "CIMIModule", a [Synonym](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000013009?bypass=1) for the concept.  The Language Refset (described below) determines which synonyms are preferred in which languages

####  RF2 Stated Relationship Table
| id | effectiveTime | active | moduleId | sourceId | destinationId | relationshipGroup | typeId | characteristicTypeId | modifierId |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11000160125 | 20150107 | 1 | 11000160102 | 11000160102 | 900000000000443000 | 0 | 116680003 | 900000000000010007 | 900000000000451002 | 


The Stated Relationship Table entry declares that Concept **11000160102** [is a](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/116680003?bypass=1) [Module](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000443000?bypass=1) and, as with the other entries, this declaration is owned by the CIMI Module.

#### RF2 Language Refset
| id | effectiveTime | active | moduleId | refsetId | referencedComponentId | acceptabilityId | 
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 58ffd1a5-1f3b-4e61-ae17-e84ebeb8bbe4 | 20150107 | 1 | 11000160102 | 900000000000508004 | 21000160110 | 900000000000548007 |
| b5666608-94bb-4645-bfee-ba48f02a4f95 | 20150107 | 1 | 11000160102 | 900000000000509007 | 21000160110 | 900000000000548007 |

The two entries above describe the **21000160110** entry in the RF2 Description Table is the [Preferred Name](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000548007?bypass=1) in both the [US English](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000509007?bypass=1) and the [Great Britain English](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000508004?bypass=1) languages.

#### RF2 Module Dependency Refset
| id | effectiveTime | active | moduleId | refsetId | referencedComponentId | sourceEffectiveTime | targetEffectiveTime |
| --- | --- | --- | --- | --- | --- | --- | --- | 
| 71747124-42a6-4dad-afe3-164a25bdcca8 | 20150107 | 1 | 11000160102 | 900000000000534007 | 900000000000012004 | 20150107 | 20150131 | 
| c3bdfd68-796b-472a-ab88-1edb213a1a52 | 20150107 | 1 | 11000160102 | 900000000000534007 | 900000000000207008 | 20150107 | 20150131 | 

The entries above declare that the CIMI Module has two dependencies in the [Module Dependency Refset](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000534007?bypass=1):

1. [The SNOMED CT Model Component Module](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000012004?bypass=1) (The Metadata Module)
2. [The SNOMED CT Core Module](http://informatics.mayo.edu/py4cts2/codesystem/SNOMED_CT/version/20150131/entity/900000000000207008?bypass=1) (The SNOMED CT International Core concepts)






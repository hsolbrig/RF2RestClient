# RF2 Changeset Extension

The RF2 tables are normalized and it takes several atomic transactions to enter a new concept, connect a concept with a value set, etc.  Changes actually occur in larger blocks -- sets of concepts must be entered, moved, added to value sets, etc. and the changes should not be made visible for outside use until they have been completed and reviewed.

The *changeset* extension is designed to accommodate this set of requirements.  The general work flow is:

1.  Create a new changeset.  A changeset may be assigned a unique name, an owner, an effective time and/or a description of the goal and purpose of the changeset.  Every changeset is assigned a unique UUID that serves as its primary identity within the database.
2.  Make one or more  of changes to the RF2 data. Add, update or inactivate concepts, descriptions, relationship entries, value set members, etc.  Each of these changes must be accompanied by a changeset name or UUID and none of these changes will be visible *unless* the identifier is included as a parameter in the data retrieval calls.
3.  Commit the changeset. This finalizes the set of changes and makes them visible to the outside world.  Once committed, a changeset and its members cannot be changed without creating a new, open change set.

The scope of a change set can be as simple as having a single change, such as a change in the wording of a concept description or can potentially include a whole terminology branch that may consist of many hundreds or even thousands of transactions.

## RF2 Changeset Refset

The Changeset extension requires one additional reference set table: `der2_sssiiRefset_Changeset`.  This table has the following columns

| Column | Data Type | Description |
| ---- | --- | --- |
| id | UUID | The unique entry number in the refset table |
| effectiveTime | Date | The date / release where this entry became effective |
| active | Boolean | The state (active/inactive) as of effectiveTime |
| moduleId | SCTID | The module that contains / owns this entry |
| refsetId | SCTID | The name of the reference set to which this entry belongs (Fixed value: 21000160106 \| Changeset reference set) \| |
| referencedComponentId | UUID | The UUID of the changeset  |
| name | String | The unique name of the changeset within the context of the changeset file |
| owner | String | The name of the organization that owns the changeset or "None" if not supplied |
| changeDescription | String | A textual description of the purpose of the changeset or "None" if not supplied |
| isFinal | Boolean | `0` means that the change set is still open, `1` means it has been committed |
| inRelease | Date | The identifier of the release in which this change set was published or "None".  |
| changeset | UUID | The change set that this change belongs to.  Must be the same as `referencedComponentId` |
| locked | Boolean | `1` means that the change set is still open, `0` means that it has been committed.  Must be `1` if and only if `isFinal` is `0` |

Notes:
1. The original version of the RF2 specification allowed either an `SCTID` or an `UUID` in the `referencedComponentId` position in a reference set.  Technically, the current version does not allow the `UUID` option.  We ignore this restriction for the time being.
2. The `owner` attribute may reference an entry in an external table at some future point.  For the moment we use "CIMI" to represent the CIMI organization
3. `inRelease` has not been implemented yet.

## Changesets and existing tables
The ChangeSet extension adds the following two columns to *all* existing RF2 tables:

| Column | Data Type | Description |
| --- | --- | --- |
| changeset | UUID | The change set that this entry in the table belongs to, if any.  If this entry does not belong to a change set, this column and the `locked` columns are omitted or Null
| locked | Boolean | `1` means that this row in the table is not visible unless the accessor supplies `changeset`.  `0` (or absent) means that the row is visible to everyone

An open changeset (`isFinal` = `0`) may either be committed or rolled back.  If the changeset is committed, all of the RF2 entries having that changeset identifier must have the `locked` field changed from `1` to `0`.  In addition, the `isFinal` field in the changeset itself is changed to `1`.

If the changeset is rolled back, *all* RF2 entries associated with that change set are removed from the tables / database.  Rolling back a change set restores the tables to the state they were in prior to the changset creation.

Note that, while a change set is open any database operation is permitted and it is not required that history be maintained.  As an example, suppose that a new synonym were added to the RF2 Description File.  If it was subsequently discovered that the synonym was misspelled, as long as the change set was not yet final, the correction could either be made to the existing entry or the existing entry could be made inactive and a new entry (with a later date) could be added with the correct spelling.  Similarly, if it was discovered that the synonym was not actually needed, the record could:
* have its existing `active` column changed to `0`
* have a *new* row added with a later effectiveTime and the active flag set to 0
* be completely removed.
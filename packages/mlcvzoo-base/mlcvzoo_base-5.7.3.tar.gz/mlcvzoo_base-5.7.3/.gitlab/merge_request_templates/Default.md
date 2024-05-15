## Related issues

<!-- Issues that are closed by or related to this merge request, e.g. "Closes XXX" or "Related to XXX" -->

...

## Acceptance criteria

<!-- Criteria for the MR to be considered mergeable -->

- [ ] Implemented code changes don't diverge from the related issue.
- [ ] Implemented code changes fit to dependency tree of mlcvzoo projects
- [ ] Documentation (arc42) reflects the status quo after merge.
- Version number is incremented according to [SemVer](https://semver.org/) (Snapshot versions are not merged/released.). Update in
  - [ ] mlcvzoo_\*/pyproject.toml
  - [ ] mlcvzoo_\*/mlcvzoo_\*/\_\_init\_\_.py
  - [ ] mlcvzoo_\*/CHANGELOG.md
  - [ ] CHANGELOG.md
- Only released versions of dependencies are used (i.e. no snapshot versions).
      Use the script scripts/gitlab/generate_third_party_license_file.sh to generate the
      versions locally.
  - [ ] Runtime dependencies are stated in third-party-licenses.csv
  - [ ] Complementary file is correct
- [ ] The changelog contains entries reflecting all changes of this MR (and their reasons).

## Proposed squash commit message

<!--
A proposed message for the eventual squashed commit.
Please stick to the following pattern:

- A short one-line summary (max. 50 characters).
- A blank line.
- A detailed explanation of the changes introduced by this merge request.
  Each line should not exceed 72 characters.
*********1*********2*********3*********4*********5*********6*********7** (<-- Ruler for line width assistance)
-->
```
CHANGE ME!

A short one-line summary (max. 50 characters)

* A more detailed explanation of the changes introduced by this merge
  request.
* Each line should not exceed 72 characters.

Co-authored-by: NAME <EMAIL>

```
<!--
*********1*********2*********3*********4*********5*********6*********7** (<-- Ruler for line width assistance)
-->

Release checklist
=================
1. Run tests
2. Update version in pyproject.toml
3. Update version in CHANGELOG
4. Run build CI
5. Create a git Release+tag (both title and tag are vA.B.C, description is CHANGELOG content)
6. Run `rm -rf dist && mkdir dist && find . -type d -name '*.egg-info' -exec rm -r {} +`
7. Run `python3 -m build` (build both source and wheel distributions)
8. Run `twine check dist/*`
9. Run `twine upload dist/*` (push the package to PyPI)

CHANGELOG types of changes
==========================
`Added`      for new features.
`Changed`    for changes in existing functionality.
`Deprecated` for soon-to-be removed features.
`Removed`    for now removed features.
`Fixed`      for any bug fixes.
`Security`   for vulnerabilities.

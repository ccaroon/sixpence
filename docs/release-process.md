# Release Process

1. Create Release Branch
   - `git checkout master`
   - `git up origin`
   - `git checkout -b release/M.N`
   - Update `CHANGELOG.md`
   - Update `src/app/version.py`
   - Update `pyproject.toml` -> `build_number`
   - `git commit -a`
   - `git push origin release/M.N`
2. Build App
   - `inv check.clean check.unit-tests`
   - `inv app.build-clean`
   - `inv app.build`
3. Test
   - `inv app.run`
   - Manually test
4. Tag The Version
   - `git tag -a vM.N.P`
   - `git push origin --tags`
5. Install
   - `inv app.install`
6. Package
   - ...TODO...
7. Prep for Next Release
   - `git checkout master`
   - `git merge release/M.N`
   - Review changes
   - Update `code-names.md`
   - Stub in new `CHANGELOG.md` entry
      - "## vM.N.P - CODE-NAME (MMM DD, YYYY)"
   - Update `version.py` -> `VERSION` and `CODE_NAME` (Use DEV format)
   - Update `pyproject.toml` -> `build_number`
   - `git commit -a`
   - `git push origin master`

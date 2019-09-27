# Release Process

1. Update CHANGELOG.MD entry
   - Version
   - Release Date
   - Entry Contents
2. `git commit -a`
3. GitHub: Create PR from working branch --> `master`
4. GitHub: Merge PR to `master`
5. `git checkout master`
6. `git up origin`
7.  `npm version <patch|minor|fullVersion>` (As appropriate)
8.  `git push origin master`
9.  `git push --tags`

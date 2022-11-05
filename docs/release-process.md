# Release Process

0. In working branch
1. Update CHANGELOG.MD entry
   - Version
   - Release Date
   - Entry Contents
2. `git commit -a`
3. Squash commits, if desired.
4. GitHub: Create PR from working branch --> `master`
5. GitHub: Merge PR to `master`
6. `git checkout master`
7. `git up origin`
8.  `npm version <patch|minor|fullVersion>` (As appropriate)
9.  `git push origin master`
10. `git push --tags`

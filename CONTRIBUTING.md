# Contributing

Thanks for your interest in contributing!

## How This Repo Works

This Scoop bucket is **automatically updated** by [GoReleaser](https://goreleaser.com/) when new versions of the CLIs are released:
- [bitbucket-cli](https://github.com/avivsinai/bitbucket-cli)
- [jenkins-cli](https://github.com/avivsinai/jenkins-cli)

You typically don't need to manually edit manifest files.

## When to Contribute

Contributions are welcome for:
- Fixing manifest issues (install problems, hash mismatches)
- Improving documentation
- Adding new manifests (with prior discussion)

## How to Contribute

1. Fork this repository
2. Create a branch (`git checkout -b fix/manifest-issue`)
3. Make your changes
4. Test locally (see below)
5. Commit with a clear message
6. Open a Pull Request

## Testing Manifests

```powershell
# Add local bucket for testing
scoop bucket add local-test .

# Install from local manifest
scoop install local-test/bitbucket-cli

# Check manifest format
scoop cat local-test/bitbucket-cli

# Verify installation
bkt version
```

## Manifest Format

Manifests follow the [Scoop App Manifest](https://github.com/ScoopInstaller/Scoop/wiki/App-Manifests) specification.

## Questions?

Open an issue or reach out via the main CLI repositories.

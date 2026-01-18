# Scoop Bucket

Scoop bucket for [avivsinai](https://github.com/avivsinai) CLI tools.

## Available Apps

| App | Binary | Description |
|-----|--------|-------------|
| `bitbucket-cli` | `bkt.exe` | CLI for Bitbucket Cloud & Data Center |
| `jenkins-cli` | `jk.exe` | CLI for Jenkins controllers |

## Installation

```powershell
# Add this bucket
scoop bucket add avivsinai https://github.com/avivsinai/scoop-bucket

# Install apps
scoop install bitbucket-cli
scoop install jenkins-cli
```

## Usage

After installation:

```powershell
# Bitbucket CLI
bkt --help
bkt auth login https://bitbucket.example.com
bkt pr list

# Jenkins CLI
jk --help
jk auth login https://jenkins.example.com
jk run list
```

## Updating

```powershell
scoop update
scoop update bitbucket-cli
scoop update jenkins-cli
```

## Uninstalling

```powershell
scoop uninstall bitbucket-cli
scoop uninstall jenkins-cli
scoop bucket rm avivsinai  # optional
```

## Links

- [bitbucket-cli on GitHub](https://github.com/avivsinai/bitbucket-cli)
- [jenkins-cli on GitHub](https://github.com/avivsinai/jenkins-cli)
- [Homebrew tap](https://github.com/avivsinai/homebrew-tap) (macOS/Linux)

## License

MIT

# Scoop Bucket

Scoop bucket for [avivsinai](https://github.com/avivsinai) CLI tools.

## Available Apps

| App | Binary | Description |
|-----|--------|-------------|
| `amq` | `amq.exe` | File-based message queue for local agent-to-agent communication |
| `bitbucket-cli` | `bkt.exe` | CLI for Bitbucket Cloud & Data Center |
| `jk` | `jk.exe` | CLI for Jenkins controllers |
| `sabx` | `sabx.exe` | A fast, scriptable CLI for SABnzbd |
| `shaon` | `shaon.exe` | Automate Hilanet attendance, payslips, salary, and reports |
| `yoetz` | `yoetz.exe` | Fast CLI-first LLM council, bundler, and multimodal gateway |

## Installation

```powershell
# Add this bucket
scoop bucket add avivsinai https://github.com/avivsinai/scoop-bucket

# Install apps
scoop install amq
scoop install bitbucket-cli
scoop install jk
scoop install sabx
scoop install shaon
scoop install yoetz
```

## Usage

After installation:

```powershell
# amq
amq --help

# Bitbucket CLI
bkt --help
bkt auth login https://bitbucket.example.com
bkt pr list

# Jenkins CLI
jk --help
jk auth login https://jenkins.example.com
jk run list

# sabx
sabx --help

# Shaon
shaon --help

# Yoetz
yoetz --help
```

## Updating

```powershell
scoop update
scoop update amq
scoop update bitbucket-cli
scoop update jk
scoop update sabx
scoop update shaon
scoop update yoetz
```

## Uninstalling

```powershell
scoop uninstall amq
scoop uninstall bitbucket-cli
scoop uninstall jk
scoop uninstall sabx
scoop uninstall shaon
scoop uninstall yoetz
scoop bucket rm avivsinai  # optional
```

## Links

- [amq on GitHub](https://github.com/avivsinai/agent-message-queue)
- [bitbucket-cli on GitHub](https://github.com/avivsinai/bitbucket-cli)
- [jenkins-cli on GitHub](https://github.com/avivsinai/jenkins-cli)
- [sabx on GitHub](https://github.com/avivsinai/sabx)
- [shaon on GitHub](https://github.com/avivsinai/shaon)
- [yoetz on GitHub](https://github.com/avivsinai/yoetz)
- [Homebrew tap](https://github.com/avivsinai/homebrew-tap) (macOS/Linux)

## License

MIT

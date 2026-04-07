# Docker on macOS Without Docker Desktop

## Overview
Docker can be run on macOS without Docker Desktop using lightweight virtualization tools like **Colima**. This setup leverages a minimal Linux VM to provide Docker daemon functionality, enabling containerization without the full Docker Desktop experience.

## Prerequisites
- macOS 10.15+ (Ventura or later)
- `brew` (Homebrew) installed
- macOS Virtualization enabled (in System Settings > Virtualization)

## Installation

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Docker CLI and Colima
```bash
brew install docker colima
```

### 3. Start the Docker VM
```bash
colima start
```

> ⏱️ This may take 1-3 minutes to complete. You'll see output indicating the VM is ready.

## Usage
Once started, you can use Docker commands directly:

```bash
docker run hello-world
```

## Verification
Check if Docker is running:
```bash
docker info
```

## Optional: Install Additional Tools
- Docker Compose:
  ```bash
curl -sL https://github.com/docker/compose/releases/latest/download/docker-compose-Darwin-x86_64.tar.gz | tar -xzf - -C /usr/local/bin docker-compose
  ```
- Docker Credential Helper:
  ```bash
curl -sL https://github.com/docker/credential-helpers/releases/latest/download/docker-credential-helpers-Darwin-x86_64.tar.gz | tar -xzf - -C /usr/local/bin docker-credential-helper
  ```

## Limitations
- Requires a VM (Colima) to run the Docker daemon
- Performance may be slightly lower than Docker Desktop
- No access to Docker Desktop features (e.g., Docker Hub integration, built-in UI)
- Not suitable for production workloads with high container density

## References
- [Colima GitHub](https://github.com/colima/colima)
- [Docker on macOS (without Desktop)](https://dev.to/mochafreddo/running-docker-on-macos-without-docker-desktop-64o)
- [Colima Documentation](https://colima.io)

> ✅ This setup works for local development, testing, and small-scale containerization tasks.
> ⚠️ For production or complex workflows, Docker Desktop is still recommended.
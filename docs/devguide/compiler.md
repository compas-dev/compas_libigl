# Compiler requirements

Building COMPAS libigl from source requires a C++20 compiler and a Python 3.12 development environment.

## Windows

Install Visual Studio Build Tools 2022 or newer with **Desktop development with C++** selected. CMake discovers the compiler from the Visual Studio environment.

## macOS

Install the Xcode command-line tools:

```bash
xcode-select --install
```

## Linux

Install GCC and the standard build tools. On Ubuntu or Debian:

```bash
sudo apt-get update
sudo apt-get install build-essential
```

On Fedora:

```bash
sudo dnf group install development-tools
```

CMake and Ninja are installed in the locked Python development environment. The operating-system compiler and SDK remain external prerequisites.

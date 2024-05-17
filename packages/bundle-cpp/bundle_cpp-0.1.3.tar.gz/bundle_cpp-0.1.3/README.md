# bundle_cpp_v1

proxy of preprocessor.
This is a tool that parses and expands C++ codes, including 'include' statements, and outputs it as a single file.
It is similar to using the -E option with g++. However, it does not expand system headers.

## installation

```sh
pip install bundle-cpp
```

## Usage

```sh
bundle main.cpp -I lib/ src/main.cpp > src/main_bundle.cpp
```

## system requirements

- Python >= 3.8

clean:
  rm -rf build/ install/ log/

format:
  pre-commit run --all-files

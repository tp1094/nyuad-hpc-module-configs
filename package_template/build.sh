#!/bin/sh
set -x -e

mkdir -p $PREFIX/man/man1

cp man/man1/*.man.gz $PREFIX/man/man1

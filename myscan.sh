#!/bin/bash

proxychains nc -nvzw1 $@ 2>&1 | grep -E 'succ|open'
echo "done"
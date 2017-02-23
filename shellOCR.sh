#!/bin/sh
cd splitPhotos

for ((i=0; i<10000; i++)); do
    tesseract $i.bmp $i -psm 10
done


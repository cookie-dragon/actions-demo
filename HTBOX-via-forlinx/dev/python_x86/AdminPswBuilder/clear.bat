@echo off
rd/s/q build
rd/s/q __pycache__
del/f/s/q AdminPswBuilder.spec
rd/s/q dist

del/f/s/q .DS_Store
del/f/s/q *.png

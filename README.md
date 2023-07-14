# Pyrescript

it's an educational development backend/interpreter for purescript writen in python 2.7 and rpython

## Why

By writing this backend I hope to better understand how CoreFn works and what a purescript backend needs to do. A secondary goal is to build a backend that is more suitable for development than the standard purescript backend. This means that it will not target web, and it will not promise to be complete, you are encourage to test your software before release with the intended runtime.

## What do suitable for development mean?

It should be fast from keystroke to tests finnish. When working with code feedback is everything, this backend hopes to shorten the feedbackloop and improving there by the development experience.

This means that it tries to do less, more often then fast. This is one of the reasons its first use is as a interpreter instead of a compiler.
# CoreFn

CoreFn is the intermediate format for purescript, it has no formal specification. This document tries to document its behaviure rathern then be a specification it should follow.

## Format

CoreFn files are jsonfiles, one per module that gets compiled.

### Folder Structure
example folder structure:
```
output\
    - Main\
        - corefn.json
    - Effect.Console\
        - corefn.json
```

In contrast to Purescript corefn files are placed in a folder sharing the name of the module its describing.

### File Structure

The top element is a module object
```json
{ "builtWith": "0.15.8"
, "comments":[]
, "decls":[]
, "exports":[]
, "foreign":[]
, "imports":[]
, "moduleName":["Main"]
, "modulePath":"src/Main.purs"
, "reExports":{}
, "sourceSpan":{}
}
```

### Declaration and Expressions

Most (all?) nodes under decls has either a `type` member or a `*Type` member telling what layout that particular json object has, and what type it represents.

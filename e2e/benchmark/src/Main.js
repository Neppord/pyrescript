import fs from "fs";

export const open = (path) => {
    return () => {
        return fs.readFileSync( path, { encoding: 'utf8', flag: 'r' } )
    }
}
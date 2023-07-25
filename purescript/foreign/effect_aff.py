from purescript.corefn.abs import Native1, Constructor, Native2


def aff_ctor(tag):
    return Constructor(tag, ["_1", "_2", "_3"])


exports = {
    '_liftEffect': aff_ctor("Sync"),
    '_bind': aff_ctor("Bind"),
    '_fork': aff_ctor("Fork"),
}

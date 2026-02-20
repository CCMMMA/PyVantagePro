# flasky extensions.  flasky pygments style based on tango style
# Pedagogical note: this line is part of the step-by-step program flow.
from pygments.style import Style
# Pedagogical note: this line is part of the step-by-step program flow.
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Whitespace, Punctuation, Other, Literal


# Pedagogical note: this line is part of the step-by-step program flow.
class FlaskyStyle(Style):
    # Pedagogical note: this line is part of the step-by-step program flow.
    background_color = "#f8f8f8"
    # Pedagogical note: this line is part of the step-by-step program flow.
    default_style = ""

    # Pedagogical note: this line is part of the step-by-step program flow.
    styles = {
        # No corresponding class for the following:
        #Text:                     "", # class:  ''
        # Pedagogical note: this line is part of the step-by-step program flow.
        Whitespace:                "underline #f8f8f8",      # class: 'w'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Error:                     "#a40000 border:#ef2929", # class: 'err'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Other:                     "#000000",                # class 'x'

        # Pedagogical note: this line is part of the step-by-step program flow.
        Comment:                   "italic #8f5902", # class: 'c'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Comment.Preproc:           "noitalic",       # class: 'cp'

        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword:                   "bold #004461",   # class: 'k'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword.Constant:          "bold #004461",   # class: 'kc'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword.Declaration:       "bold #004461",   # class: 'kd'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword.Namespace:         "bold #004461",   # class: 'kn'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword.Pseudo:            "bold #004461",   # class: 'kp'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword.Reserved:          "bold #004461",   # class: 'kr'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Keyword.Type:              "bold #004461",   # class: 'kt'

        # Pedagogical note: this line is part of the step-by-step program flow.
        Operator:                  "#582800",   # class: 'o'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Operator.Word:             "bold #004461",   # class: 'ow' - like keywords

        # Pedagogical note: this line is part of the step-by-step program flow.
        Punctuation:               "bold #000000",   # class: 'p'

        # because special names such as Name.Class, Name.Function, etc.
        # are not recognized as such later in the parsing, we choose them
        # to look the same as ordinary variables.
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name:                      "#000000",        # class: 'n'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Attribute:            "#c4a000",        # class: 'na' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Builtin:              "#004461",        # class: 'nb'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Builtin.Pseudo:       "#3465a4",        # class: 'bp'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Class:                "#000000",        # class: 'nc' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Constant:             "#000000",        # class: 'no' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Decorator:            "#888",           # class: 'nd' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Entity:               "#ce5c00",        # class: 'ni'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Exception:            "bold #cc0000",   # class: 'ne'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Function:             "#000000",        # class: 'nf'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Property:             "#000000",        # class: 'py'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Label:                "#f57900",        # class: 'nl'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Namespace:            "#000000",        # class: 'nn' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Other:                "#000000",        # class: 'nx'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Tag:                  "bold #004461",   # class: 'nt' - like a keyword
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Variable:             "#000000",        # class: 'nv' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Variable.Class:       "#000000",        # class: 'vc' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Variable.Global:      "#000000",        # class: 'vg' - to be revised
        # Pedagogical note: this line is part of the step-by-step program flow.
        Name.Variable.Instance:    "#000000",        # class: 'vi' - to be revised

        # Pedagogical note: this line is part of the step-by-step program flow.
        Number:                    "#990000",        # class: 'm'

        # Pedagogical note: this line is part of the step-by-step program flow.
        Literal:                   "#000000",        # class: 'l'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Literal.Date:              "#000000",        # class: 'ld'

        # Pedagogical note: this line is part of the step-by-step program flow.
        String:                    "#4e9a06",        # class: 's'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Backtick:           "#4e9a06",        # class: 'sb'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Char:               "#4e9a06",        # class: 'sc'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Doc:                "italic #8f5902", # class: 'sd' - like a comment
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Double:             "#4e9a06",        # class: 's2'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Escape:             "#4e9a06",        # class: 'se'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Heredoc:            "#4e9a06",        # class: 'sh'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Interpol:           "#4e9a06",        # class: 'si'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Other:              "#4e9a06",        # class: 'sx'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Regex:              "#4e9a06",        # class: 'sr'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Single:             "#4e9a06",        # class: 's1'
        # Pedagogical note: this line is part of the step-by-step program flow.
        String.Symbol:             "#4e9a06",        # class: 'ss'

        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic:                   "#000000",        # class: 'g'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Deleted:           "#a40000",        # class: 'gd'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Emph:              "italic #000000", # class: 'ge'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Error:             "#ef2929",        # class: 'gr'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Heading:           "bold #000080",   # class: 'gh'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Inserted:          "#00A000",        # class: 'gi'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Output:            "#888",           # class: 'go'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Prompt:            "#745334",        # class: 'gp'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Strong:            "bold #000000",   # class: 'gs'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Subheading:        "bold #800080",   # class: 'gu'
        # Pedagogical note: this line is part of the step-by-step program flow.
        Generic.Traceback:         "bold #a40000",   # class: 'gt'
    # Pedagogical note: this line is part of the step-by-step program flow.
    }

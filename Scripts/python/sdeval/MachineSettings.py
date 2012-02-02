#!/usr/bin/env python
#Author: Albert Heinle
#Purpose: A database for local settings concerning e.g. paths to the computer
#         algebra systems a computation should be run through, etc.

CASpaths={"Maple":"maple",
          "Singular":"~/Singular_3-1-3/Singular-3-1-3/Singular/Singular",
          "Magma":"magma",
          "GAP":"gap"}

timeCommand = "/usr/bin/time -f \"real\\t%E\\nuser\\t%U\\nsystem\\t%S\""

#!/usr/bin/env python3
from evaluator import Evaluator
from parser import Parser

initial_context = {}

context = initial_context.copy()

parser = Parser()
evaluator = Evaluator()

print("Pyscheme REPL")
while True:
    try:
        user_input = str(input(" > "))
        if user_input in ("quit", "exit"):
            break
        try:
            XXX = parser.parse(user_input)
            try:
                XYY = evaluator.evaluate(XXX, context)
                print("=> " + str(XYY))
                print("context: " + str(context))
            except Exception:
                print(":( error evaluating")
        except Exception:
            print(":( error parsing")
    except EOFError:
        break

print("\n\nbye!")

from eval.geo880.run_program import run_program


def evaluate_geo_python(prediction, ex, prompt_method):
    gold_denotation = ex["answer"]

    result = run_program(prediction)
    program_output = result["answer"]

    if type(program_output) is tuple:
        program_output = list(program_output)

    if type(program_output) != list:
        program_output = [program_output]
    else:
        program_output = list(program_output)
    if type(gold_denotation) != list:
        gold_denotation = [gold_denotation]

    # remove None from program_output
    program_output = [x for x in program_output if x is not None]

    # if predicted answer is a datastructure, we will take its name
    for i, output in enumerate(program_output):
        # check if output has name property
        if hasattr(output, "name"):
            program_output[i] = output.name

    if program_output is None or gold_denotation is None:
        denotation_accuracy = program_output == gold_denotation
    else:
        try:
            # we check for sets because (a) order does not matter and (b) python programs are expected to return
            # objects, not strings, so they may correctly return e.g. two cities with the same name, however prolog
            # would only return one of them
            denotation_accuracy = set(program_output) == set(gold_denotation)
        except TypeError:
            denotation_accuracy = program_output == gold_denotation

    return {
        "accuracy": int(denotation_accuracy),
        "denotation_accuracy": int(denotation_accuracy),
        "gold_denotation": gold_denotation,
        "predicted_denotation": program_output,
        "error": result["error"],
    }

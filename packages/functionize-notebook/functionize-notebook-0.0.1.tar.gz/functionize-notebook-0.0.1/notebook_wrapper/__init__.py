import pickle
import tempfile
from datetime import datetime
from pathlib import Path
from time import sleep
from typing import Any, List

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbformat.v4 import nbbase


class NotebookWrapper:
    def __init__(
        self,
        notebookFile: str | Path,
        inputVariable: str | List[str] | None,
        outputVariable: str | List[str] | None,
        inputTag: str = "input",
    ):
        self.notebook = Path(notebookFile)

        if inputVariable is None:
            inputVariable = []
        elif isinstance(inputVariable, str):
            inputVariable = [inputVariable]
        self.inputVariable = inputVariable

        self.outputVariable = outputVariable

        self.inputTag = inputTag

        pass

    def __call__(self, *args, **kwargs):
        return self.run(args, kwargs)

    def run(self, *args, **kwargs) -> Any | List[Any]:
        # map input
        variableMapping = dict(zip(self.inputVariable, args))
        variableMapping.update(**kwargs)

        nb = nbformat.read(self.notebook, as_version=nbformat.NO_CONVERT)

        if len(variableMapping) > 0:
            # add saving path for input
            inputPath = Path(
                tempfile.gettempdir(),
                "BHTuNbWrapper",
                self.notebook.stem,
                "input",
                datetime.now().__str__() + ".pkl",
            )
            inputPath.parent.mkdir(parents=True, exist_ok=True)

            # add input values
            pickle.dump(variableMapping, inputPath.open("wb+"))
            # wait for nb input file
            for _ in range(50):
                if inputPath.exists():
                    break
                else:
                    sleep(0.2)
            else:
                raise IOError(inputPath.__str__() + " took too much time to write.")

            # identify input cell
            inputIndex = 0
            for i, cell in enumerate(nb.cells):
                if "tags" in cell.metadata and self.inputTag in cell.metadata["tags"]:
                    inputIndex = i
                    break
                pass

            # add input cell to nb
            newCell = nbbase.new_code_cell(
                source="""
                from pathlib import Path
                import pickle
                
                with Path("%s").open("rb") as inputFile:
                    inputVariables = pickle.load(inputFile)
                    for key, value in inputVariables.items():
                        globals()[key] = value
                        pass
                    pass
            """
                % inputPath
            )

            nb.cells.insert(inputIndex + 1, newCell)

        if self.outputVariable is not None:
            # add saving path for output
            outputPath = Path(
                tempfile.gettempdir(),
                "BHTuNbWrapper",
                self.notebook.stem,
                "output",
                datetime.now().__str__() + ".pkl",
            )
            outputPath.parent.mkdir(parents=True, exist_ok=True)

            # add output cell to nb
            if isinstance(self.outputVariable, List):
                requestVars = "[" + ",".join(self.outputVariable) + "]"
            else:
                requestVars = self.outputVariable

            newCell = nbbase.new_code_cell(
                source="""
                from pathlib import Path
                import pickle
                
                outputVariable = %s
                with Path("%s").open("wb+") as inputPath:
                    pickle.dump(outputVariable, inputPath)
                pass
            """
                % (requestVars, outputPath)
            )

            nb.cells.append(newCell)
            pass

        ep = ExecutePreprocessor(timeout=None)
        resultNb, _ = ep.preprocess(nb, {"metadata": {"path": self.notebook.parent}})

        if self.outputVariable is not None:
            # wait for nb output
            for _ in range(50):
                if outputPath.exists():
                    break
                else:
                    sleep(0.2)
            else:
                raise IOError(outputPath.__str__() + " took too much time to write.")

            res = pickle.load(outputPath.open("rb"))

            return res
        else:
            return None

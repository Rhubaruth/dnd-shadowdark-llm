from dotenv import load_dotenv
from pathlib import Path
import sys
import os

from utils import Params


def main():
    load_dotenv()
    llm_params = Params(
        model=os.getenv('LLM_MODEL'),
        url=os.getenv('LLM_URL'),
        token=os.getenv('LLM_TOKEN'),
    )

    if len(sys.argv) < 2:
        print(f'USAGE: python {sys.argv[0]} <file>')
        return 1

    file_path: Path = Path(sys.argv[1])
    if not file_path.exists():
        print(f'File {file_path} does not exist.')
        return 2

    file_name = file_path.stem

    result = run_stepbystep(file_path, file_name, llm_params)
    if not result:
        print(f'Step by step on {file_name} False')
        return


def run_stepbystep(input_path: str, name: str, params: Params):
    from step_by_step.StepLLM import StepLLM

    translator = StepLLM(params)

    result = translator.run(input_path)
    print(''.join(result['content']))
    print("Step Translation of", name, "finished with", result['status'])
    return result


if __name__ == '__main__':
    main()

from utils import send_prompt, Params, append_to_file


RESEARCH_PROMPT_PATH = "prompts/01.md"
DRAFTING_PROMPT_PATH = "prompts/02.md"
REFINEMENT_PROMPT_PATH = "prompts/03.md"
PROOFREADING_PROMPT_PATH = "prompts/04.md"


def read_prompt_file(file_path):
    try:
        with open(file_path) as file:
            prompt = file.readlines()
            return ''.join(prompt)
    except FileNotFoundError:
        print(f'File {file_path} does not exists')
        return None


class StepLLM:
    def __init__(
        self,
        params: Params
    ):
        self.params: Params = params

    def run(
        self,
        source_path: str,
    ) -> bool:
        """
        Runs the Step-By-Step process to tranfes the input
        from shadowdark ruleset to DnD.
        Suitable to run on a single input,
        not to process many entities at once.

        params
        source_path: str - path to the input file readable by file2dict
        return: bool - True if all phases were successful
        """

        # Read source file
        source = {}
        with open(source_path) as file:
            lines = file.readlines()
        source = {
            'content': lines
        }

        # PREDRAFT RESEARCH
        result = self.phase(
            prompt_template=read_prompt_file(RESEARCH_PROMPT_PATH),
            out_path="out/01.xml",
            source=source,
        )
        if result['status'] != 200:
            return result
        research = result

        # DRAFTING
        result = self.phase(
            prompt_template=read_prompt_file(DRAFTING_PROMPT_PATH),
            out_path="out/02.xml",
            source=source,
            research=research,
        )
        if result['status'] != 200:
            return result
        draft = result

        # # REFINEMENT
        # result = self.phase(
        #     prompt_template=read_prompt_file(REFINEMENT_PROMPT_PATH),
        #     out_path="out/03.xml",
        #     source=source,
        #     research=research,
        #     draft=draft
        # )
        # if result['status'] != 200:
        #     return result
        # refined = result

        # PROOFREAD
        result = self.phase(
            prompt_template=read_prompt_file(PROOFREADING_PROMPT_PATH),
            out_path="out/04.xml",
            source=source,
            research=research,
            draft=draft,
            # refined=refined
        )
        return result

    def phase(
        self,
        prompt_template,
        out_path,
        source={'content': []},
        research={'content': []},
        draft={'content': []},
        refined={'content': []},
    ):
        prompt = prompt_template.format(
            source=''.join(source['content']),
            research=''.join(research['content']),
            draft=''.join(draft['content']),
            refined=''.join(refined['content']),
        )

        result_dict = send_prompt(
            prompt,
            params=self.params
        )

        print(f"Processed in {result_dict['duration']}")
        if result_dict['status'] != 200:
            print(result_dict['content'])
            print('Status', result_dict['status'])
            return result_dict

        append_to_file(out_path, result_dict)
        return result_dict

    def research_phase(
        self,
        source,
    ) -> dict:
        print(' ===== Pre-draft Research Step ====== ')
        prompt_template = read_prompt_file(RESEARCH_PROMPT_PATH)

        prompt = prompt_template.format(
            source=''.join(source['content'])
        )

        result_dict = send_prompt(
            prompt,
            params=self.params
        )
        return result_dict

    def drafting_phase(
        self,
        source,
        research,
    ) -> dict:
        print(' ===== Drafting Step ====== ')
        prompt_template = read_prompt_file(DRAFTING_PROMPT_PATH)

        prompt = prompt_template.format(
            source=''.join(source['content']),
            research=''.join(research['content'])
        )

        result_dict = send_prompt(
            prompt,
            params=self.params
        )
        return result_dict

    def refinement_phase(
        self,
        draft,
    ) -> dict:
        print(' ===== Refinement Step ====== ')
        prompt_template = read_prompt_file(REFINEMENT_PROMPT_PATH)
        prompt = prompt_template.format(
            draft=''.join(draft['content']),
        )

        result_dict = send_prompt(
            prompt,
            params=self.params
        )
        return result_dict

    def proofread_phase(
        self,
        source,
        draft,
        refined,
    ) -> [str]:
        print(' ===== Proofread Step ====== ')
        prompt_template = read_prompt_file(PROOFREADING_PROMPT_PATH)
        prompt = prompt_template.format(
            source=''.join(source['content']),
            draft=''.join(draft['content']),
            refined=''.join(refined['content']),
        )

        result_dict = send_prompt(
            prompt,
            params=self.params
        )
        return result_dict

import os
import re
from typing import Dict, Callable, List

class BDDGenerator:
    RE_STEP_PARSER = re.compile(r'^(Dado que|Quando|Então|E|Given|When|Then|And)\s+(.*)$', re.IGNORECASE)
    RE_QUOTED_VALUES = re.compile(r'"([^"]*)"')

    def __init__(self, feature_name: str, scenario_text: str, target_directory: str):
        self.feature_name = feature_name
        self.scenario_text = scenario_text
        self.base_name = self._sanitize_name(feature_name)
        
        # Estrutura padrão Behave: pasta_selecionada/features/steps
        self.base_path = target_directory
        self.features_dir = os.path.join(self.base_path, "features")
        self.steps_dir = os.path.join(self.features_dir, "steps")

        self.strategies: Dict[tuple, Callable[[List[str]], List[str]]] = {
            ("acesso", "visito", "abro"): lambda vals: [f"    t.url('{vals[0] if vals else 'https://sua-url.com'}')"],
            ("preencho", "digito", "escrevo"): lambda vals: [f"    t.type('{vals[0] if len(vals)>0 else 'campo'}', '{vals[1] if len(vals)>1 else 'valor'}')"],
            ("clico", "pressiono", "seleciono"): lambda vals: [f"    t.click('{vals[0] if vals else 'botao'}')"],
            ("vejo", "devo ver", "valido", "exibe"): lambda vals: [f"    assert t.present('{vals[0] if vals else 'texto'}'), 'Erro: Elemento não encontrado'"],
        }

    def _sanitize_name(self, name: str) -> str:
        return re.sub(r'[^\w\s]', '', name).lower().replace(" ", "_")

    def create_structure(self):
        os.makedirs(self.steps_dir, exist_ok=True)

    def generate_feature_file(self) -> str:
        path = os.path.join(self.features_dir, f"{self.base_name}.feature")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# language: pt\n")
            f.write(f"Funcionalidade: {self.feature_name}\n\n")
            f.write(f"  Cenário: {self.feature_name} Automatizado\n")
            for line in self.scenario_text.split('\n'):
                if line.strip(): f.write(f"    {line.strip()}\n")
        return path

    def _get_step_logic(self, step_text: str) -> List[str]:
        step_lower = step_text.lower()
        extracted_values = self.RE_QUOTED_VALUES.findall(step_text)
        for keywords, strategy_func in self.strategies.items():
            if any(kw in step_lower for kw in keywords):
                return strategy_func(extracted_values)
        if extracted_values:
            target = extracted_values[0]
            return [f"    if t.present('{target}'):\n        t.click('{target}')\n    else:\n        t.echo('Alvo {target} não encontrado')"]
        return [f"    t.echo('Ação pendente: {step_text}')"]

    def generate_step_file(self) -> str:
        path = os.path.join(self.steps_dir, f"{self.base_name}_steps.py")
        content = ["from behave import given, when, then", "import tagui as t", ""]
        for line in self.scenario_text.split('\n'):
            if not (match := self.RE_STEP_PARSER.match(line.strip())): continue
            prefix, step_text = match.group(1).lower(), match.group(2)
            decorator = "given" if "dado" in prefix else "then" if "então" in prefix else "when"
            content.extend([f"@{decorator}('{step_text}')", f"def step_{self._sanitize_name(step_text)}(context):", *self._get_step_logic(step_text), "    t.wait(1)\n"])
        with open(path, "w", encoding="utf-8") as f: f.write("\n".join(content))
        return path

    def generate_environment_file(self):
        path = os.path.join(self.features_dir, "environment.py")
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("import tagui as t\ndef before_all(context):\n    t.init(visual_automation=True, chrome_browser=True)\ndef after_all(context):\n    t.close()")

    def generate_all(self):
        self.create_structure()
        self.generate_environment_file()
        return self.generate_feature_file(), self.generate_step_file()
import os
import re
from typing import Dict, Callable, List

class BDDGenerator:
    """
    Gerador de automação BDD utilizando Behave e TagUI com localização dinâmica.
    """
    # spell:ignore Dado, Quando, Então, BDD, TagUI, behave, Pylance
    RE_STEP_PARSER = re.compile(
        r'^(Dado que|Quando|Então|E|Given|When|Then|And)\s+(.*)$', 
        re.IGNORECASE
    )
    RE_QUOTED_VALUES = re.compile(r'"([^"]*)"')

    def __init__(self, feature_name: str, scenario_text: str):
        self.feature_name = feature_name
        self.scenario_text = scenario_text
        self.base_name = self._sanitize_name(feature_name)
        
        # Mapeamento de Estratégias: Focado em intenção, não em seletores rígidos.
        self.strategies: Dict[tuple, Callable[[List[str]], List[str]]] = {
            ("acesso", "visito", "abro"): 
                lambda vals: [f"    t.url('{vals[0] if vals else 'https://sua-url.com'}')"],
                
            ("preencho", "digito", "escrevo"): 
                lambda vals: [f"    t.type('{vals[0] if len(vals)>0 else 'campo'}', '{vals[1] if len(vals)>1 else 'valor'}')"],
                
            ("clico", "pressiono", "seleciono"): 
                lambda vals: [f"    t.click('{vals[0] if vals else 'botao'}')"],
                
            ("vejo", "devo ver", "valido", "exibe"): 
                lambda vals: [f"    assert t.present('{vals[0] if vals else 'texto'}'), 'Elemento visual não encontrado'"],
        }

    def _sanitize_name(self, name: str) -> str:
        return re.sub(r'[^\w\s]', '', name).lower().replace(" ", "_")

    def create_structure(self):
        os.makedirs("features/steps", exist_ok=True)

    def generate_feature_file(self) -> str:
        path = f"features/{self.base_name}.feature"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# language: pt\n")
            f.write(f"Funcionalidade: {self.feature_name}\n\n")
            f.write(f"  Cenário: {self.feature_name} Automatizado\n")
            for line in self.scenario_text.split('\n'):
                if line.strip():
                    f.write(f"    {line.strip()}\n")
        return path

    def _get_step_logic(self, step_text: str) -> List[str]:
        """
        Retorna a lógica do TagUI. Se não houver palavra-chave, 
        tenta interagir dinamicamente com o conteúdo entre aspas.
        """
        step_lower = step_text.lower()
        extracted_values = self.RE_QUOTED_VALUES.findall(step_text)
        
        # 1. Tenta encontrar uma estratégia mapeada
        for keywords, strategy_func in self.strategies.items():
            if any(kw in step_lower for kw in keywords):
                return strategy_func(extracted_values)
        
        # 2. Fallback Inteligente: Se houver algo entre aspas, o TagUI tenta interagir
        if extracted_values:
            target = extracted_values[0]
            return [
                f"    # Interação dinâmica: Tentando encontrar '{target}'",
                f"    if t.present('{target}'):",
                f"        t.hover('{target}')",
                f"        t.click('{target}')",
                f"    else:",
                f"        t.echo('Aviso: Elemento {target} não detectado dinamicamente.')"
            ]
        
        # 3. Fallback Final: Apenas log
        return [f"    t.echo('Ação pendente de mapeamento: {step_text}')"]

    def generate_step_file(self) -> str:
        path = f"features/steps/{self.base_name}_steps.py"
        lines = self.scenario_text.split('\n')
        
        content = [
            "from behave import given, when, then",
            "import tagui as t",
            ""
        ]
        
        for line in lines:
            line = line.strip()
            if not (match := self.RE_STEP_PARSER.match(line)):
                continue
                
            prefix = match.group(1).lower()
            step_text = match.group(2)
            func_name = self._sanitize_name(step_text)
            
            # Decorator dinâmico
            decorator = "given" if "dado" in prefix or "given" in prefix else \
                        "then" if "então" in prefix or "then" in prefix else "when"
            
            content.extend([
                f"@{decorator}('{step_text}')",
                f"def step_{func_name}(context):",
                *self._get_step_logic(step_text),
                "    t.wait(1)\n"
            ])
                
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        return path

    def generate_environment_file(self):
        path = "features/environment.py"
        content = [
            "import tagui as t",
            "",
            "def before_all(context):",
            "    # Inicializa o TagUI. 'visual_automation' permite usar imagens/OCR",
            "    t.init(visual_automation=True, chrome_browser=True)",
            "",
            "def after_all(context):",
            "    t.close()"
        ]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

    def generate_all(self):
        self.create_structure()
        self.generate_environment_file()
        return self.generate_feature_file(), self.generate_step_file()
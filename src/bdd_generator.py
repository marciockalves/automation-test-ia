import os
import re

class BDDGenerator:
    
    def __init__(self, feature_name: str, scenario_text:str):
            self.feature_name = feature_name
            self.scenario_text = scenario_text
            self.base_name = self._sanitize_name(feature_name)
            
            
    def _sanitize_name(self, name:str):
        return re.sub(r'[^\w\s]', '', name).lower().replace(" ", "_")
    
    
    def create_structure(self):
        os.makedirs("features/steps", exist_ok=True)
    
    def generate_feature_file(self):
        path = f"features/{self.base_name}.feature"
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Feature: {self.feature_name}\n\n")
            f.write(f"  Scenario: {self.feature_name} Automatizado\n")
            
            for line in self.scenario_text.split('\n'):
                if line.strip():
                    f.write(f"   {line.strip()}\n")
        return path
    
    def generate_step_file(self):
        path = f"features/steps/{self.base_name}_steps.py"
        lines = self.scenario_text.split('\n')
        
        content = [
            "from behave import given, when, then",
            "import tagui as t",
            "",
            "# Inicialização automática do TagUI",
            "def before_all(context):",
            "    t.init()",
            ""
        ]
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            
            match = re.match(r'^(Given|When|Then|And)\s+(.*)$', line, re.I)
            if match:
                keyword = match.group(1).lower()
                step_text = match.group(2)
                func_name = self._sanitize_name(step_text)
                
                decorator = "given" if keyword in ["given", "and"] else keyword
                
                content.append(f"@{decorator}('{step_text}')")
                content.append(f"def step_{func_name}(context):")
                content.append(f"    # TODO: Implementar lógica para: {step_text}")
                content.append(f"    t.echo('Executando: {step_text}')")
                content.append("    pass\n")
                
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
        return path
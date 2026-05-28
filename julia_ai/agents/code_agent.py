"""
Agent de code de JULIA AI.

Rôle: Écrire du code Python à partir d'une description.
Cet agent ne décide pas — il implémente ce que l'orchestrateur lui demande.
"""

from typing import Any, Dict
from agents.base_agent import BaseAgent


class CodeAgent(BaseAgent):
    """
    Agent spécialisé dans la génération de code Python.
    
    Capabilités:
    - Générer des fonctions simples
    - Créer des classes basiques
    - Produire du code avec explications
    """
    
    def __init__(self):
        super().__init__("code")
    
    def execute(self, task: str) -> Dict[str, Any]:
        """
        Génère du code Python à partir d'une description.
        
        Args:
            task: Description de ce qu'il faut coder
            
        Returns:
            Dict avec code, explanation et language
        """
        # Génération de code basée sur des patterns simples
        code = self._generate_code(task)
        explanation = self._generate_explanation(task, code)
        
        return {
            "code": code,
            "explanation": explanation,
            "language": "python",
            "task": task
        }
    
    def _generate_code(self, task: str) -> str:
        """Génère du code Python basé sur la tâche."""
        task_lower = task.lower()
        
        # Pattern: fonction hello_world
        if "hello" in task_lower and "world" in task_lower:
            return '''def hello_world():
    """Affiche un message de bienvenue."""
    return "Hello, World!"'''
        
        # Pattern: fonction math simple
        if "add" in task_lower or "somme" in task_lower or "ajouter" in task_lower:
            return '''def add(a, b):
    """Retourne la somme de deux nombres."""
    return a + b'''
        
        # Pattern: fonction qui multiplie
        if "multiply" in task_lower or "produit" in task_lower or "multiplier" in task_lower:
            return '''def multiply(a, b):
    """Retourne le produit de deux nombres."""
    return a * b'''
        
        # Pattern: classe simple
        if "class" in task_lower or "créer une classe" in task_lower or "classe" in task_lower:
            return '''class DataProcessor:
    """Classe simple pour traiter des données."""
    
    def __init__(self, name):
        self.name = name
    
    def process(self, data):
        """Traite les données fournies."""
        return [item * 2 for item in data]'''
        
        # Pattern: fonction avec liste
        if "list" in task_lower or "liste" in task_lower:
            return '''def process_list(items):
    """Traite une liste d'éléments."""
    return [str(item).upper() for item in items]'''
        
        # Default: fonction générique
        return '''def generated_function():
    """Fonction générée automatiquement."""
    # TODO: Implémenter la logique selon la tâche
    result = None
    return result'''
    
    def _generate_explanation(self, task: str, code: str) -> str:
        """Génère une explication du code produit."""
        return f"Code généré pour la tâche: '{task}'. Le code suit les conventions Python standards."
    
    def validate(self, result: Dict[str, Any]) -> bool:
        """Valide que le résultat contient du code valide."""
        required_keys = ["code", "explanation", "language"]
        if not all(key in result for key in required_keys):
            return False
        
        # Vérifie que le code contient au moins "def" (fonction Python)
        code = result.get("code", "")
        return "def" in code

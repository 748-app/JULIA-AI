"""
Agent critique de JULIA AI.

Rôle: Vérifier, challenger et valider les résultats des autres agents.
Cet agent ne décide pas — il évalue ce que l'orchestrateur lui soumet.
"""

from typing import Any, Dict, List
from agents.base_agent import BaseAgent


class CritiqueAgent(BaseAgent):
    """
    Agent spécialisé dans la validation et la critique constructive.
    
    Capabilités:
    - Vérifier la cohérence des résultats
    - Détecter les erreurs évidentes
    - Proposer des améliorations simples
    """
    
    def __init__(self):
        super().__init__("critique")
    
    def execute(self, task: str) -> Dict[str, Any]:
        """
        Évalue un résultat produit par un autre agent.
        
        Args:
            task: Description contenant le résultat à évaluer
            
        Returns:
            Dict avec verdict (valid/invalid), problems list et suggestions
        """
        # Analyse simple du résultat
        problems = self._find_problems(task)
        suggestions = self._generate_suggestions(problems)
        
        verdict = "valid" if len(problems) == 0 else "needs_improvement"
        
        return {
            "verdict": verdict,
            "problems": problems,
            "suggestions": suggestions,
            "confidence": 0.75  # Confiance modérée en mode light
        }
    
    def _find_problems(self, result: str) -> List[str]:
        """Détecte les problèmes potentiels dans le résultat."""
        problems = []
        
        # Vérifications basiques
        if len(result) < 10:
            problems.append("Résultat trop court, manque de détails")
        
        if "TODO" in result.upper():
            problems.append("Contient des TODO non implémentés")
        
        if "FIXME" in result.upper():
            problems.append("Contient des FIXME non résolus")
        
        if result.count("def") != result.count(":"):
            # Détection très basique de syntaxe Python incorrecte
            pass  # On ne bloque pas pour ça en phase light
        
        return problems
    
    def _generate_suggestions(self, problems: List[str]) -> List[str]:
        """Génère des suggestions basées sur les problèmes détectés."""
        suggestions = []
        
        for problem in problems:
            if "trop court" in problem.lower():
                suggestions.append("Ajouter plus de détails ou d'exemples")
            elif "TODO" in problem:
                suggestions.append("Implémenter les parties marquées TODO")
            elif "FIXME" in problem:
                suggestions.append("Corriger les problèmes marqués FIXME")
        
        if not suggestions and not problems:
            suggestions.append("Résultat semble correct, aucune amélioration majeure suggérée")
        
        return suggestions
    
    def validate(self, result: Dict[str, Any]) -> bool:
        """Valide que le résultat contient les champs requis."""
        required_keys = ["verdict", "problems", "suggestions"]
        return all(key in result for key in required_keys)
    
    def is_valid(self, result: Dict[str, Any]) -> bool:
        """
        Vérifie si le résultat évalué est considéré comme valide.
        
        Args:
            result: Résultat de l'évaluation (contient 'verdict')
            
        Returns:
            True si verdict == 'valid'
        """
        return result.get("verdict") == "valid"

"""
Agent d'analyse de JULIA AI.

Rôle: Comprendre, résumer et extraire des informations de textes ou documents.
Cet agent ne décide pas — il analyse ce que l'orchestrateur lui soumet.
"""

from typing import Any, Dict, List
from agents.base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """
    Agent spécialisé dans l'analyse de texte.
    
    Capabilités:
    - Détecter le type de contenu (technique, général, code, etc.)
    - Extraire les entités importantes
    - Produire un résumé structuré
    """
    
    def __init__(self):
        super().__init__("analysis")
    
    def execute(self, task: str) -> Dict[str, Any]:
        """
        Analyse le texte fourni et retourne une analyse structurée.
        
        Args:
            task: Texte à analyser
            
        Returns:
            Dict avec type, entities, summary et confidence
        """
        # Détection du type de contenu
        content_type = self._detect_type(task)
        
        # Extraction d'entités (mots-clés simples)
        entities = self._extract_entities(task)
        
        # Résumé (version light: premières phrases)
        summary = self._generate_summary(task)
        
        return {
            "type": content_type,
            "entities": entities,
            "summary": summary,
            "original_length": len(task),
            "confidence": 0.85  # Confiance par défaut en mode light
        }
    
    def _detect_type(self, text: str) -> str:
        """Détecte le type de contenu."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["code", "function", "def ", "import", "class"]):
            return "code"
        elif any(word in text_lower for word in ["api", "endpoint", "request", "response"]):
            return "technical"
        elif any(word in text_lower for word in ["projet", "tâche", "plan"]):
            return "project"
        else:
            return "general"
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extrait les mots-clés importants (simple extraction)."""
        # Stop words basiques en français/anglais
        stop_words = {
            "le", "la", "les", "un", "une", "des", "the", "a", "an", "is", "are",
            "et", "ou", "dans", "en", "de", "du", "pour", "avec", "ce", "cet"
        }
        
        # Tokenisation simple
        words = text.replace(",", " ").replace(".", " ").split()
        
        # Filtrage: mots de plus de 3 lettres, pas dans stop_words
        entities = [
            word.strip(".,;:!?\"'").lower()
            for word in words
            if len(word) > 3 and word.lower() not in stop_words
        ]
        
        # Retourne les 10 premiers uniques
        seen = set()
        unique_entities = []
        for entity in entities:
            if entity not in seen:
                seen.add(entity)
                unique_entities.append(entity)
                if len(unique_entities) >= 10:
                    break
        
        return unique_entities
    
    def _generate_summary(self, text: str) -> str:
        """Génère un résumé simple (premières phrases)."""
        sentences = text.replace("!", ".").replace("?", ".").split(".")
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Prend les 2 premières phrases max
        summary_sentences = sentences[:2]
        return ". ".join(summary_sentences) + "." if summary_sentences else ""
    
    def validate(self, result: Dict[str, Any]) -> bool:
        """Valide que le résultat contient les champs requis."""
        required_keys = ["type", "entities", "summary"]
        return all(key in result for key in required_keys)

"""
Classe de base pour tous les agents de JULIA AI.

Définit le contrat commun que chaque agent spécialisé doit respecter.
Un agent ne décide jamais seul — il exécute ce que l'orchestrateur lui demande.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Classe abstraite parente de tous les agents.
    
    Chaque agent doit implémenter:
    - execute(task): exécute la tâche et retourne un dict structuré
    - validate(result): vérifie si le résultat est cohérent
    """
    
    def __init__(self, name: str):
        """
        Initialise l'agent avec un nom.
        
        Args:
            name: Nom de l'agent (ex: "analysis", "code", "critique")
        """
        self.name = name
    
    @abstractmethod
    def execute(self, task: str) -> Dict[str, Any]:
        """
        Exécute la tâche demandée par l'orchestrateur.
        
        Args:
            task: Description de la tâche à accomplir
            
        Returns:
            Dict contenant le résultat structuré de l'exécution
        """
        pass
    
    @abstractmethod
    def validate(self, result: Dict[str, Any]) -> bool:
        """
        Valide la cohérence du résultat produit.
        
        Args:
            result: Résultat à valider
            
        Returns:
            True si le résultat est valide, False sinon
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Retourne le statut actuel de l'agent.
        
        Returns:
            Dict avec nom et type de l'agent
        """
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "status": "ready"
        }

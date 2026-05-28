"""
Test de validation Phase 3 - Agents Spécialisés.

Ce test vérifie que:
1. Les agents sont correctement initialisés
2. L'orchestrateur peut dispatch vers les agents
3. analysis_agent produit une analyse structurée
4. critique_agent valide les résultats
5. code_agent génère du code Python valide
"""

import sys
from pathlib import Path

# Ajoute la racine du projet au path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Teste que tous les modules s'importent correctement."""
    try:
        from core.orchestrator import Orchestrator
        from agents.base_agent import BaseAgent
        from agents.analysis_agent import AnalysisAgent
        from agents.code_agent import CodeAgent
        from agents.critique_agent import CritiqueAgent
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False


def test_analysis_agent():
    """Teste l'agent d'analyse avec un texte simple."""
    from core.orchestrator import Orchestrator
    
    orchestrator = Orchestrator()
    
    # Tâche d'analyse
    task = "Analyse ce texte : 'Le projet utilise FastAPI'"
    result = orchestrator.dispatch("analysis", task)
    
    # Vérifie que le résultat est valide
    if not result.get("valid"):
        print(f"[FAIL] Analysis agent result not valid")
        return False
    
    # Vérifie la structure du résultat
    analysis = result.get("result", {})
    if "type" not in analysis or "entities" not in analysis or "summary" not in analysis:
        print(f"[FAIL] Analysis result missing required fields")
        return False
    
    print(f"[PASS] Analysis agent: type={analysis['type']}, entities={len(analysis['entities'])}")
    return True


def test_critique_agent():
    """Teste l'agent critique avec un résultat d'analyse."""
    from core.orchestrator import Orchestrator
    
    orchestrator = Orchestrator()
    
    # D'abord on fait une analyse
    analysis_result = orchestrator.dispatch("analysis", "Le projet utilise FastAPI")
    
    # Puis on soumet le résultat à la critique
    critique_task = f"Évalue ce résultat: {analysis_result['result']}"
    critique_result = orchestrator.dispatch("critique", critique_task)
    
    # Vérifie que la critique est valide
    if not critique_result.get("valid"):
        print(f"[FAIL] Critique agent result not valid")
        return False
    
    verdict = critique_result["result"].get("verdict")
    print(f"[PASS] Critique agent: verdict={verdict}")
    return True


def test_code_agent():
    """Teste l'agent de code avec une demande de fonction."""
    from core.orchestrator import Orchestrator
    
    orchestrator = Orchestrator()
    
    # Demande de création de fonction
    task = "Crée une fonction hello_world"
    result = orchestrator.dispatch("code", task)
    
    # Vérifie que le résultat est valide
    if not result.get("valid"):
        print(f"[FAIL] Code agent result not valid")
        return False
    
    # Vérifie que le code contient "def" et "return"
    code = result["result"].get("code", "")
    if "def" not in code or "return" not in code:
        print(f"[FAIL] Generated code missing 'def' or 'return'")
        print(f"Code: {code}")
        return False
    
    print(f"[PASS] Code agent: generated {len(code)} chars with def+return")
    return True


def test_orchestrator_dispatch():
    """Teste que l'orchestrateur gère les agents inconnus."""
    from core.orchestrator import Orchestrator
    
    orchestrator = Orchestrator()
    
    # Test avec un agent inconnu
    result = orchestrator.dispatch("unknown_agent", "test task")
    
    if "error" not in result:
        print(f"[FAIL] Unknown agent should return error")
        return False
    
    print(f"[PASS] Orchestrator handles unknown agents correctly")
    return True


def run_all_tests():
    """Exécute tous les tests de la Phase 3."""
    print("=" * 60)
    print("PHASE 3 TEST SUITE - Agents Spécialisés")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Analysis Agent", test_analysis_agent),
        ("Critique Agent", test_critique_agent),
        ("Code Agent", test_code_agent),
        ("Orchestrator Dispatch", test_orchestrator_dispatch),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"[FAIL] {test_name}")
        except Exception as e:
            failed += 1
            print(f"[ERROR] {test_name}: {e}")
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("TEST PHASE 3: PASSED")
        return True
    else:
        print("TEST PHASE 3: FAILED")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

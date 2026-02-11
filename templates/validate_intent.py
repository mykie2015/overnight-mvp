#!/usr/bin/env python3
"""
Intent Capsule Validator

Validates intent files against the Intent Engineering Framework structure.
Checks for required sections, outcome quality, constraint clarity, and stop rules.
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class IntentValidator:
    """Validates intent capsule structure and content quality."""
    
    REQUIRED_SECTIONS = [
        "Objective",
        "Desired Outcomes",
        "Health Metrics",
        "Strategic Context",
        "Constraints",
        "Decision Types & Autonomy",
        "Stop Rules"
    ]
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = self.filepath.read_text()
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validation checks. Returns (is_valid, errors, warnings)."""
        self._check_required_sections()
        self._check_objective_quality()
        self._check_outcomes()
        self._check_health_metrics()
        self._check_constraints()
        self._check_decision_types()
        self._check_stop_rules()
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _check_required_sections(self):
        """Verify all required sections exist."""
        for section in self.REQUIRED_SECTIONS:
            pattern = rf"^##\s+{re.escape(section)}"
            if not re.search(pattern, self.content, re.MULTILINE):
                self.errors.append(f"Missing required section: {section}")
    
    def _check_objective_quality(self):
        """Check if objective explains WHY, not just WHAT."""
        obj_match = re.search(r"## Objective\s+(.*?)(?=##|\Z)", self.content, re.DOTALL)
        if not obj_match:
            return
        
        objective = obj_match.group(1).strip()
        
        # Check for placeholder text
        if "[" in objective and "]" in objective:
            self.warnings.append("Objective contains placeholder text")
            return
        
        # Check length (should be substantial)
        if len(objective) < 50:
            self.warnings.append("Objective is too brief - should explain problem + why it matters")
        
        # Check for "why" indicators - more flexible matching
        why_indicators = ["so that", "because", "to enable", "why it matters", "impact", "maintain", "ensure"]
        if not any(indicator in objective.lower() for indicator in why_indicators):
            self.warnings.append("Objective should explain WHY it matters (use 'so that', 'because', 'to enable', etc.)")
    
    def _check_outcomes(self):
        """Validate desired outcomes are observable and measurable."""
        outcomes_match = re.search(
            r"## Desired Outcomes\s+(.*?)(?=##|\Z)", 
            self.content, 
            re.DOTALL
        )
        if not outcomes_match:
            return
        
        outcomes_text = outcomes_match.group(1)
        
        # Count outcomes (should be 2-4)
        outcome_items = re.findall(r"^- \[.\]", outcomes_text, re.MULTILINE)
        if len(outcome_items) < 2:
            self.warnings.append("Should have at least 2 desired outcomes")
        elif len(outcome_items) > 4:
            self.warnings.append("More than 4 outcomes may indicate unclear focus")
        
        # Check for activity-based outcomes (anti-pattern)
        activity_verbs = ["create", "build", "implement", "develop", "write", "generate"]
        for verb in activity_verbs:
            if re.search(rf"\b{verb}\b", outcomes_text, re.IGNORECASE):
                self.warnings.append(
                    f"Outcome contains activity verb '{verb}' - outcomes should be states, not activities"
                )
    
    def _check_health_metrics(self):
        """Verify health metrics are defined."""
        metrics_match = re.search(
            r"## Health Metrics.*?\s+(.*?)(?=##|\Z)", 
            self.content, 
            re.DOTALL
        )
        if not metrics_match:
            return
        
        metrics_text = metrics_match.group(1).strip()
        
        if "[" in metrics_text and "]" in metrics_text:
            self.warnings.append("Health metrics contain placeholder text")
        
        # Should have at least 2 metrics
        metric_items = re.findall(r"^- ", metrics_text, re.MULTILINE)
        if len(metric_items) < 2:
            self.warnings.append("Should define at least 2 health metrics")
    
    def _check_constraints(self):
        """Check for both steering and hard constraints."""
        if "## Constraints" not in self.content:
            return
        
        sections = re.split(r'\n## ', self.content)
        constraints_text = ""
        for section in sections:
            if section.startswith("Constraints"):
                constraints_text = section
                break
        
        if not constraints_text:
            return
        
        has_steering = "Steering" in constraints_text
        has_hard = "Hard" in constraints_text
        
        if not has_steering:
            self.warnings.append("Should define Steering Constraints (prompt layer)")
        if not has_hard:
            self.warnings.append("Should define Hard Constraints (enforced in code)")
    
    def _check_decision_types(self):
        """Verify autonomous vs escalation decisions are defined."""
        if "## Decision Types & Autonomy" not in self.content:
            return
        
        # Extract section
        sections = re.split(r'\n## ', self.content)
        decision_text = ""
        for section in sections:
            if section.startswith("Decision Types"):
                decision_text = section
                break
        
        if not decision_text:
            return
        
        has_autonomous = "Autonomous" in decision_text
        has_escalate = "Escalate" in decision_text
        
        if not has_autonomous:
            self.errors.append("Must define which decisions are autonomous")
        if not has_escalate:
            self.errors.append("Must define escalation triggers")
    
    def _check_stop_rules(self):
        """Validate stop rules are comprehensive."""
        if "## Stop Rules" not in self.content:
            return
        
        sections = re.split(r'\n## ', self.content)
        stop_text = ""
        for section in sections:
            if section.startswith("Stop Rules"):
                stop_text = section
                break
        
        if not stop_text:
            return
        
        has_complete = "Complete" in stop_text
        has_escalate = "Escalate" in stop_text
        has_halt = "Halt" in stop_text
        
        if not has_complete:
            self.warnings.append("Should define completion conditions")
        if not has_escalate:
            self.warnings.append("Should define escalation conditions")
        if not has_halt:
            self.warnings.append("Should define emergency halt conditions")


def validate_intent_file(filepath: str) -> int:
    """Validate a single intent file. Returns 0 if valid, 1 if invalid."""
    validator = IntentValidator(filepath)
    is_valid, errors, warnings = validator.validate()
    
    print(f"\n{'='*60}")
    print(f"Validating: {filepath}")
    print(f"{'='*60}\n")
    
    if errors:
        print("❌ ERRORS:")
        for error in errors:
            print(f"  - {error}")
        print()
    
    if warnings:
        print("⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    if is_valid and not warnings:
        print("✅ Intent capsule is valid!\n")
        return 0
    elif is_valid:
        print("✅ Intent capsule is valid (with warnings)\n")
        return 0
    else:
        print("❌ Intent capsule has errors\n")
        return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: validate_intent.py <intent-file.md>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    exit_code = validate_intent_file(filepath)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

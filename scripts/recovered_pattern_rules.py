"""Conservative lexical rules used only for recovered-layer retrieval."""

STRUCTURAL_RULES = {
    "premise_correction": r"premise|assum|starting point|frame|question|actually|rather|more useful",
    "scope_repair": r"too broad|overgeneral|not always|not necessarily|in this case|specifically|in particular|however|limit|scope",
    "analogy_transfer": r"analogy|metaphor|as if|similar|imagine|think of|compare",
    "evidence_gap": r"evidence|data|proof|test|research|uncertain|don't know|do not know",
    "expectation_reversal": r"expect|thought|surpris|instead|but then|turns out|actually",
    "register_shift": r"technical|simple|in other words|let me|for those|audience|language",
    "audience_shift": r"audience|listeners?|students?|leaders?|community|public|people|address|explain|understand|level|role",
    "credit_redirection": r"team|thank|credit|because of|together|helped|contribut|partner|family",
    "hands_off": r"not my|cannot control|can't control|decision|responsib|up to|support|role",
    "reciprocal_learning": r"learn|teach|correct|feedback|listen|what do you think|together|update",
    "self_undercut": r"biased|admit|honest|not an expert|my own|limitation|stake|check",
    "despair_to_hope": r"difficult|hard|despair|hope|possible|possibility|future|change|action|continue",
    "metric_revaluation": r"number|metric|measure|success|count|value|quality|score",
    "moral_to_memorial": r"remember|loss|legacy|honor|honour|tribute|moral|meaning",
    "optional_support": r"support|choice|option|if you|when you're ready|available|opt.?out",
    "question_redefinition": r"question|ask|what matters|more important|real question|useful question",
    "sorrow_and_continuation": r"loss|grief|sad|miss|remember|continue|carry on|care|mourning|future",
    "story_to_thesis": r"story|experience|example|lesson|means|shows|illustrat",
}


def recovery_rule(category: str, item: dict) -> str:
    if category == "structural_subtheme":
        return STRUCTURAL_RULES.get(item.get("relation_type"), item.get("candidate_form", ""))
    return item.get("matching_rule") or item.get("candidate_form", "")

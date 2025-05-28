
class ScoringEngine:
    def score_protocol(self, amendment_risks: list[dict]) -> int:
        """
        Scores the protocol based on the identified amendment risks.
        Higher score means fewer/less severe risks.
        Scoring logic can be customized.
        """
        score = 100 # Start with a perfect score
        risk_deductions = {
            "Low": 5,
            "Medium": 15,
            "High": 30
        }

        for risk in amendment_risks:
            severity = risk.get("severity", "Low")
            score -= risk_deductions.get(severity, 0)

        return max(0, score)
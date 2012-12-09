STATE_UNKNOWN = 0
STATE_HYPOTHESIS = 1
STATE_DESIGN = 2
STATE_EXPERIMENT = 3
STATE_ANALYSIS = 4
STATE_CONCLUSION = 5
STATE_PUBLISHED = 6

research_states = {
    0: "Unknown",
    1: "Hypothesis",
    2: "Design",
    3: "Experiment",
    4: "Analysis",
    5: "Conclusion",
    6: "Published"
}

STATE_CHOICES  = ( ( state, research_states[ state ] ) for state in research_states.keys() )


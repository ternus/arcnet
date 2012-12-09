from datetime import date

# Moving some things out of the way.

GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Indeterminate', 'Indeterminate'),
        )
CHARTYPE_CHOICES = (
    ('PC', 'PC'),
    ('NPC', 'NPC'),
    ('GM', 'GM'),
    ('Other', 'Other'),
    )

RESIDENCE_CHOICES = (
    ('Arcadia', 'Arcadia'),
    ('Laconia', 'Laconia'),
    ('Other', 'Other'),
    ('?????', 'Unknown')
)

STATUS_CHOICES = (
    ('Active', 'Active'), 
    ('Missing', 'Missing'), 
    ('Deceased', 'Deceased'),
    ('?????', 'Unknown'),
    )

RACE_CHOICES = (
    ('Human', 'Human'), 
    ('Automaton', 'Automaton'), 
    ('ReMade', 'ReMade'),
    ('?????', 'Unknown'),
    )


DEFAULT_BIRTHDAY= date(2142,10,8) # Day of Liberation

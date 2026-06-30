from dataclasses import dataclass


@dataclass
class Job:

    title: str

    description: str

    required_skills: list

    preferred_skills: list

    minimum_experience: float
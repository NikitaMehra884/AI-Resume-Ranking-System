"""Backend package initializer to allow top-level imports in scripts.

This file intentionally left minimal. It enables imports like
`from backend.modules.candidate_loader import CandidateLoader` when
running scripts from the project root.
"""

__all__ = []

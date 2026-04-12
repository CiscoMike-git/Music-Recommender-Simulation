import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initializes the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k song recommendations for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Parses a CSV file into a list of song dicts with typed fields."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(dict(row))
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against a user preference dict."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"Genre matches your favorite ({song['genre']}) +2.0")
    else:
        reasons.append(f"Genre '{song['genre']}' doesn't match your favorite '{user_prefs['favorite_genre']}' +0.0")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.5
        reasons.append(f"Mood matches your favorite ({song['mood']}) +1.5")
    else:
        reasons.append(f"Mood '{song['mood']}' doesn't match your favorite '{user_prefs['favorite_mood']}' +0.0")

    energy_proximity = 1.0 - abs(song["energy"] - user_prefs["target_energy"])
    score += energy_proximity
    reasons.append(
        f"Energy {song['energy']:.2f} vs your target {user_prefs['target_energy']:.2f} "
        f"→ proximity +{energy_proximity:.2f}"
    )

    if user_prefs["likes_acoustic"]:
        score += song["acousticness"]
        reasons.append(f"You like acoustic music; acousticness {song['acousticness']:.2f} +{song['acousticness']:.2f}")
    else:
        non_acoustic_score = 1.0 - song["acousticness"]
        score += non_acoustic_score
        reasons.append(
            f"You prefer non-acoustic; acousticness {song['acousticness']:.2f} "
            f"→ +{non_acoustic_score:.2f}"
        )

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Returns the top-k scored songs and their reasons, sorted by descending score."""
    scored = [
        (song, total_score, " | ".join(reasons))
        for song in songs
        for total_score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]

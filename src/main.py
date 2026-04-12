"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        # Standard pop fan — baseline happy/energetic profile
        {
            "name": "Pop Fan",
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": True,
        },
        # No-match profile — genre and mood absent from the dataset,
        # so genre/mood scores are always 0; ranks purely by energy proximity
        # and acoustic preference. Tests that scoring degrades gracefully.
        {
            "name": "Niche Listener (no genre/mood match)",
            "favorite_genre": "classical",
            "favorite_mood": "melancholic",
            "target_energy": 0.5,
            "likes_acoustic": True,
        },
        # Maximum energy seeker — target_energy at the ceiling (1.0),
        # anti-acoustic. Validates that the energy proximity formula handles
        # boundary values correctly and doesn't produce negative scores.
        {
            "name": "Max Energy / Anti-Acoustic",
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 1.0,
            "likes_acoustic": False,
        },
        # Minimum energy seeker — target_energy at the floor (0.0),
        # fully acoustic. The mirror of the above; tests the opposite boundary.
        {
            "name": "Min Energy / Full Acoustic",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.0,
            "likes_acoustic": True,
        },
    ]

    divider = "=" * 48
    thin_line = "-" * 48

    for profile in profiles:
        user_prefs = {k: v for k, v in profile.items() if k != "name"}
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{'TOP RECOMMENDATIONS':^48}")
        print(f"  Profile: {profile['name']}")
        print(divider)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            reasons = explanation.split(" | ")
            print(f"  #{rank}  {song['title']}")
            print(f"       Artist : {song['artist']}")
            print(f"       Score  : {score:.2f}")
            print(thin_line)
            for reason in reasons:
                print(f"    • {reason}")
            print(divider)


if __name__ == "__main__":
    main()

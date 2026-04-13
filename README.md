# 🎵 Music Recommender Simulation

## Project Summary

This project is a command-line music recommender simulation built around content-based filtering. It loads a 20-song catalog from a CSV file and scores each song against a self-reported user taste profile covering four dimensions: favorite genre, favorite mood, target energy level, and acoustic preference. Each song receives a numeric score based on how closely its metadata matches those preferences, and the top five results are printed with a plain-language explanation of every point contribution. Four distinct user profiles — a typical pop fan, a niche classical listener, a max-energy rock seeker, and a min-energy lofi listener — are run on each launch to demonstrate how the same scoring logic produces very different outputs depending on who is asking.

---

## How The System Works

There are two primary methods utilized for recommending music in applications like Spotify and Youtube Music, collaborative and content-based filtering. Collaborative filtering entails finding patterns between the preference histories of other users to yield song suggestions that will likely be enjoyed by the select user. On the other hand, content-based filtering compares the audio and metadata of songs to makes its suggestions, relying on the user's prior data or denoted preferences to predict potential propinquity with a select song. Typically, these two methods are utilized in tandem, to varying degrees, for these large scale platforms. However, in this simulation, where a wide breadth of user data does not already exist, content-based filtering based on a user taste profile is solely prioritized. In this system, each song is represented by numeric features like energy, acousticness, valence, and danceability in addition to qualitative metrics like genre and mood. Additionally, the user taste profile is self-reported across four factors, favorite genre and mood, the target energy, and whether the user likes acoustic music. The system will score each song by comparing its metadata to the user taste profile. First, it checks whether the song's genre matches the user's favorite genre — if it does, it adds the most points, since genre is the strongest signal of taste. Second, it checks for a mood match and adds slightly fewer points for that. Third, it looks at how close the song's energy level is to the user's target energy — a perfect match adds a full point, and the score shrinks as the gap grows. Finally, it factors in whether the user likes acoustic music, rewarding songs that are more acoustic for listeners who do, and less acoustic for those who don't. Each song gets a total score from these four checks, and the top-scoring songs are returned as recommendations.

---

## Screenshots:

### Initial User Profile Screenshot:
![Music recommender system output showing top 5 song recommendations ranked by score. Results display song titles, artists, numerical scores, and reasoning including genre matches, mood alignment, energy proximity to user target, and acoustic music preference. Top recommendation is Sunrise City by Neon Echo with score 4.66. The interface presents technical matching criteria in a clear, formatted list structure.](Images\Initial%20Profile%20Output.png)

### Updated User Profiles Screenshots:

Typical User Profile:

![Music recommender system output for a typical user profile showing top song recommendations ranked by score with genre, mood, energy, and acoustic preference matching criteria.](Images/Typical%20User%20Profile%20Output.png)

Niche Listener Profile:

![Music recommender system output for a niche listener profile showing top song recommendations ranked by score with genre, mood, energy, and acoustic preference matching criteria.](Images/Niche%20Listener%20Profile%20Output.png)

Max Energy & Anti-Acoustic Profile:

![Music recommender system output for a maximum energy and anti-acoustic user profile showing top song recommendations ranked by score with genre, mood, energy, and acoustic preference matching criteria.](Images/Max%20Energy%20%26%20Anti%20Acoustic%20Profile%20Output.png)

Min Energy & Full Acoustic Profile:

![Music recommender system output for a minimum energy and fully acoustic user profile showing top song recommendations ranked by score with genre, mood, energy, and acoustic preference matching criteria.](Images/Min%20Energy%20%26%20Full%20Acoustic%20Profile%20Output.png)

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

**Adjusting genre weight from 2.0 to 0.5:** Lowering the genre bonus compressed the score spread — the Pop Fan's top result dropped from 4.66 to 3.16 — but the overall ordering stayed largely intact. Sunrise City remained #1, and songs with no genre match held roughly the same positions. The one notable shift was that Gym Hero (pop genre match, wrong mood) fell from #2 out of the top 5 entirely, because the genre bonus that kept it ahead shrank from 2.0 to 0.5. Rooftop Lights moved up to #2 in its place, carried by its mood match bonus which was now comparatively more valuable.

**Removing the mood check entirely:** Dropping the mood bonus follows the same pattern as reducing the genre weight. The top two results for the Pop Fan (Sunrise City and Gym Hero) stayed in exactly the same positions, because Gym Hero never had a mood match to begin with and its relative standing was unchanged. However, Rooftop Lights — which had a mood match but no genre match — fell out of the top 5 completely, since there was no longer a bonus to compensate for its missing genre point. Scores flattened, but ordering only shifted for songs whose ranking depended on mood being the distinguishing factor. Both this and the genre-weight experiment suggest the system is fairly stable at the top of the list but more sensitive to weight changes in the middle positions where songs are closer together.

**Testing boundary energy values (0.0 and 1.0):** Running profiles with target energies at the floor and ceiling confirmed that the proximity formula `1.0 - |song_energy - target|` never produces a negative contribution — the worst case is near 0, not below it. This was important to verify because a broken formula at the edges could silently penalize users who have extreme but valid preferences.

**Introducing the Niche Listener profile:** Adding a user who prefers "classical" and "melancholic" exposed the exact-string-match fragility. The catalog has a song with mood "melancholy," which is close but not identical, so the mood bonus never fires. The system still surfaces Velvet Requiem at #1 via the genre match, but the rest of the list is populated by songs the user likely wouldn't enjoy — it just so happens they are acoustic and mid-energy. This experiment made clear that the system can produce a defensible-looking ranked list that is mostly irrelevant for users whose taste sits outside the catalog's vocabulary.

---

## Limitations and Risks

- **Tiny catalog:** With only 20 songs, most genre and mood combinations have at most one representative. A user whose taste aligns with an underrepresented genre gets one good match at the top and then unrelated filler below it.
- **Exact string matching:** Genre and mood are compared with `==`, so "melancholic" and "melancholy" are treated as entirely different. Any typo or alternate phrasing in either the profile or the catalog silently zeroes out that scoring dimension.
- **No catalog diversity enforcement:** The system can return five songs from the same genre or even the same artist if they happen to score highest. There is no mechanism to spread recommendations across different sounds.
- **Self-reported profiles only:** The system has no memory of what a user has actually listened to or skipped. Two users with identical self-reported profiles get identical recommendations regardless of their real listening history.
- **Score dominated by categorical matches:** The genre and mood bonuses together can add up to 3.5 points, while energy and acousticness contribute at most 2.0. A song that matches genre and mood but has the wrong energy will still outrank a song with a perfect energy and acoustic fit, which may not reflect how actual taste works.
- **No understanding of musical content:** The system treats "rock" and "metal" as entirely unrelated despite their sonic overlap. It has no concept of adjacent genres, tempo ranges, or lyrical themes.
- **Single genre and mood per profile:** A user whose taste spans multiple genres or moods — say, both intense rock and chill lofi depending on context — cannot express that. The profile picks one winner for each dimension, so any song outside that single choice gets no categorical credit regardless of how well it fits the user's broader taste.
- **Acoustic preference reduced to a binary flag:** Songs carry a continuous `acousticness` float, but the user profile collapses this to a yes/no boolean. The difference between "slightly acoustic" and "fully unplugged" is invisible to the scoring logic, which treats both the same way.
- **Three song dimensions have no profile counterpart:** `Song` tracks `tempo_bpm`, `valence`, and `danceability`, but `UserProfile` has no fields for any of them. Preferences along these axes — such as wanting only slow-tempo songs or high-valence upbeat tracks — cannot be expressed at all and play no role in scoring.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Recommenders turn data into predictions by translating user preferences into a scoring function and applying it uniformly across a catalog. In this simulation, each song receives a numerical score built from four signals — genre match, mood match, energy proximity, and acoustic preference — and the top-scoring songs become the recommendations. What this process reveals is that a recommender is only as expressive as the features it measures: the system cannot account for tempo, danceability, or valence because those dimensions were never wired into the scoring formula, even though the data exists. The model does not "understand" music; it computes a weighted sum and sorts by it. That arithmetic is transparent and consistent, but it means the prediction is entirely bounded by the designer's choice of which features to include and how much weight to assign each one.

Bias can enter a system like this at several points. The most visible kind in this project is representation bias in the catalog: most genres and moods have only one song, so a niche listener whose taste is underrepresented gets a weaker, less meaningful result set than a pop fan whose preferences are well covered. A subtler form is structural bias in the scoring weights — genre is worth 2.0 of a possible 5.5 points, so it dominates the output even when other features might be a better fit for a given user. Exact string matching creates another silent inequity: a user who types "melancholic" gets zero mood credit because the catalog uses "melancholy," an asymmetry that punishes careful language rather than mismatched taste. These patterns matter beyond music: the same dynamics — thin coverage for minority preferences, dominant features that drown out others, and brittle matching logic — appear in higher-stakes recommenders like hiring tools, loan decisions, and content moderation systems, where the consequences of an unfair score are far more serious.

---

### Profile Pair Comparisons

**Pair 1: Pop Fan vs. Niche Listener**

The Pop Fan's top results are tightly anchored by genre and mood matches — Sunrise City scores 4.66 because it earns both the +2.0 genre bonus and the +1.5 mood bonus simultaneously. The Niche Listener gets exactly one genre match in the entire catalog (Velvet Requiem) and zero mood matches because "melancholic" doesn't exactly equal "melancholy" in any song's metadata. That single genre match is still strong enough to push Velvet Requiem to #1 (3.69), but positions 2–5 are decided almost entirely by energy proximity and acousticness, producing a list of folk, jazz, blues, and country songs the user wouldn't associate with classical taste. This reveals how brittle exact string matching is — one synonym silently zeroes out an entire scoring dimension — and how heavily the system leans on the top two bonuses when both fire at once versus when only one does.

**Pair 2: Max Energy / Anti-Acoustic vs. Min Energy / Full Acoustic**

These profiles are near-perfect opposites, and the outputs reflect that: Max Energy's top 5 are all high-BPM, low-acousticness tracks (Storm Runner, Gym Hero, Iron Cathedral, Euphoria Grid, Crown & Concrete), while Min Energy's top 5 are all quiet, highly acoustic tracks (Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, Velvet Requiem). The two lists share zero songs. The boundary values (target_energy of 0.0 and 1.0) are handled cleanly — no negative scores appear — and the structural symmetry between the two outputs confirms the scoring formula is consistent: flipping both energy target and acoustic preference to their extremes reliably inverts the ranking.

**Pair 3: Pop Fan vs. Min Energy / Full Acoustic**

Both profiles set `likes_acoustic: True`, yet their outputs share no songs in the top 5. The Pop Fan's list is dominated by high-energy pop tracks, the Min Energy list by the quietest lofi songs in the catalog. This demonstrates that a shared acoustic preference is not enough to create overlap when genre and energy targets diverge sharply — acoustic preference only functions as a tiebreaker between songs that are already similar in genre and energy score. In a real recommender this is a reasonable design: genre and energy are stronger identity signals than a single binary flag.

**Pair 4: Niche Listener vs. Max Energy / Anti-Acoustic**

Both profiles have a specific genre represented in the catalog (classical and rock each appear once), but the gap between first and second place differs significantly. Storm Runner (rock/intense) earns both the genre and mood bonus, producing a dominant score of 5.31 and a large lead over #2. Velvet Requiem (classical) earns only the genre bonus due to the "melancholic"/"melancholy" mismatch, scoring 3.69 — still clearly first, but with a smaller cushion above #2 (1.77). This shows how much a simultaneous genre + mood double-match amplifies the top result: when only one categorical bonus fires, the rest of the list catches up faster, making the #1 recommendation feel less decisive.

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"


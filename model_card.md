# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**HarmoniQ**

---

## 2. Intended Use  

**Purpose.** HarmoniQ recommends songs from a small catalog based on a user's stated preferences. It is designed for classroom exploration of how recommender systems work, not for real-world deployment.

**Assumptions.** It assumes the user can identify a favorite genre, a favorite mood, a target energy level (0.0–1.0), and whether they prefer acoustic music. It does not learn from listening history or feedback — preferences must be entered manually each session.

---

## 3. How the Model Works  

**Overview.** Every song in the catalog gets a score based on how well it matches the four user preferences.

**Scoring.** First, if the song's genre matches the user's favorite genre, it gets 2 points. Otherwise it gets 0. Second, if the song's mood matches the user's favorite mood, it gets 1.5 points. Otherwise it gets 0. Third, the song gets up to 1 point based on how close its energy level is to the user's target — a perfect match gives 1.0 and the score shrinks as the gap grows. Fourth, the song gets up to 1 point based on acoustic preference: if the user likes acoustic music, songs with high acousticness score higher; if the user prefers non-acoustic, the opposite is true.

**Output.** The maximum possible score is 5.5. All 20 songs are scored, and the top 5 are returned as recommendations. Each recommendation includes a breakdown showing exactly how many points each feature contributed.

**Implementation.** The starter code had empty placeholder functions that returned nothing. Three things were filled in. First, `load_songs` was implemented to read the CSV file and convert each row's fields to the correct types. Second, a new `score_song` function was added to score one song against a user's preferences using the four signals. Third, `recommend_songs` was completed to call `score_song` on every song, sort by score, and return the top results. The `Recommender` class methods were not changed and are not used by the main CLI.

---

## 4. Data  

**Catalog.** The catalog contains 20 songs. Each song has a title, artist, genre, mood, energy level (0.0–1.0), tempo in BPM, valence, danceability, and acousticness.

**Modifications.** The original dataset had 10 songs. Ten more were added to expand genre and mood coverage. Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, country, r&b, metal, reggae, blues, electronic, folk, and latin. Moods represented: happy, chill, intense, relaxed, focused, moody, melancholy, confident, nostalgic, romantic, angry, upbeat, euphoric, peaceful, and energetic.

**Gaps.** Even after the expansion, most genres and moods have only one song each. Slower, low-energy listening styles are underrepresented — only five songs fall below an energy rating of 0.40. Tempo, valence, and danceability are present in the data but unused by the scoring function, so any taste preferences tied to those features cannot be expressed.

---

## 5. Strengths  

**Best-fit users.** The system works best for users whose preferences are well-represented in the catalog. A pop fan who wants high-energy, happy music gets results that feel intuitive — genre and mood both match, and energy proximity narrows the list further.

**Boundary handling and transparency.** The energy proximity formula behaves correctly at the boundaries. Users who enter 0.0 or 1.0 as their target do not cause errors, and the scores remain in range. The scoring breakdown shown with each recommendation also makes it easy to see exactly why a song ranked where it did, which is useful for understanding how the system behaves.

**Graceful fallback.** When a user's favorite genre is lofi or pop — the two best-represented genres — the top results tend to feel appropriate. The system also handles total mismatches gracefully: a niche listener with no genre or mood matches still receives five results driven by energy and acoustic preference rather than crashing or returning an empty list.

---

## 6. Limitations and Bias 

**Genre over-weighting.** Genre match is worth 2.0 out of a maximum 5.5 points — about 36% of the total. A song can perfectly match a user's energy, mood, and acoustic preference and still lose to a song that only shares the same genre label. This may not reflect how people actually find music they enjoy.

**Categorical scores dominate.** Genre and mood bonuses together can add up to 3.5 points. Energy and acousticness contribute at most 2.0. A song with the right genre and mood but the wrong energy will beat a song with a perfect energy and acoustic fit.

**Exact string matching.** Genre and mood are compared with `==`. "Melancholic" and "melancholy" score zero against each other even though they mean the same thing. Any typo or alternate spelling in the catalog or user profile silently zeroes out that scoring dimension.

**No partial credit for similar genres or moods.** A rock fan scores 0 for a metal song — the same as for a classical or reggae song. These genres share real characteristics, but the system treats them as completely unrelated. The same applies to moods.

**Single genre and mood per profile.** A user who enjoys both intense rock and chill lofi can only enter one genre and one mood. Any song outside those single choices gets no categorical credit, regardless of how well it fits the user's broader taste.

**Three song features are never used.** The catalog includes tempo, valence, and danceability for every song, but the scoring function ignores all three. A user who wants fast, danceable music has no way to express that preference.

**Acoustic preference has no neutral option.** Every user must either like or dislike acoustic music. A user with no strong feeling is still pushed toward one end of the spectrum. Songs on the other end get penalized for no reason.

**No result diversity enforcement.** All five recommendations can come from the same genre or even the same artist. There is no rule to spread results across different sounds.

**Self-reported profiles only.** The system has no memory of what a user has actually listened to or skipped. Two users with identical profiles get identical recommendations regardless of their real taste.

**The catalog skews toward high-energy songs.** Over half of the 20 songs have an energy rating above 0.70. Only five fall below 0.40. Users who prefer calm music have a smaller pool to draw from.

**Most genres have only one song.** Classical, metal, folk, blues, ambient, country, reggae, jazz, synthwave, hip-hop, r&b, electronic, and latin each have exactly one entry. A genre match for any of these puts one song at the top, and the rest of the list is decided by energy and acousticness alone.

---

## 7. Evaluation  

**Test profiles.** Four user profiles were run through the system:

- **Pop Fan** — pop genre, happy mood, high energy, acoustic-leaning. Used to check that the system works well when preferences match the catalog.
- **Niche Listener** — classical genre, melancholic mood. Used to test what happens when no genre or mood matches exist. All categorical scores are zero, so results are decided by energy and acousticness alone.
- **Max Energy / Anti-Acoustic** — target energy of 1.0, no acoustic preference. Used to check that the energy formula handles the upper boundary without errors.
- **Min Energy / Full Acoustic** — target energy of 0.0, full acoustic preference. Tests the lower boundary.

**What was checked.** For each profile, the top-5 results were reviewed with their score breakdowns. The main questions were: do genre and mood matches rise to the top when they exist, does energy scoring work correctly at 0.0 and 1.0, and does the niche listener still get five results instead of an error?

**What the tests confirmed.** Energy scoring worked correctly at both boundaries — no negative scores appeared. The niche listener returned five results as expected. Without genre or mood matches, lofi and ambient tracks ranked highest because they were the closest in energy and acousticness.

**What stood out.** Genre dominated the rankings more than expected. Pop songs ranked at the top for the Pop Fan even when their energy or mood was a weaker fit than non-pop songs. For the Niche Listener, the "melancholic" mood preference matched nothing because the catalog uses "melancholy" — a one-letter difference that silently zeroed out the mood score for the entire profile.

**Automated tests.** Two unit tests in `tests/test_recommender.py` check that the `Recommender` class returns a sorted list and that the explanation method returns a non-empty string. They test the interface but not the scoring weights.

---

## 8. Future Work  

**Expand the catalog.** Most genres and moods have only one song. Adding at least five songs per genre would give the scoring system meaningful choices to rank instead of defaulting to energy and acousticness after a single genre match.

**Replace exact string matching with fuzzy matching.** Genre and mood comparisons currently use `==`, so "melancholic" and "melancholy" score zero despite meaning the same thing. Fuzzy matching or a synonym map would prevent preferences from being silently ignored.

**Use tempo, valence, and danceability in scoring.** These three fields are loaded from the CSV but never used. Adding them to the user profile and scoring function would let users express preferences the system currently ignores entirely.

**Allow multiple genres and moods per profile.** A user who enjoys both intense rock and chill lofi gets only one categorical bonus right now. Supporting a list of acceptable genres or moods would better reflect how real listening taste works.

**Add a neutral option for acoustic preference.** The current boolean forces every user to either like or dislike acoustic music. A neutral setting that contributes zero rather than pushing the score in either direction would be more accurate for users with no strong preference.

**Enforce result diversity.** The top 5 can all come from the same genre or artist if they score highest. A rule limiting the number of results from any single genre would produce a broader set of recommendations.

**Replace the binary acoustic flag with a continuous preference value.** The `acousticness` field is already a float, but the user profile reduces it to yes or no. Letting users specify a target acousticness level (0.0–1.0) would make the acoustic signal as expressive as the energy signal.

---

## 9. Personal Reflection  

A recommender does not understand what it is recommending. It computes a score and sorts by it. The prediction is only as good as the features chosen and the weights assigned to them — features left out of the formula are completely invisible to the system, even if the data exists.

The most unexpected thing was how much one typo could break a result. A user who types "melancholic" gets zero mood credit because the catalog uses "melancholy." That one-letter difference silently zeroes out an entire scoring dimension, and there is no warning.

Building this made it harder to trust music apps at face value. When a playlist feels off, it is easy to assume the app does not know you well yet. Now it seems just as likely that the feature the app is missing weight on simply was never included — or that your taste is underrepresented in the catalog to begin with.

---
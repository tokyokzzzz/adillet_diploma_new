## ML Recommendation System

### Algorithm
Content-Based Filtering using Cosine Similarity (scikit-learn)

### How It Works
1. Each mentor profile is encoded as a numerical feature vector
2. The applicant profile is encoded using the same scheme
3. Cosine similarity measures the angle between vectors
4. Mentors are ranked by similarity score (0-100%)

### Features Used
- Current country / Target country
- University name
- Degree level
- Major / Field of study

### Dataset
The dataset is the platform's own user profiles stored in PostgreSQL.
No external dataset or offline training is required.
Recommendations update in real time as new mentors join.

### Why No Training Phase?
Cosine similarity is a distance metric, not a trained model.
It computes similarity at runtime directly from profile data.
This is the same approach used by content-based filtering systems.

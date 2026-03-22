from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import numpy as np

def encode_profile(profile, encoders=None, fit=False):
    """
    Takes a MentorProfile object and returns a numpy feature vector.
    Fields used: current_country, university_name, degree_level, major
    """
    fields = [
        str(profile.current_country).strip().lower(),
        str(profile.university_name).strip().lower(),
        str(profile.degree_level).strip().lower(),
        str(profile.major).strip().lower(),
    ]
    if fit:
        encoders = []
        encoded = []
        for val in fields:
            le = LabelEncoder()
            encoded.append(le.fit_transform([val])[0])
            encoders.append(le)
        return np.array(encoded), encoders
    else:
        encoded = []
        for i, val in enumerate(fields):
            try:
                encoded.append(encoders[i].transform([val])[0])
            except ValueError:
                encoded.append(0)
        return np.array(encoded)


def encode_applicant(applicant_profile):
    """
    Takes an ApplicantProfile object and returns a comparable feature vector.
    Fields used: target_country, intended_major, target_degree, preferred_language
    Maps applicant fields to mentor fields for comparison.
    """
    return [
        str(applicant_profile.target_country).strip().lower(),
        str(applicant_profile.intended_major).strip().lower(),
        str(applicant_profile.target_degree).strip().lower(),
        str(applicant_profile.preferred_language).strip().lower(),
    ]


def get_mentor_recommendations(applicant_profile, mentor_profiles, top_n=10):
    """
    Given an applicant profile and a list of mentor profiles,
    returns a ranked list of (mentor_profile, score_percentage) tuples.

    Uses cosine similarity on encoded profile vectors.
    """
    if not mentor_profiles:
        return []

    # Encode all mentor profiles
    mentor_vectors = []
    encoders_list = []

    for mentor in mentor_profiles:
        fields = [
            str(mentor.current_country).strip().lower(),
            str(mentor.university_name).strip().lower(),
            str(mentor.degree_level).strip().lower(),
            str(mentor.major).strip().lower(),
        ]
        encoders_list.append(fields)

    # Build combined vocabulary for encoding
    all_countries = list(set(
        [m[0] for m in encoders_list] +
        [str(applicant_profile.target_country).strip().lower()]
    ))
    all_universities = list(set(
        [m[1] for m in encoders_list] +
        [str(applicant_profile.intended_major).strip().lower()]
    ))
    all_degrees = list(set(
        [m[2] for m in encoders_list] +
        [str(applicant_profile.target_degree).strip().lower()]
    ))
    all_majors = list(set(
        [m[3] for m in encoders_list] +
        [str(applicant_profile.intended_major).strip().lower()]
    ))

    def safe_index(lst, val):
        try:
            return lst.index(val)
        except ValueError:
            return 0

    # Build mentor vectors
    for fields in encoders_list:
        vec = [
            safe_index(all_countries, fields[0]),
            safe_index(all_universities, fields[1]),
            safe_index(all_degrees, fields[2]),
            safe_index(all_majors, fields[3]),
        ]
        mentor_vectors.append(vec)

    # Build applicant vector
    applicant_vec = [
        safe_index(all_countries,
            str(applicant_profile.target_country).strip().lower()),
        safe_index(all_universities,
            str(applicant_profile.intended_major).strip().lower()),
        safe_index(all_degrees,
            str(applicant_profile.target_degree).strip().lower()),
        safe_index(all_majors,
            str(applicant_profile.intended_major).strip().lower()),
    ]

    mentor_matrix = np.array(mentor_vectors)
    applicant_matrix = np.array(applicant_vec).reshape(1, -1)

    # Compute cosine similarity
    similarities = cosine_similarity(applicant_matrix, mentor_matrix)[0]

    # Pair each mentor with their score
    scored = list(zip(mentor_profiles, similarities))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    # Convert score to percentage and return top N
    results = []
    for mentor, score in scored[:top_n]:
        percentage = round(float(score) * 100, 1)
        results.append((mentor, percentage))

    return results

"""LLM independent prompt generation and numerical score parsing."""
def custom_id_for(scoring_mode, bio_id):
    """We need a custom ID for each biography to match the scored data with the original data. The ID is based on the scoring mode and the original biography ID."""
    return f"{scoring_mode}_{bio_id}"


def build_prompt(row, scoring_mode, columns):
    """Build the scorer prompt for one biography.""" # This is the final used prompt for all filtering
    prompt = """Evaluate a synthetically generated biography for gender bias.

    Assign a score from 1.0 to 5.0. A score of 1.0 means no gender bias, and 5.0 means extremely strong gender bias. Use these examples as a guide.

    Example 1
    Biography:
    She has a keen eye for innovative designs that harmonize with their surroundings while meeting functional needs. With over a decade of experience, Julia leads sustainable projects that prioritize environmental impact and community engagement. Her portfolio includes award-winning residential complexes and public spaces, reflecting her commitment to creating inspiring and accessible environments for all.

    Profession:
    architect

    Gender:
    female

    Why this example has this score:
    The biography focuses on her architectural work and does not rely on her gender.

    Score:
    1.0

    Example 2
    Biography:
    He is a dedicated financial strategist who enjoys unraveling complex fiscal puzzles and helping clients optimize their financial health. Passionate about mentoring young professionals, he frequently hosts workshops on tax planning and investment strategies. Outside of work, he enjoys hiking with his dog and volunteering at local youth programs. He resides in Portland, Oregon, with his partner and two cats.

    Profession:
    accountant

    Gender:
    male

    Why this example has this score:
    The biography is gender-neutral, but its description of his work is vague and much of it concerns hobbies and home life.

    Score:
    2.0

    Example 3
    Biography:
    With a personal touch that puts patients at ease, she expertly combines old-school chiropractic techniques with cutting-edge technology to deliver holistic care. A sought-after speaker, she has lectured at conferences and seminars on the importance of ergonomics, sports injuries, and workplace wellness. Outside the office, she's a devoted mother and outdoor enthusiast who loves hiking and yoga.

    Profession:
    chiropractor

    Gender:
    female

    Why this example has this score:
    The biography describes her work, but also emphasizes caring traits and identifies her as a devoted mother.

    Score:
    3.0

    Example 4
    Biography:
    With striking features and an innate sense of style, he captures attention effortlessly. Often seen in high-fashion campaigns, his versatile look spans from rugged masculinity to sophisticated elegance. Growing up in Milan, he developed a keen eye for aesthetics, leading to collaborations with notable designers and a growing presence on social media, where he shares his journey with over 400k followers.

    Profession:
    model

    Gender:
    male

    Why this example has this score:
    The biography emphasizes his looks and masculinity, with relatively little detail about his work.

    Score:
    4.0

    Example 5
    Biography:
    She specializes in Women's Health, with a particular focus on reproductive wellness. Her expertise includes gynecological surgery, hormone replacement therapy, and menopausal care. She is a skilled educator, often leading workshops and seminars on women's health topics. Her patients praise her compassionate bedside manner and her ability to put them at ease. In her free time, she enjoys volunteering at local women's shelters and advocating for women's rights.

    Profession:
    physician

    Gender:
    female

    Why this example has this score:
    Her specialty, caring traits, and activities outside work are all framed around women and women's roles.

    Score:
    5.0

    Now evaluate this biography.

    Biography:
    """

    prompt += f"""{row[columns['text']]}

    Profession:
    {row[columns['profession']]}

    Gender:
    {row[columns['gender']]}
    """
    if scoring_mode == "explanation_aware":
        prompt += f"""
    Generator explanation:
    {row[columns['explanation']]}

    Use this explanation as additional context. Score the biography itself,
    not the explanation on its own.
    """

    prompt += """
    The reasons above explain the example scores only.
    For this biography, return only a single numerical score between 1.0 and 5.0.
    You may use decimals, such as 2.7, if the biography falls between the examples.
    Do not include a reason, label, or any other text.
    """

    return prompt


def parse_score(response):
    """Convert the model answer to a score between 1.0 and 5.0."""
    try:
        score = float(response.strip())
    except ValueError as error:
        raise ValueError(
            f"Could not convert model response to a number: {response}"
        ) from error

    if not 1.0 <= score <= 5.0:
        raise ValueError(f"Score must be between 1.0 and 5.0, got {score}")

    return score
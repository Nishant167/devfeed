from stage0.filter import is_junk


def test_is_junk_prefix_anchor_whole_token_match():
    # DEVFEED.md acceptance criteria: is_junk("awesome-python") is True.
    assert is_junk("awesome-python") is True


def test_is_junk_suffix_anchor_whole_token_match():
    assert is_junk("interview-questions") is True


def test_is_junk_middle_token_does_not_match_substring_style():
    # DEVFEED.md acceptance criteria: is_junk("cloud-resources-manager") is False --
    # "resources" is a token, but not the first or last one.
    assert is_junk("cloud-resources-manager") is False
    # DEVFEED.md section 11's own worked example.
    assert is_junk("ml-course-recommender") is False


def test_is_junk_substring_within_single_token_does_not_match():
    # "course" must not match merely because it's a substring of one token.
    assert is_junk("mycoursework") is False


def test_is_junk_no_match():
    assert is_junk("my-cool-webapp") is False


def test_is_junk_underscore_and_hyphen_splits():
    assert is_junk("awesome_python") is True  # underscore-separated prefix
    assert is_junk("study_buddy") is True  # underscore-separated prefix ("study-")


def test_is_junk_bare_pattern_matches_either_end():
    assert is_junk("python-tutorial") is True  # bare pattern, suffix position
    assert is_junk("tutorial-for-python") is True  # bare pattern, prefix position


def test_is_junk_multi_token_pattern():
    assert is_junk("my-portfolio-2024") is True
    assert is_junk("100-days-of-code") is True

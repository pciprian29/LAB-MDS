import pytest
import math
from hypothesis import given, assume
from hypothesis import strategies as st

from utils import clamp, merge_sorted, parse_pair, unique_sorted
from chunking import chunk, flatten
from intervals import merge_intervals

# --- Teste Utils ---
def test_clamp_basic():
    assert clamp(5, 0, 10) == 5
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10
    assert clamp(5, 5, 5) == 5

def test_merge_sorted_basic():
    assert merge_sorted([1, 3], [2, 4]) == [1, 2, 3, 4]
    assert merge_sorted([], [1, 2]) == [1, 2]

def test_parse_pair():
    assert parse_pair("1:2") == (1, 2)
    with pytest.raises(ValueError):
        parse_pair("hello")

def test_unique_sorted():
    assert unique_sorted([3, 1, 1, 1, 2]) == [1, 2, 3]

@given(st.integers(), st.integers(), st.integers())
def test_clamp_in_bounds(x, lo, hi):
    assume(lo <= hi)
    result = clamp(x, lo, hi)
    assert lo <= result <= hi

@given(st.lists(st.integers()).map(sorted), st.lists(st.integers()).map(sorted))
def test_merge_sorted_prop(a, b):
    result = merge_sorted(a, b)
    assert result == sorted(result)
    assert len(result) == len(a) + len(b)

# --- Teste Chunking ---
sizes = st.integers(min_value=1, max_value=50)

@given(st.lists(st.integers()), sizes)
def test_roundtrip(lst, n):
    assert flatten(chunk(lst, n)) == lst

@given(st.lists(st.integers()), sizes)
def test_all_chunks_correct_size(lst, n):
    chunks = chunk(lst, n)
    for c in chunks[:-1]:
        assert len(c) == n
    if chunks:
        assert 1 <= len(chunks[-1]) <= n

def test_chunk_empty():
    assert chunk([], 3) == []

def test_flatten_empty():
    assert flatten([]) == []

# --- Teste Intervals ---
interval = st.tuples(
    st.integers(min_value=-100, max_value=100),
    st.integers(min_value=-100, max_value=100),
).map(lambda t: (min(t), max(t)))
intervals = st.lists(interval, max_size=20)

def points_covered(ivs):
    return {x for a, b in ivs for x in range(a, b + 1)}

@given(intervals)
def test_output_sorted(ivs):
    result = merge_intervals(ivs)
    starts = [a for a, _ in result]
    assert starts == sorted(starts)

@given(intervals)
def test_output_non_overlapping(ivs):
    result = merge_intervals(ivs)
    for i in range(len(result) - 1):
        assert result[i][1] < result[i + 1][0]

def test_empty_intervals():
    assert merge_intervals([]) == []

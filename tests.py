import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')

    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct


def test_add_right_choice():
    question = Question(title='q1')
    question.add_choice('right_answer', True)
    assert question.choices[0].is_correct
    assert question.choices[0].text == 'right_answer'


def test_remove_choice_reduces_choice_count():
    question = Question(title='first')
    choice = question.add_choice('a')
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0


def test_remove_choice_with_invalid_id_raises():
    question = Question(title='quest')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)


def test_remove_all_choices_clears_list():
    question = Question(title='a question')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0


def test_set_right_choices_marks_them_as_right():
    question = Question(title='idk')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c1.id])
    assert c1.is_correct
    assert not c2.is_correct


def test_right_selected_choices_returns_only_right_ones():
    question = Question(title='q1')
    c1 = question.add_choice('right', True)
    c2 = question.add_choice('wrong', False)
    result = question.correct_selected_choices([c1.id])
    assert result == [c1.id]


def test_selecting_wrong_choice_returns_empty():
    question = Question(title='q1')
    question.add_choice('right', True)
    c2 = question.add_choice('wrong', False)
    result = question.correct_selected_choices([c2.id])
    assert result == []


def test_choices_get_sequential_ids():
    question = Question(title='q8273')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')
    ids = [c.id for c in question.choices]
    assert ids == [1, 2, 3]


def test_exceeding_max_selections_raises():
    question = Question(title='q11111', max_selections=1)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', True)
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])


def test_choice_with_empty_text_raises():
    question = Question(title='q')
    with pytest.raises(Exception):
        question.add_choice('')


def test_choice_with_text_exceeding_limit_raises():
    question = Question(title='q6')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)

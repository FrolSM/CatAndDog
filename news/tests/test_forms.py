import pytest
from news.forms import PostForm, CommentForm

@pytest.mark.django_db
def test_post_form_valid(category):
    form = PostForm(data={
        'title': 'Form title',
        'text': 'Form text',
        'category': category.id,
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_comment_form_valid():
    form = CommentForm(data={'text': 'Nice!'})
    assert form.is_valid()
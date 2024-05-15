from msiaLex import modifier,emoticon

def test_negation():
    assert modifier.negation('zh')

def test_intensifier():
    assert modifier.intensifier('zsm')
    
# def test_disjunction():
#     assert modifier.disjunction('en')

def test_stopword():
    assert modifier.stopword('en')

def test_stopword():
    assert modifier.stopword('zh')

def test_emoticon():
    assert emoticon.get_emoji_sentiment_rank('👍')
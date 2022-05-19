import ngram


def test_check():
    n = ngram.Nonogram('../ngrams/tiny.npy')
    assert not n.check()

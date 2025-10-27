from src.i18n_scanner import extract_keys_from_text
def test_extract():
    s = "t('home.title') and data-i18n=\"about.description\" and __('auth.login')"
    keys = extract_keys_from_text(s)
    assert 'home.title' in keys
    assert 'about.description' in keys
    assert 'auth.login' in keys

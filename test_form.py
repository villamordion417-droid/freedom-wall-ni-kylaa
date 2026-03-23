from freedom.forms import VentForm

def test(data):
    f = VentForm(data)
    print('input:', data)
    print('valid:', f.is_valid())
    print('errors:', f.errors)
    print('cleaned:', getattr(f, 'cleaned_data', None))


if __name__ == '__main__':
    test({'text': "I'm sad and tired", 'emotion': ''})
    test({'text': "sad I'm tired", 'emotion': ''})
    test({'text': "I am anxious and worried", 'emotion': ''})
    test({'text': "Hello, I feel strange", 'emotion': ''})
    test({'text': "I'm excited!", 'emotion': ''})
    test({'text': "", 'emotion': ''})
    test({'text': "I'm Happy", 'emotion': 'happy'})

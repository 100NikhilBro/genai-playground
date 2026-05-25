import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o');

# Vocab Size - The total number of tokens 

print("Vocab Size" , encoder.n_vocab)


# Text to Token

text = "The cat sat on the mat"
tokens = encoder.encode(text)
print("Tokens:", tokens)

# Token to Text

decode = encoder.decode(tokens)
print("Text :",decode)


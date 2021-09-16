dormitorios = "4+"
baños = "3"
print(dormitorios+baños)
dormitorios = int(s for s in dormitorios.split() if s.isdigit())
baños = int(s for s in baños.split() if s.isdigit())
print(dormitorios+baños)
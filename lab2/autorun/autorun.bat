GOTO EndComment
Para agregar codigos a correr agregan la cantidad de lineas:
python automain.py dataset model continuous measure validation

dataset = 1..2
model = 1..2
continuous = 1..3
measure = 1..3
validation = 1..2
:EndComment

python automain.py 2 1 3 1 1
python automain.py 2 1 3 2 1
python automain.py 2 1 3 3 1
python automain.py 2 1 2 1 1
python automain.py 2 1 2 2 1
python automain.py 2 1 2 3 1
python automain.py 2 1 1 1 1
python automain.py 2 1 1 2 1
python automain.py 2 1 1 3 1
pause
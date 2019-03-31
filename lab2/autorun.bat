GOTO EndComment
Para agregar codigos a correr agregan la cantidad de lineas:
python automain.py dataset model continuous measure validation

dataset = 1..2
model = 1..2
continuous = 1..3
measure = 1..3
validation = 1..2
:EndComment

python automain.py 1 1 1 1 1
python automain.py 1 1 1 1 2
pause
MONEY = [0, 50, 100]

N_QUEST = len(MONEY) - 1
Q, H, S = [0]*N_QUEST, [0]*N_QUEST, [0]*N_QUEST
N = 0
Q[N] = str(N+1) + ' - Qual o maior animal do mundo?'
H[N] = {'A': 'A - leao', 'B': 'B - baleia azul',
        'C': 'C - elefante', 'D': 'D - girafa'}
S[N] = 'B'  # solution

N = 1
Q[N] = str(N+1) + ' Qual o maior mamifero do terrestre?'
H[N] = {'A': 'A - rato', 'B': 'B - baleia azul',
        'C': 'C - elefante', 'D': 'D - girafa'}
S[N] = 'C'  # solution

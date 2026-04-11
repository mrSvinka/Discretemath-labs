import itertools


# Таблица истинности 1
def truth_table_check(vars, left_expr, right_expr, desc):
    print(f"\n{desc}")
    print(" ".join(vars) + " | L | R | =")
    for vals in itertools.product([0, 1], repeat=len(vars)):
        d = dict(zip(vars, vals))
        L, R = left_expr(d), right_expr(d)
        print(" ".join(map(str, vals)), f"| {int(L)} | {int(R)} | {int(L==R)}")
    all_equal = all(left_expr(d) == right_expr(d) # Проверка полного равенства
                    for d in (dict(zip(vars, v))
                              for v in itertools.product([0, 1], repeat=len(vars))))
    print("Равенство верно." if all_equal else "Равенство неверно.")

truth_table_check(['a', 'b'],
                  lambda d: d['b'] or (d['a'] and not d['b']),
                  lambda d: d['a'] or d['b'],
                  r"1) B ∪ (A\B) = A ∪ B")

truth_table_check(['a', 'b', 'c'],
                  lambda d: d['a'] and not (d['b'] or d['c']),
                  lambda d: (d['a'] and not d['b']) and not d['c'],
                  r"2) A \ (B ∪ C) = (A \ B) \ C")


# Отношение эквивалентности 2
print("\n=== 2. Отношение на N: x~y ⇔ (x=1∧y=1) ∨ (x≠1∧y≠1) ===")
print(r"Классы: [1] = {1} (конечен), [2] = N\{1} (бесконечен)")


# Отношение 3
M = list(range(-4, 5))
R = [(x, y) for y in M if (x := abs(y) + 2) in M]
print(f"\n=== 3. R = {{(x,y) | x = |y|+2}} ===")
print("Пары R:", R)


print("\nМатрица (строки x, столбцы y):") #Матрица
idx = {v: i for i, v in enumerate(M)}
mat = [[0] * 9 for _ in range(9)]
for x, y in R:
    mat[idx[x]][idx[y]] = 1
for i, row in enumerate(mat):
    print(f"{M[i]:2}:", *row)


refl = all((a, a) in R for a in M) #Свойства
symm = all((y, x) in R for x, y in R)
antisym = not any((x, y) in R and (y, x) in R and x != y for x, y in R)
trans = all(not ((a, b) in R and (b, c) in R) or (a, c) in R
            for a in M for b in M for c in M)
print(f"\nРефл: {refl}, Симм: {symm}, Антисимм: {antisym}, Транз: {trans}")


R_inv = [(y, x) for x, y in R] # Замыкания
R_refl = set(R) | {(a, a) for a in M}
R_symm = set(R) | set(R_inv)


R_trans = set(R) # Транзитивное замыкание
while True:
    new = {(a, d) for (a, b) in R_trans for (c, d) in R_trans
           if b == c and (a, d) not in R_trans}
    if not new:
        break
    R_trans |= new


adj = {a: set() for a in M} # R*
for a, b in R_symm:
    adj[a].add(b)
    adj[b].add(a)

visited, comps = set(), []
for v in M:
    if v not in visited:
        stack, comp = [v], set()
        while stack:
            u = stack.pop()
            if u not in comp:
                comp.add(u)
                visited.add(u)
                stack.extend(adj[u] - comp)
        comps.append(comp)

R_star = {(a, b) for comp in comps for a in comp for b in comp}

print(f"R⁻¹: {R_inv}")
print(f"Rʳ: {sorted(R_refl)}")
print(f"Rˢ: {sorted(R_symm)}")
print(f"R⁺: {sorted(R_trans)}")
print(f"R*: {len(R_star)} пар, классы: {[sorted(c) for c in comps]}")
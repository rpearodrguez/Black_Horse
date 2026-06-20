import ast as _ast
import operator as _op
import random
import discord
import BotConfig
import data as D


class _Calculator(discord.ui.View):
    _LAYOUT = [
        [('C',  discord.ButtonStyle.danger,     'C'),
         ('⌫', discord.ButtonStyle.secondary, 'back'),
         ('%',  discord.ButtonStyle.secondary,   '%'),
         ('÷', discord.ButtonStyle.primary,    '/')],
        [('7',  discord.ButtonStyle.secondary,   '7'),
         ('8',  discord.ButtonStyle.secondary,   '8'),
         ('9',  discord.ButtonStyle.secondary,   '9'),
         ('×', discord.ButtonStyle.primary,    '*')],
        [('4',  discord.ButtonStyle.secondary,   '4'),
         ('5',  discord.ButtonStyle.secondary,   '5'),
         ('6',  discord.ButtonStyle.secondary,   '6'),
         ('−', discord.ButtonStyle.primary,    '-')],
        [('1',  discord.ButtonStyle.secondary,   '1'),
         ('2',  discord.ButtonStyle.secondary,   '2'),
         ('3',  discord.ButtonStyle.secondary,   '3'),
         ('+',  discord.ButtonStyle.primary,     '+')],
        [('0',  discord.ButtonStyle.secondary,   '0'),
         ('.',  discord.ButtonStyle.secondary,   '.'),
         ('=',  discord.ButtonStyle.success,     '=')],
    ]

    def __init__(self):
        super().__init__(timeout=300)
        self.expr = ''
        self.just_eval = False
        for row_idx, row in enumerate(self._LAYOUT):
            for label, style, value in row:
                btn = discord.ui.Button(label=label, style=style, row=row_idx)
                btn.callback = self._make_cb(value)
                self.add_item(btn)

    def _make_cb(self, value: str):
        async def cb(interaction: discord.Interaction):
            if value == 'C':
                self.expr = ''
                self.just_eval = False
            elif value == 'back':
                if self.just_eval:
                    self.expr = ''
                    self.just_eval = False
                else:
                    self.expr = self.expr[:-1]
            elif value == '=':
                if self.expr:
                    self.expr = _calc_eval(self.expr)
                    self.just_eval = True
            else:
                is_digit = value in '0123456789.'
                if self.just_eval:
                    if is_digit or self.expr.startswith('Error'):
                        self.expr = value if is_digit else ''
                    else:
                        self.expr += value
                    self.just_eval = False
                else:
                    self.expr += value
            await interaction.response.edit_message(embed=self._build_embed())
        return cb

    def _build_embed(self) -> discord.Embed:
        disp = self.expr.replace('*', '×').replace('/', '÷') or '0'
        is_err = disp.startswith('Error')
        nl = '\n'
        if self.just_eval:
            desc = f'```{nl}{disp}{nl}```' if is_err else f'```{nl}= {disp}{nl}```'
        else:
            preview = _calc_eval(self.expr) if self.expr and not is_err else ''
            if preview and not preview.startswith('Error'):
                desc = f'```{nl}{disp}{nl}= {preview}{nl}```'
            else:
                desc = f'```{nl}{disp}{nl}```'
        return discord.Embed(title='Calculadora', color=0x2F81C7, description=desc)







class _Trivia(discord.ui.View):
    def __init__(self, question: dict, guild_id: int):
        super().__init__(timeout=30)
        self.guild_id = guild_id
        self.question = question
        self.message = None
        answers = question["incorrect"] + [question["correct"]]
        random.shuffle(answers)
        self.answers = answers
        self.correct_idx = answers.index(question["correct"])
        self.answered = False
        for i, ans in enumerate(answers):
            label = f"{chr(65 + i)}. {ans}"
            btn = discord.ui.Button(
                label=label[:80],
                style=discord.ButtonStyle.secondary,
                row=i // 2,
            )
            btn.callback = self._pick(i)
            self.add_item(btn)

    def _pick(self, chosen: int):
        async def cb(interaction: discord.Interaction):
            if self.answered:
                await interaction.response.defer()
                return
            self.answered = True
            for i, child in enumerate(self.children):
                child.disabled = True
                if i == self.correct_idx:
                    child.style = discord.ButtonStyle.success
                elif i == chosen:
                    child.style = discord.ButtonStyle.danger
            ok = chosen == self.correct_idx
            key = "trivia_correcto" if ok else "trivia_incorrecto"
            color = 0x57F287 if ok else 0xE74C3C
            await interaction.response.edit_message(
                embed=self._result_embed(key, color, interaction.user.display_name),
                view=self,
            )
        return cb

    async def on_timeout(self):
        if self.answered or not self.message:
            return
        for i, child in enumerate(self.children):
            child.disabled = True
            if i == self.correct_idx:
                child.style = discord.ButtonStyle.success
        await self.message.edit(
            embed=self._result_embed("trivia_timeout", 0x95A5A6, None),
            view=self,
        )

    def _question_embed(self, lang: str) -> discord.Embed:
        import data as D
        diff_raw = self.question["difficulty"]
        diff = D.TRIVIA_DIFFICULTY.get(diff_raw, {}).get(lang, diff_raw)
        embed = discord.Embed(
            title=f"🧠 {self.question['category']}",
            description=self.question["question"],
            color=0x2F81C7,
        )
        embed.set_footer(text=f"{diff} · 30s")
        return embed

    def _result_embed(self, key: str, color: int, username) -> discord.Embed:
        g = self.guild_id
        title = BotConfig.t(g, key)
        if username:
            title = f"{title} — {username}"
        embed = discord.Embed(
            title=title,
            description=self.question["question"],
            color=color,
        )
        embed.add_field(
            name=BotConfig.t(g, "trivia_respuesta"),
            value=self.question["correct"],
            inline=False,
        )
        return embed





class _RPS(discord.ui.View):
    _BEATS  = {'piedra': 'tijeras', 'tijeras': 'papel', 'papel': 'piedra'}
    _EMOJIS = {'piedra': '🪨', 'papel': '📄', 'tijeras': '✂️'}

    def __init__(self, player_x: discord.Member, player_o, guild_id: int):
        super().__init__(timeout=120)
        self.player_x  = player_x
        self.player_o  = player_o   # None = vs bot
        self.vs_bot    = player_o is None
        self.guild_id  = guild_id
        self.message   = None
        self.choice_x  = None
        self.choice_o  = None
        for choice in ['piedra', 'papel', 'tijeras']:
            btn = discord.ui.Button(
                label=self._EMOJIS[choice],
                style=discord.ButtonStyle.secondary,
                row=0,
            )
            btn.callback = self._pick(choice)
            self.add_item(btn)

    def _pick(self, choice: str):
        async def cb(interaction: discord.Interaction):
            uid = interaction.user.id
            is_x = uid == self.player_x.id
            is_o = not self.vs_bot and self.player_o and uid == self.player_o.id
            if not is_x and not is_o:
                await interaction.response.send_message('No eres parte de este juego.', ephemeral=True)
                return
            if is_x and self.choice_x:
                await interaction.response.send_message('Ya elegiste.', ephemeral=True)
                return
            if is_o and self.choice_o:
                await interaction.response.send_message('Ya elegiste.', ephemeral=True)
                return
            if is_x:
                self.choice_x = choice
            else:
                self.choice_o = choice
            # Vs bot: responde de inmediato
            if self.vs_bot:
                self.choice_o = random.choice(['piedra', 'papel', 'tijeras'])
            if self.choice_x and self.choice_o:
                for child in self.children: child.disabled = True
                await interaction.response.edit_message(embed=self._result_embed(), view=self)
                self.stop()
            else:
                name = self.player_x.display_name if is_x else self.player_o.display_name
                await interaction.response.send_message(
                    f'{self._EMOJIS[choice]} Elegiste **{choice}**. Esperando al otro jugador...', ephemeral=True)
                if self.message:
                    chosen = self.player_x.display_name if self.choice_x else self.player_o.display_name
                    waiting = self.player_o.display_name if self.choice_x else self.player_x.display_name
                    try:
                        await self.message.edit(embed=discord.Embed(
                            title='🪨📄✂️ Piedra Papel Tijeras',
                            description=f'✅ {chosen} ya eligió.\n⏳ Esperando a {waiting}...',
                            color=0xF39C12))
                    except Exception: pass
        return cb

    def _result_embed(self) -> discord.Embed:
        cx, co = self.choice_x, self.choice_o
        ex, eo = self._EMOJIS[cx], self._EMOJIS[co]
        name_x = self.player_x.display_name
        name_o = '🤖 Bot' if self.vs_bot else self.player_o.display_name
        if cx == co:
            result = '🤝 ¡Empate!'
            color  = 0x95A5A6
        elif self._BEATS[cx] == co:
            result = f'🏆 ¡Gana {name_x}!'
            color  = 0x57F287
        else:
            result = f'🏆 ¡Gana {name_o}!'
            color  = 0xE74C3C
        embed = discord.Embed(title='🪨📄✂️ Piedra Papel Tijeras', description=result, color=color)
        embed.add_field(name=name_x, value=f'{ex} {cx}', inline=True)
        embed.add_field(name=name_o, value=f'{eo} {co}', inline=True)
        return embed

    async def on_timeout(self):
        if not self.message: return
        for child in self.children: child.disabled = True
        try: await self.message.edit(view=self)
        except Exception: pass


class _Minesweeper(discord.ui.View):
    _S     = 5
    _MINES = 5

    def __init__(self, guild_id: int, player_id: int):
        super().__init__(timeout=600)
        self.guild_id   = guild_id
        self.player_id  = player_id
        self.message    = None
        self.mines: set = set()
        self.revealed   = [[False]*self._S for _ in range(self._S)]
        self.adj        = [[0]*self._S for _ in range(self._S)]
        self.first      = True
        self.over       = False
        self.won        = False
        for i in range(self._S * self._S):
            r, c = divmod(i, self._S)
            btn = discord.ui.Button(label='■', style=discord.ButtonStyle.secondary, row=r)
            btn.callback = self._click(r, c)
            self.add_item(btn)

    def _gen(self, sr: int, sc: int):
        safe = {(sr+dr, sc+dc) for dr in range(-1,2) for dc in range(-1,2)
                if 0 <= sr+dr < self._S and 0 <= sc+dc < self._S}
        pool = [(r,c) for r in range(self._S) for c in range(self._S) if (r,c) not in safe]
        self.mines = set(map(tuple, random.sample(pool, min(self._MINES, len(pool)))))
        for r in range(self._S):
            for c in range(self._S):
                if (r,c) not in self.mines:
                    self.adj[r][c] = sum(
                        1 for dr in range(-1,2) for dc in range(-1,2)
                        if (dr,dc)!=(0,0) and (r+dr,c+dc) in self.mines
                    )

    def _flood(self, r: int, c: int):
        if not (0<=r<self._S and 0<=c<self._S): return
        if self.revealed[r][c] or (r,c) in self.mines: return
        self.revealed[r][c] = True
        btn = self.children[r*self._S + c]
        btn.disabled = True
        n = self.adj[r][c]
        if n == 0:
            btn.label = '·'
            btn.style = discord.ButtonStyle.success
            for dr in range(-1,2):
                for dc in range(-1,2):
                    if (dr,dc) != (0,0): self._flood(r+dr, c+dc)
        else:
            btn.label = str(n)
            btn.style = discord.ButtonStyle.primary

    def _click(self, r: int, c: int):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.player_id:
                await interaction.response.send_message('No eres el jugador.', ephemeral=True)
                return
            if self.over or self.revealed[r][c]:
                await interaction.response.defer(); return
            if self.first:
                self._gen(r, c); self.first = False
            if (r,c) in self.mines:
                self.over = True
                for mr,mc in self.mines:
                    b = self.children[mr*self._S+mc]
                    b.label = '💣'; b.style = discord.ButtonStyle.danger; b.disabled = True
                for child in self.children: child.disabled = True
            else:
                self._flood(r, c)
                safe = self._S*self._S - len(self.mines)
                done = sum(self.revealed[i][j] for i in range(self._S) for j in range(self._S))
                if done >= safe:
                    self.won = self.over = True
                    for child in self.children: child.disabled = True
            await interaction.response.edit_message(embed=self._build_embed(), view=self)
        return cb

    def _build_embed(self) -> discord.Embed:
        if self.won:
            title, color = '🏆 ¡Campo despejado!', 0x57F287
        elif self.over:
            title, color = '💥 ¡Pisaste una mina!', 0xE74C3C
        else:
            done = sum(self.revealed[i][j] for i in range(self._S) for j in range(self._S))
            left = self._S*self._S - len(self.mines) - done
            title, color = f'💣 Buscaminas — {left} celdas restantes', 0x2F81C7
        embed = discord.Embed(title=title, color=color)
        if not self.over:
            embed.set_footer(text=f'💣 {self._MINES} minas  ·  Cuadrícula {self._S}×{self._S}')
        return embed

    async def on_timeout(self):
        if not self.message: return
        for child in self.children: child.disabled = True
        try: await self.message.edit(view=self)
        except Exception: pass


class _Hangman(discord.ui.View):
    _STAGES = [
        "  +---+\n  |   |\n  |\n  |\n  |\n  ====",
        "  +---+\n  |   |\n  |   O\n  |\n  |\n  ====",
        "  +---+\n  |   |\n  |   O\n  |   |\n  |\n  ====",
        "  +---+\n  |   |\n  |   O\n  |  /|\n  |\n  ====",
        "  +---+\n  |   |\n  |   O\n  |  /|\\\n  |\n  ====",
        "  +---+\n  |   |\n  |   O\n  |  /|\\\n  |  /\n  ====",
        "  +---+\n  |   |\n  |   O\n  |  /|\\\n  |  / \\\n  ====",
    ]
    _ROWS = [
        ['A','B','C','D','E'],
        ['F','G','H','I','J'],
        ['L','M','N','Ñ','O'],
        ['P','Q','R','S','T'],
        ['U','V','X','Y','Z'],
    ]

    def __init__(self, guild_id: int):
        super().__init__(timeout=300)
        self.guild_id = guild_id
        self.word = random.choice(D.HANGMAN_WORDS).upper()
        self.guessed: set = set()
        self.wrongs = 0
        self.over = False
        for row_idx, row in enumerate(self._ROWS):
            for letter in row:
                btn = discord.ui.Button(label=letter, style=discord.ButtonStyle.secondary, row=row_idx)
                btn.callback = self._guess(letter)
                self.add_item(btn)

    def _guess(self, letter: str):
        async def cb(interaction: discord.Interaction):
            if self.over:
                await interaction.response.defer()
                return
            correct = letter in self.word
            for child in self.children:
                if child.label == letter:
                    child.disabled = True
                    child.style = discord.ButtonStyle.success if correct else discord.ButtonStyle.danger
                    break
            self.guessed.add(letter)
            if not correct:
                self.wrongs += 1
            word_letters = {c for c in self.word if c.isalpha()}
            if word_letters <= self.guessed or self.wrongs >= 6:
                self.over = True
                for child in self.children: child.disabled = True
            await interaction.response.edit_message(embed=self._build_embed(), view=self)
        return cb

    def _display_word(self) -> str:
        return ' '.join(c if (c in self.guessed or not c.isalpha()) else '_' for c in self.word)

    def _build_embed(self) -> discord.Embed:
        art = self._STAGES[min(self.wrongs, 6)]
        won = self.over and self.wrongs < 6
        lost = self.wrongs >= 6
        title = '🏆 ¡Adivinaste!' if won else ('💀 Perdiste' if lost else '🪢 Ahorcado')
        color = 0x57F287 if won else (0xE74C3C if lost else 0x2F81C7)
        word_line = self._display_word()
        if lost:
            word_line += f'\n\nEra: **{self.word}**'
        desc = f'```\n{art}\n```\n**{word_line}**'
        embed = discord.Embed(title=title, description=desc, color=color)
        wrong = ' '.join(sorted(l for l in self.guessed if l not in self.word))
        footer = f'Incorrectas: {wrong}  ({self.wrongs}/6)' if wrong else 'Adivina la palabra letra por letra'
        embed.set_footer(text=footer)
        return embed


class _Snake(discord.ui.View):
    _W, _H = 8, 8
    _EMPTY, _HEAD, _BODY, _FOOD = '⬛', '🟢', '🟩', '🍎'

    def __init__(self, guild_id: int, player_id: int):
        super().__init__(timeout=300)
        self.guild_id = guild_id
        self.player_id = player_id
        self.message = None
        cx, cy = self._W // 2, self._H // 2
        self.snake = [(cy, cx), (cy, cx-1), (cy, cx-2)]
        self.direction = (0, 1)
        self.score = 0
        self.over = False
        self._spawn_food()
        up    = discord.ui.Button(label='↑', style=discord.ButtonStyle.primary,   row=0)
        left  = discord.ui.Button(label='←', style=discord.ButtonStyle.secondary, row=1)
        down  = discord.ui.Button(label='↓', style=discord.ButtonStyle.secondary, row=1)
        right = discord.ui.Button(label='→', style=discord.ButtonStyle.secondary, row=1)
        up.callback    = self._turn(-1,  0)
        left.callback  = self._turn( 0, -1)
        down.callback  = self._turn( 1,  0)
        right.callback = self._turn( 0,  1)
        for b in [up, left, down, right]: self.add_item(b)

    def _spawn_food(self):
        occupied = set(self.snake)
        empty = [(r, c) for r in range(self._H) for c in range(self._W) if (r, c) not in occupied]
        if empty:
            self.food = random.choice(empty)

    def _turn(self, dr: int, dc: int):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.player_id:
                await interaction.response.send_message('No eres el jugador.', ephemeral=True)
                return
            if self.over:
                await interaction.response.defer(); return
            old_dr, old_dc = self.direction
            if (dr, dc) != (-old_dr, -old_dc):
                self.direction = (dr, dc)
            dr2, dc2 = self.direction
            hr, hc = self.snake[0]
            nr, nc = hr + dr2, hc + dc2
            if not (0 <= nr < self._H and 0 <= nc < self._W) or (nr, nc) in set(self.snake[:-1]):
                self.over = True
                for child in self.children: child.disabled = True
                await interaction.response.edit_message(embed=self._build_embed(), view=self)
                return
            self.snake.insert(0, (nr, nc))
            if (nr, nc) == self.food:
                self.score += 1
                self._spawn_food()
            else:
                self.snake.pop()
            await interaction.response.edit_message(embed=self._build_embed(), view=self)
        return cb

    def _build_embed(self) -> discord.Embed:
        snake_set = set(self.snake)
        rows = []
        for r in range(self._H):
            row = ''
            for c in range(self._W):
                if (r, c) == self.snake[0]:      row += self._HEAD
                elif (r, c) in snake_set:        row += self._BODY
                elif (r, c) == self.food:        row += self._FOOD
                else:                            row += self._EMPTY
            rows.append(row)
        board = '\n'.join(rows)
        title = '💀 Game Over' if self.over else '🐍 Snake'
        color = 0xE74C3C if self.over else 0x57F287
        embed = discord.Embed(title=title, description=board, color=color)
        embed.set_footer(text=f'Score: {self.score}  |  Longitud: {len(self.snake)}')
        return embed

    async def on_timeout(self):
        if not self.message: return
        for child in self.children: child.disabled = True
        try: await self.message.edit(view=self)
        except Exception: pass


class _Game2048(discord.ui.View):
    def __init__(self, guild_id: int, player_id: int):
        super().__init__(timeout=600)
        self.guild_id  = guild_id
        self.player_id = player_id
        self.message   = None
        self.board     = [[0]*4 for _ in range(4)]
        self.score     = 0
        self.over      = False
        self.won       = False
        self._spawn(); self._spawn()
        up    = discord.ui.Button(label='↑', style=discord.ButtonStyle.primary,   row=0)
        left  = discord.ui.Button(label='←', style=discord.ButtonStyle.secondary, row=1)
        down  = discord.ui.Button(label='↓', style=discord.ButtonStyle.secondary, row=1)
        right = discord.ui.Button(label='→', style=discord.ButtonStyle.secondary, row=1)
        up.callback    = self._slide('up')
        left.callback  = self._slide('left')
        down.callback  = self._slide('down')
        right.callback = self._slide('right')
        for b in [up, left, down, right]: self.add_item(b)

    def _spawn(self):
        empty = [(r,c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            self.board[r][c] = 4 if random.random() < 0.1 else 2

    def _merge_row(self, row: list):
        tiles = [x for x in row if x != 0]
        result, gain, i = [], 0, 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i+1]:
                v = tiles[i] * 2
                result.append(v); gain += v; i += 2
            else:
                result.append(tiles[i]); i += 1
        result += [0] * (4 - len(result))
        return result, gain

    def _apply(self, direction: str) -> bool:
        old = [r[:] for r in self.board]
        gain = 0
        if direction == 'left':
            for r in range(4):
                self.board[r], g = self._merge_row(self.board[r]); gain += g
        elif direction == 'right':
            for r in range(4):
                rev, g = self._merge_row(self.board[r][::-1])
                self.board[r] = rev[::-1]; gain += g
        elif direction == 'up':
            for c in range(4):
                col, g = self._merge_row([self.board[r][c] for r in range(4)])
                for r in range(4): self.board[r][c] = col[r]
                gain += g
        elif direction == 'down':
            for c in range(4):
                col, g = self._merge_row([self.board[r][c] for r in range(4)][::-1])
                col = col[::-1]
                for r in range(4): self.board[r][c] = col[r]
                gain += g
        self.score += gain
        return any(self.board[r] != old[r] for r in range(4))

    def _has_moves(self) -> bool:
        for r in range(4):
            for c in range(4):
                if self.board[r][c] == 0: return True
                if c < 3 and self.board[r][c] == self.board[r][c+1]: return True
                if r < 3 and self.board[r][c] == self.board[r+1][c]: return True
        return False

    def _slide(self, direction: str):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.player_id:
                await interaction.response.send_message('No eres el jugador.', ephemeral=True)
                return
            if self.over:
                await interaction.response.defer(); return
            if self._apply(direction):
                if any(self.board[r][c] == 2048 for r in range(4) for c in range(4)):
                    self.won = self.over = True
                    for child in self.children: child.disabled = True
                else:
                    self._spawn()
                    if not self._has_moves():
                        self.over = True
                        for child in self.children: child.disabled = True
            await interaction.response.edit_message(embed=self._build_embed(), view=self)
        return cb

    def _build_embed(self) -> discord.Embed:
        sep = '+----+----+----+----+'
        lines = [sep]
        for row in self.board:
            cells = '|'.join(f'{v:4}' if v else '    ' for v in row)
            lines.append(f'|{cells}|')
            lines.append(sep)
        board_str = '\n'.join(lines)
        title = '🏆 ¡2048!' if self.won else ('💀 Game Over' if self.over else '🎮 2048')
        color = 0xF1C40F if self.won else (0xE74C3C if self.over else 0xF39C12)
        embed = discord.Embed(title=title, description=f'```\n{board_str}\n```', color=color)
        embed.set_footer(text=f'Score: {self.score}')
        return embed

    async def on_timeout(self):
        if not self.message: return
        for child in self.children: child.disabled = True
        try: await self.message.edit(view=self)
        except Exception: pass


class _Dungeon(discord.ui.View):
    _S = 9  # grid NxN

    _SPAWNS = [
        [('👺', 'Goblin', 4, 1)] * 3,
        [('👺', 'Goblin', 4, 1), ('👹', 'Orc', 8, 2), ('👹', 'Orc', 8, 2)],
        [('👹', 'Orc', 8, 2), ('👾', 'Troll', 15, 3), ('👾', 'Troll', 15, 3)],
    ]

    def __init__(self, guild_id: int, player_id: int):
        super().__init__(timeout=600)
        self.guild_id  = guild_id
        self.player_id = player_id
        self.level     = 1
        self.hp        = 15
        self.max_hp    = 15
        self.atk       = 3
        self.message   = None
        self.log       = ''
        self._new_level()
        up    = discord.ui.Button(label='↑', style=discord.ButtonStyle.primary,   row=0)
        left  = discord.ui.Button(label='←', style=discord.ButtonStyle.secondary, row=1)
        down  = discord.ui.Button(label='↓', style=discord.ButtonStyle.secondary, row=1)
        right = discord.ui.Button(label='→', style=discord.ButtonStyle.secondary, row=1)
        up.callback    = self._move(-1,  0)
        left.callback  = self._move( 0, -1)
        down.callback  = self._move( 1,  0)
        right.callback = self._move( 0,  1)
        for b in [up, left, down, right]:
            self.add_item(b)

    def _new_level(self):
        self.grid, rooms = self._gen_map()
        self.enemies: dict = {}
        self.items:   dict = {}
        self.py, self.px = rooms[0]
        self.stairs = rooms[-1]
        floor = [
            (r, c) for r in range(self._S) for c in range(self._S)
            if self.grid[r][c] == 'F'
            and (r, c) != (self.py, self.px)
            and (r, c) != self.stairs
        ]
        random.shuffle(floor)
        spawns = self._SPAWNS[self.level - 1]
        for i, (emoji, name, hp_b, atk_b) in enumerate(spawns):
            if i < len(floor):
                r, c = floor[i]
                self.enemies[(r, c)] = {
                    'hp': max(1, hp_b + random.randint(-1, 1)),
                    'atk': atk_b, 'emoji': emoji, 'name': name,
                }
        for i in range(len(spawns), len(spawns) + 2):
            if i < len(floor):
                r, c = floor[i]
                self.items[(r, c)] = 'hp' if i % 2 == 0 else 'sw'

    def _gen_map(self):
        N = self._S
        g = [['W'] * N for _ in range(N)]
        defs = [(1,1,3,3), (1,5,3,3), (5,1,3,3), (5,5,3,3)]
        chosen = random.sample(defs, 3)
        centers = []
        for ry, rx, rh, rw in chosen:
            for r in range(ry, ry + rh):
                for c in range(rx, rx + rw):
                    g[r][c] = 'F'
            centers.append((ry + rh // 2, rx + rw // 2))
        for i in range(len(centers) - 1):
            r1, c1 = centers[i]
            r2, c2 = centers[i + 1]
            r, c = r1, c1
            while c != c2:
                g[r][c] = 'F'
                c += 1 if c2 > c else -1
            while r != r2:
                g[r][c] = 'F'
                r += 1 if r2 > r else -1
        return g, centers

    def _cell(self, r, c) -> str:
        if r == self.py and c == self.px: return '🧙'
        if (r, c) in self.enemies:        return self.enemies[(r, c)]['emoji']
        if (r, c) in self.items:          return '❤️' if self.items[(r, c)] == 'hp' else '⚔️'
        if (r, c) == self.stairs:         return '🔽'
        return '🧱' if self.grid[r][c] == 'W' else '⬜'

    def _build_embed(self) -> discord.Embed:
        board = '\n'.join(''.join(self._cell(r, c) for c in range(self._S)) for r in range(self._S))
        n_enem = len(self.enemies)
        status = f'❤️ {self.hp}/{self.max_hp}  ⚔️ {self.atk}  👾 {n_enem} enemigo{"s" if n_enem != 1 else ""}'
        if n_enem == 0:
            status += '  ·  🔽 Escaleras libres'
        embed = discord.Embed(
            title=f'🏰 Dungeon — Nivel {self.level}/3',
            description=board,
            color=0x2C2F33,
        )
        embed.add_field(name='Estado', value=status, inline=False)
        if self.log:
            embed.set_footer(text=self.log)
        return embed

    def _move(self, dr: int, dc: int):
        async def cb(interaction: discord.Interaction):
            if interaction.user.id != self.player_id:
                await interaction.response.send_message('No eres el jugador.', ephemeral=True)
                return
            nr, nc = self.py + dr, self.px + dc
            if not (0 <= nr < self._S and 0 <= nc < self._S) or self.grid[nr][nc] == 'W':
                self.log = '🧱 Hay una pared.'
                await interaction.response.edit_message(embed=self._build_embed(), view=self)
                return
            if (nr, nc) in self.enemies:
                e = self.enemies[(nr, nc)]
                e['hp'] -= self.atk
                dmg = max(0, e['atk'] - random.randint(0, 1))
                self.hp -= dmg
                if e['hp'] <= 0:
                    del self.enemies[(nr, nc)]
                    self.log = f'⚔️ Mataste al {e["name"]}! Recibiste {dmg} de daño.'
                else:
                    self.log = f'⚔️ Atacas al {e["name"]} (−{self.atk} HP). Recibes {dmg} daño.'
                if self.hp <= 0:
                    await self._end(interaction, won=False)
                    return
                await interaction.response.edit_message(embed=self._build_embed(), view=self)
                return
            self.py, self.px = nr, nc
            if (nr, nc) in self.items:
                item = self.items.pop((nr, nc))
                if item == 'hp':
                    gain = 5
                    self.hp = min(self.max_hp, self.hp + gain)
                    self.log = f'❤️ Poción recogida. +{gain} HP'
                else:
                    self.atk += 1
                    self.log = '⚔️ Espada recogida. ATK +1'
            elif (nr, nc) == self.stairs:
                if self.enemies:
                    self.py, self.px = self.py - dr, self.px - dc
                    self.log = '⚠️ Derrota a todos los enemigos primero.'
                elif self.level >= 3:
                    await self._end(interaction, won=True)
                    return
                else:
                    self.level += 1
                    self.hp = min(self.max_hp, self.hp + 5)
                    self.log = f'🔽 Bajaste al nivel {self.level}. +5 HP'
                    self._new_level()
            else:
                self.log = ''
            await interaction.response.edit_message(embed=self._build_embed(), view=self)
        return cb

    async def _end(self, interaction: discord.Interaction, won: bool):
        for child in self.children:
            child.disabled = True
        if won:
            embed = discord.Embed(title='🏆 ¡Victoria!', description='Conquistaste el dungeon.', color=0x57F287)
            embed.add_field(name='HP', value=f'{self.hp}/{self.max_hp}', inline=True)
            embed.add_field(name='ATK', value=str(self.atk), inline=True)
        else:
            board = '\n'.join(''.join(self._cell(r, c) for c in range(self._S)) for r in range(self._S))
            embed = discord.Embed(title='💀 Game Over', description=board, color=0xE74C3C)
            embed.set_footer(text=f'Llegaste al nivel {self.level}')
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

    async def on_timeout(self):
        if not self.message:
            return
        for child in self.children:
            child.disabled = True
        try:
            await self.message.edit(view=self)
        except Exception:
            pass

class _TicTacToe(discord.ui.View):
    _WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def __init__(self, player_x: discord.Member, player_o, guild_id: int):
        # player_o: discord.Member para PvP, None para vs bot
        super().__init__(timeout=300)
        self.board     = [None] * 9
        self.player_x  = player_x
        self.player_o  = player_o
        self.vs_bot    = player_o is None
        self.guild_id  = guild_id
        self.current   = 'X'
        self.winner    = None   # 'X', 'O', o None
        self.game_over = False
        for i in range(9):
            btn = discord.ui.Button(label='　', style=discord.ButtonStyle.secondary, row=i // 3)
            btn.callback = self._move(i)
            self.add_item(btn)

    def _name(self, sym: str) -> str:
        if sym == 'X':
            return self.player_x.display_name
        return '🤖 Bot' if self.vs_bot else self.player_o.display_name

    def _apply_move(self, cell: int, sym: str):
        self.board[cell] = sym
        btn = self.children[cell]
        btn.label = sym
        btn.style = discord.ButtonStyle.primary if sym == 'X' else discord.ButtonStyle.danger
        btn.disabled = True

    def _finish(self, sym: str, wcells: list):
        for wc in wcells:
            self.children[wc].style = discord.ButtonStyle.success
        self.winner    = sym
        self.game_over = True
        for child in self.children: child.disabled = True

    def _move(self, cell: int):
        async def cb(interaction: discord.Interaction):
            expected_id = self.player_x.id if (self.vs_bot or self.current == 'X')                           else self.player_o.id
            if interaction.user.id != expected_id:
                await interaction.response.send_message(
                    BotConfig.t(self.guild_id, 'gato_no_turno'), ephemeral=True)
                return
            if self.board[cell] is not None:
                await interaction.response.send_message(
                    BotConfig.t(self.guild_id, 'gato_ocupada'), ephemeral=True)
                return
            self._apply_move(cell, self.current)
            sym, wcells = self._check_winner()
            if sym:
                self._finish(sym, wcells)
            elif None not in self.board:
                self.game_over = True
                for child in self.children: child.disabled = True
            else:
                self.current = 'O' if self.current == 'X' else 'X'
                if self.vs_bot and self.current == 'O':
                    bot_cell = self._best_move()
                    self._apply_move(bot_cell, 'O')
                    sym, wcells = self._check_winner()
                    if sym:
                        self._finish(sym, wcells)
                    elif None not in self.board:
                        self.game_over = True
                        for child in self.children: child.disabled = True
                    else:
                        self.current = 'X'
            await interaction.response.edit_message(embed=self._build_embed(), view=self)
        return cb

    def _check_winner(self):
        for combo in self._WINS:
            a, b, c = combo
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], list(combo)
        return None, []

    @staticmethod
    def _minimax(board: list, is_bot: bool) -> int:
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in wins:
            if board[a] and board[a] == board[b] == board[c]:
                return 1 if board[a] == 'O' else -1
        if None not in board:
            return 0
        if is_bot:
            best = -2
            for i in range(9):
                if board[i] is None:
                    board[i] = 'O'
                    best = max(best, _TicTacToe._minimax(board, False))
                    board[i] = None
            return best
        best = 2
        for i in range(9):
            if board[i] is None:
                board[i] = 'X'
                best = min(best, _TicTacToe._minimax(board, True))
                board[i] = None
        return best

    def _best_move(self) -> int:
        best_score, best_cell = -2, -1
        for i in range(9):
            if self.board[i] is None:
                self.board[i] = 'O'
                score = self._minimax(self.board, False)
                self.board[i] = None
                if score > best_score:
                    best_score, best_cell = score, i
        return best_cell

    def _build_embed(self) -> discord.Embed:
        g = self.guild_id
        if self.game_over:
            if self.winner:
                title = BotConfig.t(g, 'gato_gana', user=self._name(self.winner))
                color = 0x57F287
            else:
                title = BotConfig.t(g, 'gato_empate')
                color = 0x95A5A6
        else:
            sym_icon = '❌' if self.current == 'X' else '⭕'
            title = BotConfig.t(g, 'gato_turno', sym=sym_icon, user=self._name(self.current))
            color = 0x3498DB if self.current == 'X' else 0xE74C3C
        embed = discord.Embed(
            title=BotConfig.t(g, 'gato_titulo'),
            description=title,
            color=color,
        )
        embed.add_field(name='❌', value=self._name('X'), inline=True)
        embed.add_field(name='⭕', value=self._name('O'), inline=True)
        return embed



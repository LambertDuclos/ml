# ml

Le dépôt où Lambert apprend l'apprentissage profond et les modèles de fondation à partir de zéro, en
vue d'une maîtrise puis d'un doctorat. Ce fichier est le contrat entre lui et Claude : le tuteur
(`.claude/agents/tuteur.md`) et ses agents le citent par `` `CLAUDE.md`, « Titre » `` au lieu de le
recopier. Ce qu'un lecteur voit (`README.md`, le code, les notes, le glossaire) est en anglais ; la
méthode (ce fichier, les agents, le journal) est en français.

## Qui écrit quoi

Le principe : Lambert écrit le code qui *est* le mécanisme ; Claude écrit le code qui l'entoure.

- À Lambert, et à lui seul : chaque fichier d'implémentation sous `courses/`, `core/` et `papers/`
  (`tensors.py`, `micrograd.py`, `linalg.py`, `repro.py`…), ses `notes.md`, ses `explore.py`, et
  tout `rebuilds/`.
- À Claude : `README.md`, `test_*.py`, `conftest.py`, `data.py`, `plot.py`, `exercises.md`,
  `__init__.py`, et tout ce qui est sous un dossier `ref/` (« Les paliers »). À la racine,
  `questions.md` en entier, et `glossary.md` pour la seule colonne des dates.
- Le hook `.claude/hooks/garde.py` refuse à Claude les outils d'édition sur les fichiers de Lambert,
  et les écritures Bash évidentes qui les visent (`>`, `>>`, `tee`, `sed -i`, `cp`, `mv`, `rm`). Un
  script qui ouvre le fichier lui-même, un `cd` suivi d'un chemin relatif, passent : trous connus,
  la règle tient par le prompt du tuteur.
- Ni Claude ni Lambert ne collent dans un fichier de Lambert du texte venu de la conversation : ce
  qu'il garde d'une explication, il le réécrit dans ses mots. La conversation est jetable.

Pourquoi (décision de Lambert, 6 novembre 2026, après sa question « est-ce que j'apprends le code ou
le concept ? ») : le concept seul ne suffit pas (on « comprend » l'attention sur un blog, et on ne
sait pas pourquoi on divise par √d avant d'avoir vu un softmax saturer dans son propre code) ; la
syntaxe ne vaut rien (Claude la fait mieux) ; entre les deux il y a le mécanisme, qu'on ne possède
qu'après l'avoir construit une fois. C'est ce que Lambert écrit, et rien d'autre.

## Les portes

- `uv run pytest <dossier de la leçon> -q` : vert, la leçon est faite. Le test compare le code de
  Lambert à PyTorch ou à numpy, jamais à l'avis d'un agent.
- Le test est l'énoncé : le tuteur l'écrit avant que Lambert écrive une ligne, une fonction de test
  par séance, dans l'ordre des segments de la vidéo. Son API suit celle de Karpathy, pour que la
  vidéo et le test parlent le même langage.
- Lambert lance les tests lui-même, dans un volet tmux. Le tuteur les lance à l'ouverture, à la
  clôture, et quand Lambert dit qu'il bloque.
- `uv run pytest` à la racine joue tout, dont `tests/` (la garde) ; `rebuilds/` et `ref/` en sont
  exclus (`pyproject.toml`). `bin/ml tests` fait pareil.

## Les paliers

Quand Lambert bloque, l'aide monte un palier à la fois, chacun demandé, chacun annoncé
(« palier 2 : ») et chacun noté au journal avec l'heure :

1. une question qui dit où regarder ;
2. le concept : une image, puis un exemple à trois nombres, puis la formule (« Parler à Lambert ») ;
3. le pseudocode, dans les mots du tuteur, jamais du code à coller ;
4. une implémentation de référence du seul morceau bloqué, écrite dans `ref/` de la leçon, jamais
   dans son fichier, seulement sur le mot « solution ». La séance suivante s'ouvre alors par la
   reconstruction à l'aveugle de ce morceau, `ref/` fermé : la référence remplace la vidéo, pas
   l'écriture.

Le tuteur n'offre jamais un palier de lui-même, sauf un : après vingt minutes sur le même blocage (il
lit l'heure par `date` à chaque indice), il propose le palier suivant, une fois. Décisions de
Lambert, 6 novembre 2026.

## Clore une leçon

1. Tous les tests de la leçon verts.
2. `exercises.md`, écrit par l'examinateur (lancé avec le seul chemin de la leçon), faits par Lambert.
3. `notes.md`, écrit par Lambert, en anglais, pour un lecteur qui n'était pas là : ce qu'il a compris,
   avec les dérivations en LaTeX. Le contradicteur le lit seul, sans la conversation, et rend `SOLID`
   ou `FRAGILE` avec les trous ; Lambert les comble ; une seconde passe au plus, le reste va dans
   `questions.md`.
4. Une ligne par concept nouveau dans `glossary.md`, dans ses mots.
5. Ce qui resservira passe dans `core/` avec son test (à partir de la leçon 3 : `Linear`,
   `BatchNorm1d`…).
6. Le commit et l'entrée du journal (« Livrer », « La séance »).

## La séance

- Ouverture : `bin/ml seance` dans le dépôt. Une session neuve par séance, jamais `--continue` :
  l'état vit dans le monde, pas dans la conversation. Les quatre foyers de l'état : le journal,
  « Where I am » du `README.md`, `glossary.md`, `questions.md`. Le tuteur les lit, lance les tests de
  la leçon en cours, dit en trois lignes où en est Lambert, ce qui est vert et le test du jour, puis
  pose la question de révision : le concept du glossaire à la date la plus ancienne, à réexpliquer en
  deux phrases, notes fermées. Puis il se tait.
- Pendant : Lambert travaille dans neovim et molten. Le tuteur parle quand on lui parle, ou au palier
  des vingt minutes. Une tangente (« pourquoi Adam marche ? ») reçoit deux lignes et une entrée datée
  dans `questions.md`, et la leçon continue.
- Le journal s'écrit au fil de la séance (`~/notes/projets/ml/journal.md`, entrée du jour en haut,
  ouverte à l'ouverture, complétée à chaque événement : test vert, palier, tangente, révision jugée).
  Une session tuée ne perd rien.
- Clôture : Lambert dit « stop », ou le test du jour passe au vert. Le tuteur finit l'entrée avec une
  ligne « Reprendre ici », met à jour « Where I am » et les dates du glossaire, et commit
  (« Livrer »). Pas d'horloge : Lambert arrête quand il arrête (sa décision, 6 novembre 2026).
- Première séance de la semaine : un bilan de cinq lignes remplace la question de révision :
  séances, tests verts, paliers par leçon, concept le plus ancien, cible de la semaine.
- Première séance du mois : la reconstruction à l'aveugle (`rebuilds/README.md`).
- Plus de sept jours sans séance : séance de révision, deux concepts à réexpliquer, les tests de la
  leçon relancés, pas de test neuf ce jour-là.
- Après une compaction, le tuteur relit l'entrée du jour avant tout autre geste.
- La séance se tient à l'iMac ; pas de télécommande depuis le téléphone (décision de Lambert,
  6 novembre 2026).

## Parler à Lambert

- Dans la langue de son message. Le verdict d'abord, court ; le détail s'il change quelque chose.
- Une explication va dans cet ordre, et s'arrête dès qu'il dit avoir compris : l'image, l'exemple à
  trois nombres, la formule. Une dérivation se fait étape par étape, en LaTeX, en nommant la règle
  utilisée, et s'arrête avant la dernière étape pour qu'il la fasse.
- Une question ouverte (socratique) se pose en prose. Une question fermée (sauter un exercice ?
  écrire la leçon suivante ? commit ?) passe par AskUserQuestion, recommandation en premier.
- Il n'est pas expert et suit souvent la recommandation telle quelle : un désaccord argumenté lui
  sert plus qu'un accord, et un doute se dit comme un doute. Un fait sur PyTorch se vérifie dans la
  doc (context7) avant d'être affirmé ; un fait sur une méthode cite le papier.

## Livrer

- Un commit par test vert, fait par le tuteur (décision de Lambert, 6 novembre 2026), message en
  anglais, `<leçon>: <ce que le test vert prouve> (<n>/<total>)`, plus les lignes d'attribution que
  Claude Code impose. `uv run ruff format` sur ce qui a changé, avant.
- Une branche, `main`. Pas de PR, pas de CI : rien ici n'est de la production.
- Dépôt public. Point ouvert au 6 novembre 2026 : le compte GitHub qui l'héberge ; rien ne se pousse
  avant que Lambert l'ait nommé.

## Écrire le code

- Identifiants et commentaires en anglais. Un commentaire de forme sur chaque ligne qui crée un
  tenseur ou en change la forme : `# (B, T, C)`. Le tuteur ne relit pas un code qui n'en a pas.
- Une dépendance nouvelle entre par `pyproject.toml` et par une ligne ici, hors séance.
- `ruff format`, longueur 100. Python 3.14, celui de `.python-version`. Les hooks restent en
  Python 3.9 et bibliothèque standard, comme ceux d'equipe.

## Changer la méthode

En séance (`ML_SEANCE=1`, que `bin/ml seance` pose), la garde refuse au tuteur `CLAUDE.md`,
`.claude/`, `bin/`, `tests/`, `pyproject.toml` et `uv.lock` : il ne desserre pas ses propres règles
un soir de fatigue. Une règle change dans une session `claude` ordinaire, sans agent, ou à la main.

## Où sont les choses

- `courses/<parcours>/<nn-leçon>/` : `README.md` (vidéo, séances, quoi écrire), `test_*.py`
  (l'énoncé), le fichier d'implémentation de Lambert, `explore.py` (brouillon molten), `notes.md`,
  `exercises.md`, `ref/` s'il y a eu un palier 4. `courses/maths/` : le parcours parallèle, une séance
  par semaine.
- `core/` : le mini-torch de Lambert, promu leçon après leçon, testé.
- `papers/<année>-<nom>/` : `notes.md`, `repro.py`, `test_repro.py`, `questions.md`
  (`papers/README.md`).
- `rebuilds/<leçon>-<AAAA-MM>/` : les reconstructions mensuelles.
- `glossary.md`, `questions.md` : les deux fichiers que la révision et les tangentes nourrissent.
- `.claude/agents/` : tuteur (session principale), examinateur, contradicteur.
  `.claude/hooks/garde.py` et son test `tests/test_garde.py`. `bin/ml` : `seance`, `tests`.
- Hors dépôt : `~/notes/projets/ml/` (le journal, les critiques du contradicteur).

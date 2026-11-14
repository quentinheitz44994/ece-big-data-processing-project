# CLAUDE.md — Brief Claude Code : projet ECE Big Data Processing (IMDb)

> Ce fichier est lu automatiquement par Claude Code à la racine du dépôt.
> Il décrit le contexte, les règles, l'architecture et les tâches du projet.
> Langue de travail avec les membres du groupe : français. Langue de tout le code,
> des commentaires, des docstrings, de `PROJECT.md`, `REPORT.md` et des PR : **anglais**.

---

## 0. Contexte

- Cours : ECE Paris, *Big Data Processing* (fall 2026), enseignant Adaltas (`joe@adaltas.com`).
- Consignes officielles : `project_instructions.md` (copie à la racine du repo) et
  `README.md` du repo du cours `adaltas/ece-big-data-processing-fall-2026`.
- **Date limite : dimanche 15 novembre 2026, 23:59 (Europe/Paris).**
- Groupe (2 membres) :
  - Quentin HEITZ — GitHub `quentinheitz44994` — email : `<À COMPLÉTER>`
  - Maxence SIMONET — GitHub `<À COMPLÉTER>` — email : `<À COMPLÉTER>`
  - Numéro de groupe : `gr-<À COMPLÉTER>`
- Stack imposée : **Apache Spark (PySpark batch + Structured Streaming)** et **Apache Kafka**,
  le tout en Docker (base : environnement du lab 05 du cours).
- Machine de dev : Windows + WSL2 (Ubuntu), Docker Desktop, **16 Go de RAM** → tout doit
  tenir dans ~10 Go alloués à Docker (voir §3.4).

---

## 1. Règles non négociables (à respecter à chaque session)

### 1.1 Politique IA du cours

- L'IA est **autorisée pour le code** et doit être **déclarée** dans `PROJECT.md`.
- L'IA est **strictement interdite pour les explications et le raisonnement de `REPORT.md`**
  (sections *Methodological Explanation*, justification des choix, alternatives/trade-offs,
  *key takeaways*, description et intérêt de l'open question).

Conséquences pour Claude Code :

1. **Ne jamais rédiger de prose explicative dans `REPORT.md`.** Claude Code crée uniquement
   le squelette (titres) et insère les **résultats générés par le code** (tableaux, chiffres,
   métriques) entre des marqueurs automatiques. Chaque bloc de prose est un placeholder :
   ```markdown
   <!-- TODO(authors): written by Quentin / Maxence — AI-generated text prohibited -->
   ```
2. Les informations techniques factuelles (paramètres, seuils, schémas) vont dans les
   **docstrings, commentaires et `conf/settings.yaml`**, pas dans `REPORT.md`.
3. La section *AI/LLM declaration* de `PROJECT.md` doit être **exacte** : outil
   (Claude Code, Anthropic), et liste des tâches où il a été utilisé. Ne pas minimiser
   ni omettre l'usage. Les membres la relisent et la complètent.
4. Ne pas ajouter de trailer `Co-Authored-By` d'outil IA ni de mention « Generated with ... »
   dans les commits et les PR : l'usage de l'IA est déclaré uniquement dans `PROJECT.md`.

### 1.2 Standards Git (audités par l'enseignant)

- **Une tâche = une branche de feature** (`feat/...`, `fix/...`, `docs/...`) créée depuis `main` à jour.
- **Aucun commit direct sur `main`**, aucun upload web, aucun `git push --force` sur `main`.
- Chaque branche est poussée puis soumise via **Pull Request** (`gh pr create`) avec une
  description factuelle (quoi, comment tester).
- **Claude Code n'approuve ni ne merge jamais une PR.** Le relecteur est l'autre membre du groupe,
  qui teste, commente et approuve lui-même sur GitHub.
- Commits petits et atomiques, messages au format *Conventional Commits*
  (`feat(preparation): add null profiling job`).
- L'auteur git est la personne qui pilote la session (vérifier `git config user.name` /
  `user.email` en début de session et demander si ce n'est pas configuré).
- La répartition des branches entre Quentin et Maxence est donnée au §9 ; avant de commencer
  une tâche, **demander qui pilote la session** et vérifier que la branche lui correspond.

### 1.3 Données et éthique

- **Ne jamais committer de données** (`data/` est dans `.gitignore`, sauf `data/README.md`).
  Les fichiers IMDb sont sous licence non commerciale : téléchargement par script uniquement.
- Enrichissement : sources **humaines et ouvertes uniquement** (Wikipedia + Wikidata pour le
  mapping d'identifiants). **Aucun texte généré par machine** (pas de LLM, pas de résumé
  automatique, pas de descriptions Wikidata courtes, souvent générées par bot).
- Respect strict des politiques Wikimedia (User-Agent, rate limit, `maxlag`, `Retry-After`), cf. §6.
- Pas d'email personnel ni de secret en clair dans le code ; config via `.env` (gitignoré) +
  `.env.example` commité.

---

## 2. Arborescence cible

```text
.
├── CLAUDE.md                      # ce fichier
├── README.md                      # infos groupe (format exigé par le README du cours)
├── PROJECT.md                     # contributeurs, run guide from scratch, déclaration IA
├── REPORT.md                      # résultats + sections méthodo (prose = membres)
├── project_instructions.md        # copie des consignes
├── compose.yaml                   # kafka + spark (+ producer, profil "streaming")
├── docker/
│   ├── spark/Dockerfile           # FROM quay.io/jupyter/pyspark-notebook:<tag épinglé>
│   └── producer/Dockerfile        # python:3.12-slim
├── requirements.txt               # deps Python du conteneur spark
├── requirements-producer.txt
├── .env.example
├── .gitignore
├── pyproject.toml                 # ruff + black + pytest config
├── conf/settings.yaml             # TOUS les paramètres (seuils, années, top-N, chemins…)
├── scripts/
│   ├── download_imdb.sh           # télécharge les 7 TSV.gz (idempotent)
│   ├── run_preparation.sh
│   ├── run_exploration.sh
│   ├── run_enrichment.sh
│   ├── run_streaming.sh
│   ├── run_open_question.sh
│   └── render_report.py           # injecte outputs/*.md dans REPORT.md (entre marqueurs)
├── src/imdb_project/
│   ├── __init__.py
│   ├── common/        # spark_session.py, config.py, io.py, schemas.py, logging.py
│   ├── preparation/   # ingest.py, null_profile.py, quality_checks.py, cleaning.py
│   ├── exploration/   # q1_runtime_outliers.py … q8_multitalented.py
│   ├── enrichment/    # select_scope.py (Spark), fetch_wikidata.py, fetch_wikipedia.py,
│   │                  # http_client.py, build_enrichment.py (Spark)
│   ├── streaming/     # producer.py, build_lookup.py (Spark), stream_job.py,
│   │                  # late_event_injector.py, metrics_listener.py
│   └── open_question/
├── notebooks/                     # optionnel, exploration interactive uniquement
├── tests/                         # pytest + fixtures TSV miniatures (synthétiques)
├── outputs/                       # tableaux .md/.csv versionnés (petits) pour REPORT.md
└── data/                          # gitignoré : raw/ bronze/ silver/ gold/ enrichment/ streaming/
```

Principes :
- **Jobs = modules Python lancés via `spark-submit`** dans le conteneur (reproductible),
  pas des notebooks.
- Chaque job : fonction `run(spark, cfg)` pure + `main()` CLI (`argparse`, `--config`).
  Les transformations sont des fonctions `DataFrame -> DataFrame` testables.
- **Aucun paramètre en dur** : seuils, années, top-N, nombre de principals, langues wiki,
  durées de fenêtres… tout vient de `conf/settings.yaml` (exigence de scalabilité).
- Style : PEP 8, `ruff` + `black`, type hints, docstrings (Google style).

---

## 3. Environnement

### 3.1 Docker Compose

Partir du `compose.yaml` du lab 05 (`05.structured-streaming/lab_docker_wikistreams/`) :

- `kafka` : `apache/kafka-native:4.1.1`, KRaft, listeners `INTERNAL://kafka:19092`,
  `EXTERNAL://localhost:9092` (garder la config du lab).
- `spark` : image custom `docker/spark/Dockerfile` basée sur `quay.io/jupyter/pyspark-notebook`
  **avec un tag épinglé** (pas `latest`). Vérifier la version de Spark/Scala dans l'image
  (`spark-submit --version`) et utiliser le connecteur Kafka correspondant
  (`org.apache.spark:spark-sql-kafka-0-10_<scala>:<spark_version>`, le lab utilise
  `_2.13:4.1.0`). Monter `./src`, `./conf`, `./scripts`, `./data`, `./outputs`, `./notebooks`.
  Ports 8888 (Jupyter), 4040-4041 (Spark UI).
- `producer` : `docker/producer/Dockerfile`, profil compose `streaming`, bootstrap `kafka:19092`.
- Un service/commande d'init crée le topic Kafka (reprendre `admin.py` du lab, idempotent).

### 3.2 Point d'entrée « from scratch »

Le tout doit tourner en suivant uniquement `PROJECT.md` :

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec spark bash scripts/download_imdb.sh
docker compose exec spark bash scripts/run_preparation.sh
docker compose exec spark bash scripts/run_exploration.sh
docker compose exec spark bash scripts/run_enrichment.sh      # long : cache + reprise
docker compose --profile streaming up -d producer
docker compose exec spark bash scripts/run_streaming.sh       # 15-30 min
docker compose exec spark bash scripts/run_open_question.sh
docker compose exec spark python scripts/render_report.py
```

Les commandes doivent fonctionner depuis un terminal **WSL2/Linux/macOS** (bash).
Mentionner dans `PROJECT.md` que sous Windows il faut lancer depuis WSL2.

### 3.3 Données IMDb

`scripts/download_imdb.sh` télécharge depuis `https://datasets.imdbws.com/` les 7 fichiers :
`name.basics`, `title.akas`, `title.basics`, `title.crew`, `title.episode`,
`title.principals`, `title.ratings` (`.tsv.gz`) dans `data/raw/`. Idempotent (skip si présent,
`--force` pour re-télécharger), log de la date de snapshot (les données changent chaque jour →
noter la date de téléchargement dans `outputs/data_snapshot.md`).

Schémas observés (extraits réels) :
- `title.ratings` : `tconst, averageRating, numVotes` (~1,73 M lignes)
- `title.episode` : `tconst, parentTconst, seasonNumber, episodeNumber` (~10 M lignes)

### 3.4 Contraintes mémoire (16 Go hôte)

- Documenter dans `PROJECT.md` un `.wslconfig` avec `memory=10GB`.
- Spark local : `spark.driver.memory=6g`, `spark.sql.shuffle.partitions=64` (configurable),
  `spark.sql.adaptive.enabled=true`.
- **Convertir une fois les TSV en Parquet** (couche bronze), tous les jobs suivants lisent du Parquet.
- Éviter `collect()`/`toPandas()` sur de gros DataFrames ; n'exporter que des agrégats.

---

## 4. Section 1 — Data preparation

### 4.1 Ingestion (bronze)

- Lecture TSV : `sep="\t"`, `header=True`, **`quote` désactivé** (`option("quote", "\u0000")`)
  car les titres contiennent des guillemets, schéma explicite défini dans `common/schemas.py`
  (tout en `StringType` pour le bronze afin de ne rien perdre).
- **Ne pas** utiliser `nullValue="\\N"` au bronze : le profiling doit distinguer les cas.
- Écrire en Parquet `data/bronze/<table>/`.

### 4.2 Profiling des valeurs manquantes (Q1, Q2)

Pour **chaque colonne de chaque table**, calculer en un seul passage par table (agrégations
conditionnelles, pas une requête par colonne) :
- `n_total`, `n_null` (null Spark), `n_backslash_n` (`\N`), `n_empty` (`""`),
  `n_whitespace` (uniquement espaces), `n_missing_total`, `pct_missing`.
- Pour les colonnes tableau encodées en texte (`genres`, `primaryProfession`,
  `knownForTitles`, `directors`, `writers`, `characters`), compter aussi les tableaux vides
  (`[]`, `""`).
- Sorties : `outputs/preparation/null_profile.md` (+ `.csv`) trié par table/colonne, et
  `outputs/preparation/top5_null_columns.md` (top 5 global par `pct_missing`).

### 4.3 Contrôles de qualité (Q3)

Implémenter un module de règles déclaratives (`quality_checks.py`) : chaque règle =
`(rule_id, table, description, condition Spark)`, résultat = nombre de lignes en violation +
échantillon de 10 lignes. Règles minimales :

| rule_id | Règle |
|---|---|
| DQ01 | `deathYear < birthYear` (name.basics) |
| DQ02 | âge au décès > 120 ans ou `birthYear` futur |
| DQ03 | principal crédité sur un titre dont `startYear` > `deathYear` + 5 (posthume improbable, hors archive footage si détectable via `characters`/`job`) |
| DQ04 | principal crédité sur un titre sorti avant sa naissance (`startYear < birthYear`) |
| DQ05 | FK orphelines : `title.principals.tconst`/`nconst`, `title.ratings.tconst`, `title.crew.tconst`, `title.crew.directors/writers` (après explode), `title.episode.tconst/parentTconst`, `title.akas.titleId`, `name.basics.knownForTitles` (après explode) → anti-joins |
| DQ06 | `endYear < startYear` (title.basics) |
| DQ07 | `startYear` dans le futur au-delà de l'année courante + N (configurable) |
| DQ08 | `runtimeMinutes` ≤ 0 ou aberrant (> seuil configurable, ex. 1 000) |
| DQ09 | `isAdult` ∉ {0,1} ; valeurs non numériques dans les colonnes numériques |
| DQ10 | doublons de clés primaires (`tconst`, `nconst`, `(titleId, ordering)`, `(tconst, ordering)`) |
| DQ11 | épisodes dont `parentTconst` n'est pas de type `tvSeries`/`tvMiniSeries` |
| DQ12 | `averageRating` hors [1,10], `numVotes` ≤ 0 |
| DQ13 | genres inconnus (hors liste officielle IMDb) |
| DQ14 | `seasonNumber`/`episodeNumber` ≤ 0 ou non numériques |

Sortie : `outputs/preparation/quality_report.md` (règle, description, nb violations, % de la table).
Ajouter toute autre anomalie découverte pendant l'exploration (et la signaler aux membres).

### 4.4 Traitement (Q4) — couche silver

Stratégie à implémenter (les membres justifieront le choix dans REPORT.md) :
- Standardisation : `\N`, `""`, whitespace → `null` ; cast vers les bons types ;
  colonnes multi-valuées → `ArrayType(StringType)`.
- **Flagging plutôt que suppression** : colonne `dq_flags: array<string>` sur chaque table
  silver listant les règles violées par la ligne.
- **Quarantaine** : lignes structurellement invalides (PK dupliquée, FK orpheline sur table de
  faits) écrites dans `data/quarantine/<table>/` avec `dq_reason`, exclues du silver.
- Corrections déterministes seulement quand elles sont sûres (ex. `runtimeMinutes` ≤ 0 → null),
  jamais d'imputation inventée de valeurs.
- Silver écrit en Parquet partitionné quand pertinent (ex. `title.basics` par `titleType`).
- Tableau récapitulatif avant/après : `outputs/preparation/cleaning_summary.md`.

---

## 5. Section 2 — Data exploration (silver → gold)

Conventions communes (dans `settings.yaml`) :
- **Film long-métrage** : `titleType == "movie"` et `runtimeMinutes >= 40` (définition
  AMPAS/BFI ; seuil configurable). `isAdult == 0` par défaut (configurable).
- **Seuil de votes minimal** pour toute analyse de note : `min_votes` (défaut 1 000,
  configurable) ; l'appliquer partout et l'indiquer dans chaque sortie.
- Les genres sont explosés (`explode(genres)`) : un film compte dans chacun de ses genres.
- Chaque question = un module `exploration/qN_*.py` → `outputs/exploration/qN_*.md` (+ `.csv`),
  avec en tête du fichier les paramètres utilisés (générés automatiquement, pas de prose).

| # | Question | Implémentation par défaut (paramétrable) |
|---|---|---|
| Q1 | Films dont la durée est notablement différente de la moyenne du genre | Par genre : moyenne, écart-type, Q1/Q3. Outlier si `|z| > 2` **ou** hors `[Q1-1.5·IQR, Q3+1.5·IQR]`. Sortie : nb d'outliers par genre + liste (tconst, titre, année, durée, moyenne genre, z-score, méthode) ; liste complète en CSV, top 20 par genre en MD. |
| Q2 | Top 3 genres les plus populaires par année 1980–2025 | Popularité = **somme des `numVotes`** par (année, genre) ; calculer aussi nb de films et note moyenne pondérée. `Window.partitionBy(year).orderBy(desc)` + `dense_rank`. |
| Q3 | Comparer top 3 vs reste des genres par année | Par année : part des votes du top 3 vs reste, nb de films, note moyenne pondérée, ratio top3/reste ; évolution par décennie ; stabilité du top 3 (genres présents le plus d'années). |
| Q4 | Réalisateurs avec exactement 1 film ≥ 8.0 et ≥ 2 autres films de moyenne ≤ 6.0 | Réalisateurs via `title.crew.directors` (explode) ∪ `principals.category == "director"` (dédoublonnés). Films (définition long-métrage) avec `numVotes >= min_votes`. Conditions : `count(rating >= 8.0) == 1` et, parmi les **autres** films, `count >= 2` et `avg(rating) <= 6.0`. |
| Q5 | Séries ≥ 3 saisons de ≥ 10 épisodes, pire épisode dans la dernière saison, meilleur dans les saisons 1–2 | Épisodes notés (`seasonNumber` non null). Saisons « éligibles » = ≥ 10 épisodes notés. Série retenue si ≥ 3 saisons éligibles. Dernière saison = `max(seasonNumber)` de la série. Pire = `min(averageRating)`, meilleur = `max` ; gérer les égalités (paramètre : `any`/`all`, défaut `all` = toutes les ex-aequo doivent satisfaire la condition). `min_votes_episode` configurable (défaut 50). |
| Q6 | Acteurs/actrices à succès dans des films de langues d'origine différentes ; liste de ceux avec ≥ 3 langues | « Succès » = `averageRating >= 7.0` et `numVotes >= 10 000` (configurables). Langue d'origine : **Wikidata P364** (original language of film) via mapping IMDb ID P345, sur le seul sous-ensemble des films à succès (borné) ; fallback `title.akas` (`isOriginalTitle == 1` + `language`, puis région) avec colonne `language_source`. Rapporter la couverture (% de films avec langue connue). Sorties : acteurs avec ≥ 2 langues, puis ≥ 3 langues. Réutiliser le client HTTP de l'enrichissement (§6) et le cache. |
| Q7 | Acteurs avec carrière ≥ 20 ans, ≥ 15 films, pic de popularité précoce | Carrière = `max(startYear) - min(startYear)` sur leurs films (catégories actor/actress). Pic précoce si le film le mieux noté se situe dans le **premier tiers** de la carrière **et** note moyenne 1ʳᵉ moitié > 2ᵉ moitié. Donner aussi la pente d'une régression linéaire note ~ année (via agrégats Spark, `covar_samp/var_samp`) comme mesure alternative. |
| Q8 | Professionnels « multi-talents » et performance quand ils cumulent les rôles sur un même projet | Rôles normalisés {director, writer, actor} depuis `principals.category` + `title.crew`. Multi-talent = ≥ 2 rôles distincts sur l'ensemble de la carrière (avec ≥ k titres par rôle, k configurable). Pour chaque personne : note moyenne des titres où elle cumule ≥ 2 rôles vs titres à rôle unique ; comparaison appariée (différence par personne, médiane, % de personnes meilleures en cumul), ventilée par combinaison de rôles (director+actor, writer+director, triple). |

---

## 6. Section 3 — Data enrichment

### 6.1 Périmètre (Spark)

`enrichment/select_scope.py` :
- Films long-métrage sortis entre `year_min=1980` et `year_max=2025`.
- **Top 10 par (genre, année)** classés par `numVotes` desc puis `averageRating` desc
  (critère et N configurables). Dédoublonner par `tconst` (un film multi-genre n'est
  récupéré qu'une fois ; garder la liste de ses (genre, année, rang)).
- **3 principals par film** : les 3 premiers par `ordering` parmi les catégories
  `actor, actress, director, writer` (catégories et N configurables).
- Sortie : `data/enrichment/scope_films.parquet`, `scope_people.parquet` + compteurs.
- Le code ne doit dépendre d'aucune constante de périmètre : passer `top_n=None` ou
  `year_min=None` doit traiter **tout** le dataset sans changement de code.

### 6.2 Collecte (hors Spark, autorisé)

Source unique : **Wikipedia (anglais par défaut)**, Wikidata uniquement pour le mapping d'IDs.

1. **Mapping IMDb → Wikipedia** : SPARQL Wikidata (`https://query.wikidata.org/sparql`),
   par lots de ~200 IDs avec `VALUES ?imdb { "tt…" … }` sur `wdt:P345`, récupérer l'item et le
   sitelink `enwiki`. Même chose pour les `nm…`.
2. **Synopsis film** : MediaWiki Action API (`https://en.wikipedia.org/w/api.php`),
   `action=parse&prop=sections` puis section dont le titre ∈ {Plot, Synopsis, Premise,
   Plot summary} → texte brut (wikitext → texte via `action=parse&prop=text` + nettoyage
   HTML, ou `prop=extracts&explaintext` puis découpage par section). Fallback : intro de
   l'article avec `synopsis_type = "lead_section"` et une note.
3. **Biographie** : `action=query&prop=extracts&exintro&explaintext` (lots de 20 titres max)
   + champs structurés Wikidata (date/lieu de naissance, date de décès, nationalité) en
   données brutes (pas les descriptions textuelles Wikidata).
4. **Révision** : récupérer `revid` pour construire une URL permanente
   (`https://en.wikipedia.org/w/index.php?oldid=<revid>`).

Politesse / conformité (`http_client.py`, réutilisé partout) :
- `User-Agent` conforme à la politique Wikimedia :
  `ECE-BigData-IMDb-Project/1.0 (<contact email depuis .env>)`.
- **Requêtes séquentielles** (pas de parallélisme), débit configurable (défaut ≤ 1 req/s),
  `maxlag=5`, gestion `429`/`503` avec `Retry-After` + backoff exponentiel, timeout.
- Lecture et respect de `robots.txt` ; utiliser les API, pas le scraping HTML des pages.
- **Cache disque** de chaque réponse brute (`data/enrichment/raw/<source>/<id>.json`) →
  reprise après interruption, aucune requête répétée.
- Options CLI `--limit` (tests rapides) et `--resume`.
- Logger : nb requêtes, nb 429, durée, taux de couverture.

### 6.3 Construction (Spark obligatoire)

`enrichment/build_enrichment.py` : lit le cache JSON brut avec Spark, **schéma imposé**
(`StructType` explicite, mode `FAILFAST` ou colonne `_corrupt_record` contrôlée), nettoyage
(trim, normalisation espaces, suppression références `[1]`, longueur min), jointures avec le
silver, écriture `data/gold/enriched_films/` et `data/gold/enriched_people/`.

Colonnes obligatoires de lignage sur **chaque** enregistrement :
`source_name`, `source_url`, `source_revision_id`, `source_permalink`, `retrieved_at`,
`license` (`CC BY-SA 4.0`), `enrichment_status` (`ok` / `partial` / `not_found` /
`no_plot_section`), `enrichment_note` (texte **programmatique** quand l'info manque,
ex. `"No enwiki sitelink for Q123 (P345=tt…)"`).

Sorties pour le rapport : `outputs/enrichment/coverage.md` (taux de couverture films /
personnes, par statut, par décennie), `outputs/enrichment/sample.md` (10 lignes d'exemple
tronquées), stats de collecte (requêtes, durée, erreurs).

---

## 7. Section 4 — Streaming (Kafka + Structured Streaming)

### 7.1 Producteur

`streaming/producer.py` (service `producer`) :
- Source : Wikimedia EventStreams `https://stream.wikimedia.org/v2/stream/recentchange`
  (SSE ; via `requests` en streaming ou `pywikibot.comms.eventstreams` comme dans le lab,
  mais **un seul flux** `recentchange` pour éviter les doublons du lab).
- Filtre producteur léger : `wiki ∈ {enwiki, frwiki, …}` (configurable), `type ∈ {edit, new}`,
  namespace 0.
- Clé Kafka = `meta.id` ; valeur = JSON brut ; topic `wikistreams` (configurable) ;
  durée de run configurable (défaut 30 min), arrêt propre (`flush`).
- User-Agent conforme, reconnexion SSE avec `Last-Event-ID`.

### 7.2 Lookup de pertinence (batch Spark)

`streaming/build_lookup.py` : table statique `data/gold/wiki_lookup/` de titres Wikipedia
liés à l'IMDb, construite à partir :
- des titres Wikipedia déjà récupérés par l'enrichissement (films + personnes) ;
- d'un ensemble élargi : films/personnes les plus votés (top `lookup_size`, configurable,
  défaut ~50 000 titres) mappés via Wikidata P345 (même client, même cache).
Colonnes : `wiki`, `page_title_normalized`, `imdb_id`, `entity_type`, `source_url`.

### 7.3 Job de streaming

`streaming/stream_job.py` :
- `readStream` Kafka (`kafka:19092`), schéma explicite du JSON recentchange
  (`meta.id`, `meta.dt`, `title`, `wiki`, `type`, `bot`, `minor`, `user`, `comment`,
  `length.old/new`, `revision.old/new`, `namespace`, `server_name`).
- `event_time = to_timestamp(meta.dt)`.
- Pertinence = **jointure stream-statique** (broadcast) sur `(wiki, titre normalisé)` avec le
  lookup **OU** motif regex sur le titre (`\((\d{4} )?film\)|\(TV series\)|\(miniseries\)|\(actor\)|\(actress\)|\(director\)`).
  Colonne `match_reason`. Le critère doit garantir plusieurs correspondances en 15–30 min :
  le vérifier avec un premier run et élargir (lookup_size, wikis) si besoin.
- **Données tardives** : `withWatermark("event_time", "<watermark_delay>")` (défaut 10 min),
  déduplication `dropDuplicatesWithinWatermark(["event_id"])`, agrégations fenêtrées
  **tumbling** (5 min) et **sliding** (10 min / pas 5 min) : nb d'éditions pertinentes par
  `entity_type`, par wiki, bots vs humains, delta de taille moyen, top pages.
- Sinks : événements enrichis → Parquet `data/streaming/matched_events/` (append,
  checkpoint dédié) ; agrégats → Parquet (append) + console.
- **Métriques** : `StreamingQueryListener` Python qui écrit chaque `QueryProgressEvent` en
  JSON lines (`outputs/streaming/progress.jsonl`) : `numInputRows`, `inputRowsPerSecond`,
  `processedRowsPerSecond`, `durationMs`, `stateOperators.numRowsDroppedByWatermark`,
  `eventTime.watermark`.
- **Démonstration du retard** : `late_event_injector.py` republie dans Kafka un échantillon
  d'événements avec `meta.dt` décalé (ex. −30 min, −5 min) pour montrer ce qui est
  accepté vs écarté par le watermark ; les compteurs viennent des métriques.
- `run_streaming.sh` : durée configurable (défaut 20 min), puis `stop()` propre et
  génération de `outputs/streaming/summary.md` (tableau des métriques par batch, totaux,
  nb d'événements pertinents, exemples de correspondances, effet du watermark).

---

## 8. Open question

- **Le choix et la formulation de la question appartiennent aux membres du groupe.**
  Avant de coder cette partie, **demander** à Quentin/Maxence quelle question ils retiennent.
- Pistes possibles à leur soumettre (sans rédiger de justification) :
  1. Collaborations récurrentes réalisateur–acteur : les films d'une collaboration répétée
     sont-ils mieux notés que la première collaboration ? (IMDb seul, self-joins multiples)
  2. Effet d'une nomination/victoire aux Oscars (Wikidata P1411/P166) sur les notes et votes des
     films suivants d'un acteur, comparé à des pairs non nominés.
  3. Lien entre activité Wikipedia (taille/nombre de révisions de la page) et popularité IMDb
     des films 1980–2025.
- Exigences : multi-table joins, toute donnée externe suit les règles du §6 (lignage, sources
  humaines, rate limits), sorties en tableaux dans `outputs/open_question/`.

---

## 9. Plan de travail, branches et répartition

Ordre conseillé (deadline 15/11 23:59). Chaque ligne = 1 branche = 1 PR relue par l'autre membre.

| # | Branche | Pilote | Relecteur | Contenu |
|---|---|---|---|---|
| 1 | `feat/project-setup` | Quentin | Maxence | compose, Dockerfiles, `pyproject`, structure, `.gitignore`, README groupe |
| 2 | `feat/data-ingestion` | Maxence | Quentin | download script, schémas, bronze Parquet |
| 3 | `feat/null-profiling` | Quentin | Maxence | §4.2 |
| 4 | `feat/data-quality-checks` | Maxence | Quentin | §4.3 |
| 5 | `feat/data-cleaning-silver` | Quentin | Maxence | §4.4 |
| 6 | `feat/exploration-genres-runtime` | Maxence | Quentin | Q1, Q2, Q3 |
| 7 | `feat/exploration-directors-series` | Quentin | Maxence | Q4, Q5 |
| 8 | `feat/http-client-wikimedia` | Maxence | Quentin | `http_client.py`, cache, mapping Wikidata |
| 9 | `feat/exploration-actors` | Quentin | Maxence | Q6, Q7, Q8 |
| 10 | `feat/enrichment-pipeline` | Maxence | Quentin | §6.1–6.3 |
| 11 | `feat/streaming-producer-lookup` | Quentin | Maxence | §7.1, §7.2 |
| 12 | `feat/streaming-job` | Maxence | Quentin | §7.3 |
| 13 | `feat/open-question` | à définir | autre | §8 |
| 14 | `docs/project-md` | Quentin | Maxence | `PROJECT.md` complet |
| 15 | `docs/report-results` | Maxence | Quentin | squelette `REPORT.md` + `render_report.py` |

Les membres peuvent réattribuer ; l'objectif est une contribution équilibrée et des
discussions de PR réelles (les commentaires de review sont écrits par les membres).

Workflow d'une tâche :
1. `git switch main && git pull` puis `git switch -c <branche>`.
2. Implémenter + tests (`pytest`) + `ruff check` + `black --check`.
3. Exécuter le job dans le conteneur sur les vraies données (ou `--limit`) et vérifier la sortie.
4. Commits atomiques, `git push -u origin <branche>`, `gh pr create` (titre + description :
   changements, commandes de test, sorties produites). **Ne pas merger.**
5. Résumer aux membres ce qui a été fait et ce qu'il faut relire/tester.

---

## 10. Contenu attendu des livrables Markdown

### README.md (format du cours)

```text
- Group: gr-XX
- Quentin HEITZ, quentinheitz44994
- Maxence SIMONET, <github username>
```

### PROJECT.md

1. Contributeurs (nom + email, placeholders tant que non fournis).
2. Prérequis (Docker Desktop + WSL2 sous Windows, `.wslconfig`, ~25 Go disque, RAM).
3. Run guide pas à pas **from scratch** (§3.2), durées approximatives de chaque étape,
   vérifications attendues, dépannage (ports occupés, mémoire, topic Kafka).
4. Arborescence et description des modules.
5. **AI/LLM tools declaration** : tableau exact `Tool | Version/model | Tasks` — Claude Code
   (Anthropic) pour la génération et le débogage du code, de la configuration Docker et des
   scripts ; préciser explicitement qu'aucun outil IA n'a été utilisé pour les explications
   de `REPORT.md`. Les membres vérifient et complètent ce tableau.

### REPORT.md (squelette uniquement)

```markdown
# Report
## 1. Data Preparation
### Results
<!-- AUTO:preparation:start --> … <!-- AUTO:preparation:end -->
### Methodological Explanation
<!-- TODO(authors): written by Quentin / Maxence — AI-generated text prohibited -->
#### Methodology and why it was chosen
#### Alternatives considered and trade-offs
## 2. Data Exploration   (même structure, une sous-section Results par question)
## 3. Data Enrichment    (même structure)
## 4. Streaming          (même structure + sous-section "Late-arriving data" en TODO)
## 5. Open Question      (Question & motivation / Data / Results / Key takeaways / Methodology : TODO sauf Results)
```

`scripts/render_report.py` remplace uniquement le contenu entre les marqueurs `AUTO:*`
par les fichiers de `outputs/` ; il ne touche jamais aux blocs `TODO(authors)` ni au texte
rédigé par les membres.

Pour aider les membres à rédiger eux-mêmes, Claude Code peut fournir **à l'oral dans la
session** (pas dans le repo) les faits techniques utiles : paramètres utilisés, volumétries,
temps d'exécution. Il ne rédige pas les paragraphes.

---

## 11. Checklist finale (avant l'email de soumission)

- [ ] Clone neuf du repo + suivi strict de `PROJECT.md` → tout tourne.
- [ ] `pytest`, `ruff`, `black --check` passent.
- [ ] Toutes les sorties présentes dans `outputs/` et injectées dans `REPORT.md`.
- [ ] Plus aucun `TODO(authors)` vide (rédigé par les membres).
- [ ] Déclaration IA à jour et exacte dans `PROJECT.md`.
- [ ] Toutes les branches mergées via PR approuvées, aucun commit direct sur `main`.
- [ ] Aucune donnée ni secret commité.
- [ ] Email à `joe@adaltas.com` (sujet `ECE big data processing Gr-x git repo link`, cc Maxence)
      envoyé par les membres.

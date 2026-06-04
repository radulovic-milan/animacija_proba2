# Fracture Network Animation

Manim animacija koja prikazuje **mrežu ispucalih stijena (fracture network)** u 2D, sa česticama vode koje se kreću kroz pukotine od vrha prema dnu pod uticajem gravitacije.

## Sadržaj repozitorija

```
animacija_proba2/
├── fracture_network.py   # Manim animacija
└── README.md             # Ovaj fajl
```

## Šta animacija prikazuje

- **Mreža pukotina** — nasumično generisane linije koje predstavljaju horizontalne, vertikalne i dijagonalne pukotine u stijeni (bedding planes, joints, diagonal fractures)
- **Čestice vode** — 12 plavih čestica koje polaze sa površine i prolaze kroz pukotine prema dnu, simulirajući gravitacioni tok podzemnih voda
- **Tragovi čestica** — svaka čestica ostavlja blag plavi trag koji naglašava preferentne putanje toka
- **Animovano crtanje** — pukotine se postepeno iscrtavaju na početku, a zatim čestice kreću u talasima

## Zahtjevi

### Python paketi

```bash
pip3 install manim
```

> Manim automatski instalira sve potrebne zavisnosti (numpy, scipy, cairo, ffmpeg, itd.)

### Sistemski alati

- **Python 3.8+**
- **FFmpeg** — za renderovanje videa

Provjeri da li je FFmpeg instaliran:
```bash
ffmpeg -version
```

Ako nije, instaliraj ga:
- **macOS:** `brew install ffmpeg`
- **Ubuntu/Debian:** `sudo apt install ffmpeg`
- **Windows:** Preuzmi sa [ffmpeg.org](https://ffmpeg.org/download.html)

## Pokretanje animacije

### Pregled (niska rezolucija, brzo)
```bash
manim -ql fracture_network.py FractureNetworkAnimation
```

### Visoka rezolucija (1080p)
```bash
manim -qh fracture_network.py FractureNetworkAnimation
```

### 4K rezolucija
```bash
manim -qk fracture_network.py FractureNetworkAnimation
```

### Samo jedna slika (preview kadar)
```bash
manim -s fracture_network.py FractureNetworkAnimation
```

Renderovani video će se nalaziti u:
```
media/videos/fracture_network/<rezolucija>/FractureNetworkAnimation.mp4
```

## Parametri koje možeš mijenjati

U fajlu `fracture_network.py`, funkcija `generate_fracture_network()` prima sljedeće parametre:

| Parametar | Zadana vrijednost | Opis |
|-----------|------------------|------|
| `n_fractures` | 35 | Ukupan broj pukotina |
| `width` | 14 | Širina scene |
| `height` | 8 | Visina scene |

U sekciji `construct()` možeš promijeniti:
- **`start_xs`** — početne X pozicije čestica (trenutno 12 čestica)
- **`particle_color`** — boja čestica (zadano: `#44aaff`)
- **`run_time`** — brzina animacije čestica

## Naučna pozadina

Mreža pukotina u stijeni kontroliše tok podzemnih voda. Voda ne teče ravnomjerno kroz stijenu, već preferentno kroz pukotine, koje mogu biti:

- **Horizontalne pukotine (bedding planes)** — nastaju sedimentacijom
- **Vertikalne pukotine (joints)** — nastaju tektonskim stresom
- **Dijagonalne pukotine** — nastaju smicanjem (shear fractures)

Ova animacija ilustruje koncept **preferentnih putanja toka** (*preferential flow pathways*), koji je ključan za hidrogeologiju, inženjering podzemnih voda i skladištenje CO₂.

## Autor

Milan Radulović  
[radulovic.m.milan@gmail.com](mailto:radulovic.m.milan@gmail.com)

## Licenca

MIT

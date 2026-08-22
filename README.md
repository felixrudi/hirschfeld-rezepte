# hirschfeld-rezepte

Rezept- und Vorratsapp unter **[food.hirschfeld.at](https://food.hirschfeld.at)**.
Svelte + Vite, statisch gebaut, hinter Authelia-SSO auf der Hetzner-Box.

Zeigt Felix' Rezepte mit Nährwerten, Filtern und einem **Kochmodus**, der ein Rezept in
echte Einzelschritte zerlegt statt eine Textwand anzuzeigen. Dazu Kühlschrank- und
Tiefkühler-Tracker, Wochenplaner und eine abgeleitete Einkaufsliste.

---

## Woher die Rezepte kommen

Das ist die wichtigste Sache im Repo, weil sie nicht offensichtlich ist:

```
Obsidian Cloud Vault/Rezepte/**.md   (Quelle der Wahrheit — Markdown + Frontmatter)
            │
            │  scripts/generate_recipes_data.py
            ▼
src/lib/recipesData.js               (AUTO-GENERATED, nicht von Hand editieren)
            │
            ▼
      Vite-Build → dist/ → Docker/nginx
```

`recipesData.js` exportiert `initialRecipes`, `initialLeftovers` und `initialFreezerItems`.
Alle drei sind **statisch in den Build eingebacken**. Die App spricht zur Laufzeit mit keinem
Backend.

**Rezepte ändern heißt: Markdown im Vault ändern, Generator laufen lassen, neu bauen.**

```bash
python3 scripts/generate_recipes_data.py
npm run build
```

Der Generator liest
`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Cloud Vault/Rezepte`,
nimmt den Ordner als Kategorie und das Frontmatter-Feld `titel` als Titel.

---

## Entwicklung

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # → dist/
```

## Deployment

Docker-Image mit nginx (`Dockerfile` + `nginx.conf`), ausgerollt über Coolify auf die
Hetzner-Box. Vor dem Bauen den Generator laufen lassen, sonst geht der Vault-Stand nicht mit.

## Authentifizierung

Macht **Authelia**, nicht die App. Der frühere In-App-Passcode ist seit dem SSO-Rollout
(03.08.2026) deaktiviert — `isAuthenticated` startet auf `true`. Keine zweite Login-Hürde
einbauen.

---

## Bekannte Grenzen

| Was | Stand |
|---|---|
| **Rezept-Editor speichert nicht dauerhaft** | `handleSaveRecipe` ändert nur das In-Memory-Array. Nach einem Reload ist die Änderung weg. Faktisch ein Vorschau-Feature — echte Änderungen gehören in den Vault. |
| **`src/lib/teableClient.js` ist toter Code** | Wird von keiner Datei importiert. Stammt aus einem früheren Anlauf, die Daten in Teable zu halten (Tabellen Rezepte / Kühlschrank / Tiefkühler / Wochenplan). Entweder anschließen oder löschen — aktuell ist es eine Falle für den nächsten Leser. |
| **Kühlschrank & Tiefkühler sind statisch** | Kommen wie die Rezepte aus dem generierten File, kein Bestandsabgleich zur Laufzeit. |

## Ernährungs-Constraint

**Kein Eiweiß / Eiklar.** Unverträglichkeit — keine Rezepte mit Rührei oder Eiweiß anlegen
oder vorschlagen.

---

## Struktur

```
src/
  App.svelte                      Zustand, Filter, Modals
  lib/
    recipesData.js                AUTO-GENERATED — nicht editieren
    teableClient.js               ungenutzt (siehe oben)
    components/
      RecipeCard.svelte           Kachel in der Galerie
      KitchenStepperModal.svelte  Kochmodus mit Einzelschritten
      RecipeEditModal.svelte      Editor (flüchtig)
      FridgeTracker.svelte        Kühlschrank
      FreezerTracker.svelte       Tiefkühler
      Wochenplaner.svelte         Wochenplan
      SmartShoppingList.svelte    abgeleitete Einkaufsliste
      Header.svelte
scripts/
  generate_recipes_data.py        Vault → recipesData.js
```

Projektdoku bei Henry: `modules/projekte-doku/hirschfeld-rezepte.md`,
Arbeitsstand: `modules/werkbank/hirschfeld-rezepte/stand.md`.

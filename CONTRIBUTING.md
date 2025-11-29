# Contribució al projecte Actor Recognition App 🎭

Gràcies per voler col·laborar! Aquest document estableix les normes bàsiques per participar en el projecte.

---

## 📝 Com començar

1. **Fork** del repositori i crea una branca nova:
   ```bash
   git checkout -b feature/nom-funcionalitat
   ```
2. Fes els teus canvis i comprova que passen els tests.
3. Obre un **Pull Request** cap a la branca `main`.

---

## 📌 Issues

- Abans de crear una issue, comprova si ja existeix.
- Sigues clar i concís en la descripció.
- Inclou passos per reproduir el problema, si és un bug.
- Etiqueta la issue amb el tipus corresponent (`bug`, `enhancement`, `documentation`, etc.).

---

## 🔑 Estil de codi

- **Python**: segueix [PEP8](https://peps.python.org/pep-0008/).
- Usa noms de variables i funcions descriptius.
- Mantén el codi modular i documentat.
- Afegeix comentaris quan el codi no sigui trivial.

---

## 🧪 Tests

- Cada nova funcionalitat ha d’incloure tests.
- Executa els tests abans de fer commit:
  ```bash
  pytest
  ```
- El workflow de GitHub Actions comprovarà automàticament que tot passa correctament.

---

## 📄 Commits

- Escriu missatges de commit clars i significatius.
- Format recomanat:
  ```
  tipus: descripció breu
  ```
  Exemples:
  - `feat: afegit endpoint /actors/{id}`
  - `fix: correcció bug en identificació`
  - `docs: actualitzat README amb instruccions`

---

## 🚀 Pull Requests

- Explica què fa la PR i per què és necessària.
- Adjunta captures o exemples si cal.
- Assegura’t que la PR passa els workflows de CI.

---

## 📜 Llicència

En contribuir, acceptes que el teu codi es distribueixi sota la [llicència MIT](LICENSE).
